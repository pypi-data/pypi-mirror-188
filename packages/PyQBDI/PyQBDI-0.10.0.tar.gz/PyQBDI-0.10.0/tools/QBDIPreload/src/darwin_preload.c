/*
 * This file is part of QBDI.
 *
 * Copyright 2017 - 2023 Quarkslab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "darwin_exceptd.h"
#include "QBDIPreload.h"

#include <mach-o/dyld.h>
#include <mach-o/loader.h>
#include <mach/mach.h>
#include <mach/mach_error.h>
#include <mach/mach_init.h>
#include <mach/mach_port.h>
#include <mach/mach_traps.h>
#include <mach/mach_vm.h>
#include <mach/task.h>
#include <mach/thread_act.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

#include <QBDI.h>

#if defined(QBDI_ARCH_X86)
#include "X86/osx_X86.h"
#elif defined(QBDI_ARCH_X86_64)
#include "X86_64/osx_X86_64.h"
#elif defined(QBDI_ARCH_AARCH64)
#include "AARCH64/osx_AARCH64.h"
#else
#error "Architecture not supported"
#endif

#define DYLD_INTERPOSE(_replacment, _replacee)                                \
  __attribute__((used)) static struct {                                       \
    const void *replacment;                                                   \
    const void *replacee;                                                     \
  } _interpose_##_replacee __attribute__((section("__DATA,__interpose"))) = { \
      (const void *)(unsigned long)&_replacment,                              \
      (const void *)(unsigned long)&_replacee};

static const size_t STACK_SIZE = 8388608;

static bool HAS_EXITED = false;
static bool HAS_PRELOAD = false;
static bool DEFAULT_HANDLER = false;
static GPRState ENTRY_GPR;
static FPRState ENTRY_FPR;

static struct ExceptionHandler *MAIN_EXCEPTION_HANDLER = NULL;

static void writeCode(rword address, void *data, size_t data_size) {
  kern_return_t kr;
  vm_prot_t cur_protection, max_protection;
  task_t self = mach_task_self();
  int pageSize = getpagesize();

  // 1. copy the page data to another pages
  void *pageAddr = mmap(NULL, pageSize, PROT_READ | PROT_WRITE,
                        MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (pageAddr == MAP_FAILED) {
    perror("Failed to create a new page");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  rword addressPage = address & ~(pageSize - 1);

  memcpy(pageAddr, (void *)addressPage, pageSize);

  // 2. write data
  memcpy(pageAddr + (address & (pageSize - 1)), data, data_size);

  // 3. protect page to RX
  kr = mach_vm_protect(self, (mach_vm_address_t)pageAddr, pageSize, false,
                       VM_PROT_READ | VM_PROT_EXECUTE);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to change memory protection to RX: %s",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // 4. remap page
  mach_vm_address_t remapAddr = addressPage;
  kr = mach_vm_remap(self, &remapAddr, pageSize, 0,
                     VM_FLAGS_OVERWRITE | VM_FLAGS_FIXED, self,
                     (mach_vm_address_t)pageAddr, TRUE, &cur_protection,
                     &max_protection, VM_INHERIT_COPY);

  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to remap the page to the origin address: %s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }
  if (remapAddr != addressPage) {
    fprintf(stderr,
            "Remap fail to use the given address: "
            "0x%" PRIRWORD " != 0x%" PRIRWORD "\n",
            (rword)remapAddr, (rword)address);
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // 5. unmap the temporary map
  if (munmap(pageAddr, pageSize) == -1) {
    perror("Failed to munmap");
  }
}

static struct {
  rword originPageAddr;
  rword remapPageAddr;
  int size;
} ENTRY_BRK;

void setEntryBreakpoint(rword address) {
  kern_return_t kr;
  vm_prot_t cur_protection, max_protection;

  // 1. get current mach_port_t from current task
  mach_port_t task;
  task_t self = mach_task_self();
  kr = task_for_pid(self, getpid(), &task);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to get mach_port for self pid: %s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // 2. iterate on region to find the region of address
  uint32_t depth = 1;
  vm_size_t size = 0;
  vm_address_t addr = 0, next = addr;

  while (1) {
    struct vm_region_submap_info_64 basic_info;
    mach_msg_type_number_t count = VM_REGION_SUBMAP_INFO_COUNT_64;
    kr = vm_region_recurse_64(task, &next, &size, &depth,
                              (vm_region_recurse_info_t)&basic_info, &count);
    if (kr != KERN_SUCCESS) {
      fprintf(stderr, "Cannot found address 0x%" PRIRWORD " : %s\n", address,
              mach_error_string(kr));
      exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
    }

    if (basic_info.is_submap) {
      depth++;
      continue;
    }

    addr = next;
    next += size;

    // Found region of address
    if (addr <= address && address < addr + size) {
      size_t pageSize = getpagesize();
      // align addr and size
      ENTRY_BRK.originPageAddr = addr & ~(pageSize - 1);
      ENTRY_BRK.size =
          ((addr - ENTRY_BRK.originPageAddr) + size + pageSize - 1) &
          ~(pageSize - 1);
      break;
    }
  }

  // 3. remap the region
  ENTRY_BRK.remapPageAddr = 0;
  kr = mach_vm_remap(self, &ENTRY_BRK.remapPageAddr, ENTRY_BRK.size, 0,
                     VM_FLAGS_ANYWHERE, self, ENTRY_BRK.originPageAddr, TRUE,
                     &cur_protection, &max_protection, VM_INHERIT_COPY);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr,
            "Failed to remap original page before insert breakpoint: "
            "%s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // 4. write the breakpoint
  writeCode(address, (void *)&BRK_INS, sizeof(BRK_INS));
}

void unsetEntryBreakpoint() {
  kern_return_t kr;
  vm_prot_t cur_protection, max_protection;
  task_t self = mach_task_self();

  // 1. remap original code
  kr = mach_vm_remap(self, &ENTRY_BRK.originPageAddr, ENTRY_BRK.size, 0,
                     VM_FLAGS_OVERWRITE | VM_FLAGS_FIXED, self,
                     ENTRY_BRK.remapPageAddr, TRUE, &cur_protection,
                     &max_protection, VM_INHERIT_COPY);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr,
            "Failed to remap original page after inserted breakpoint: "
            "%s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // 2. remove copy
  if (munmap((void *)ENTRY_BRK.remapPageAddr, ENTRY_BRK.size) == -1) {
    perror("Failed to munmap");
  }
}

rword getEntrypointAddress() {
  uint32_t imageIndex = -1;
  bool foundImageIndex = false;
  char *execPath = NULL;
  char *execBaseName = NULL;
  uint32_t execPathLen = 0;

  unsigned i = 0, j = 0;
  rword segaddr = 0;
  rword entryoff = 0;
  rword slide;
  const struct MACH_HEADER *header;

  // get path of the binary and extract basename
  _NSGetExecutablePath(NULL, &execPathLen);
  if (execPathLen <= 0) {
    fprintf(stderr, "Fail to get binary path\n");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }
  execPathLen += 1;
  execPath = (char *)malloc(execPathLen);
  if (execPath == NULL) {
    fprintf(stderr, "Buffer allocation fail\n");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }
  memset(execPath, '\0', execPathLen);
  if (_NSGetExecutablePath(execPath, &execPathLen) != 0) {
    free(execPath);
    fprintf(stderr, "Fail to get binary path\n");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  execBaseName = strrchr(execPath, '/');
  if (execBaseName == NULL) {
    execBaseName = execPath;
  } else {
    // skip '/'
    execBaseName++;
  }

  // search image index that match the basename
  while (!foundImageIndex) {
    const char *currentImageName = _dyld_get_image_name(++imageIndex);
    const char *currentBaseName;
    if (currentImageName == NULL) {
      free(execPath);
      fprintf(stderr, "Fail to found binary index\n");
      exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
    }
    currentBaseName = strrchr(currentImageName, '/');
    if (currentBaseName == NULL) {
      currentBaseName = currentImageName;
    } else {
      // skip '/'
      currentBaseName++;
    }
    foundImageIndex = (strcmp(currentBaseName, execBaseName) == 0);
  }
  free(execPath);

  // get header of the binary
  slide = _dyld_get_image_vmaddr_slide(imageIndex);
  header = (struct MACH_HEADER *)_dyld_get_image_header(imageIndex);

  // Checking that it is indeed a mach binary
  if (header->magic != MACH_MAGIC) {
    fprintf(stderr, "Process is not a mach binary\n");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // Find entrypoint and _TEXT segment command - Logic copied from
  // libmacho/getsecbyname.c
  struct load_command *cmd =
      (struct load_command *)((char *)header + sizeof(struct MACH_HEADER));
  for (i = 0; i < header->ncmds; i++) {
    if (cmd->cmd == LC_UNIXTHREAD) {
      uint32_t flavor = *((uint32_t *)cmd + 2);
      switch (flavor) {
        // TODO: support more arch
        case THREAD_STATE_ID: {
          THREAD_STATE *state = (THREAD_STATE *)((uint32_t *)cmd + 4);
          entryoff = getPC(state);
          return entryoff + slide;
        }
      }
    }
#ifdef LC_MAIN
    else if (cmd->cmd == LC_MAIN) {
      entryoff = ((struct entry_point_command *)cmd)->entryoff;
      j |= 1;
    }
#endif
    else if (cmd->cmd == MACH_SEG_CMD &&
             strcmp("__TEXT", ((struct MACH_SEG *)cmd)->segname) == 0) {
      segaddr = ((struct MACH_SEG *)cmd)->vmaddr;
      j |= 2;
    }
    cmd = (struct load_command *)((char *)cmd + cmd->cmdsize);
  }

  if (j != 3) {
    fprintf(stderr, "Could not find process entry point\n");
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  return segaddr + slide + entryoff;
}

void catchEntrypoint(int argc, char **argv) {
  int status = QBDIPRELOAD_NOT_HANDLED;

  unsetEntryBreakpoint();
  stopExceptionHandler(MAIN_EXCEPTION_HANDLER);

#if defined(QBDI_ARCH_X86_64) || defined(QBDI_ARCH_X86)
  // detect legacy UNIXTHREAD start (push 0)
  uint16_t *insn = (uint16_t *)QBDI_GPR_GET(&ENTRY_GPR, REG_PC);
  if (*insn == 0x6a) {
    argc = *(int *)QBDI_GPR_GET(&ENTRY_GPR, REG_SP);
    argv = (char **)((rword)QBDI_GPR_GET(&ENTRY_GPR, REG_SP) + sizeof(rword));
  }
#endif
  status = qbdipreload_on_main(argc, argv);

  if (DEFAULT_HANDLER && (status == QBDIPRELOAD_NOT_HANDLED)) {
    VMInstanceRef vm;
    qbdi_initVM(&vm, NULL, NULL, 0);
    qbdi_instrumentAllExecutableMaps(vm);

    // Skip system library (to avoid conflicts)
    size_t size = 0, i = 0;
    char **modules = qbdi_getModuleNames(&size);

    // Filter some modules to avoid conflicts
    qbdi_removeInstrumentedModuleFromAddr(vm, (rword)&catchEntrypoint);
    for (i = 0; i < size; i++) {
      if (strstr(modules[i], "libsystem")) {
        qbdi_removeInstrumentedModule(vm, modules[i]);
      }
    }
    for (i = 0; i < size; i++) {
      free(modules[i]);
    }
    free(modules);

    // Setup VM states
    qbdi_setGPRState(vm, &ENTRY_GPR);
    qbdi_setFPRState(vm, &ENTRY_FPR);

    rword start = QBDI_GPR_GET(qbdi_getGPRState(vm), REG_PC);
    rword stop = *((rword *)QBDI_GPR_GET(qbdi_getGPRState(vm), REG_SP));

    status = qbdipreload_on_run(vm, start, stop);
  }
  exit(status);
}

kern_return_t redirectExec(mach_port_t exception_port, mach_port_t thread,
                           mach_port_t task, exception_type_t exception,
                           mach_exception_data_t code,
                           mach_msg_type_number_t codeCnt) {
  kern_return_t kr;
  THREAD_STATE threadState;
  THREAD_STATE_FP floatState;
  mach_msg_type_number_t count;

  // Reading thread state
  count = THREAD_STATE_COUNT;
  kr = thread_get_state(thread, THREAD_STATE_ID, (thread_state_t)&threadState,
                        &count);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to get GPR thread state: %s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }
  count = THREAD_STATE_FP_COUNT;
  kr = thread_get_state(thread, THREAD_STATE_FP_ID, (thread_state_t)&floatState,
                        &count);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to get FPR thread state: %s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }

  // x86 breakpoint quirk
  fixSignalPC(&threadState);

  int status =
      qbdipreload_on_premain((void *)&threadState, (void *)&floatState);

  // Copying the initial thread state
  qbdipreload_threadCtxToGPRState(&threadState, &ENTRY_GPR);
  qbdipreload_floatCtxToFPRState(&floatState, &ENTRY_FPR);

  // if not handled, use default handler
  if (status == QBDIPRELOAD_NOT_HANDLED) {
    DEFAULT_HANDLER = true;

    // Allocating fake stack
    void *newStack = NULL;
    kr =
        mach_vm_map(task, (mach_vm_address_t *)&newStack, STACK_SIZE, 0,
                    VM_FLAGS_ANYWHERE, MEMORY_OBJECT_NULL, 0, false,
                    VM_PROT_READ | VM_PROT_WRITE, VM_PROT_ALL, VM_INHERIT_COPY);
    if (kr != KERN_SUCCESS) {
      fprintf(stderr, "Failed to allocate fake stack: %s\n",
              mach_error_string(kr));
      exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
    }

    // Swapping to fake stack
    prepareStack(newStack, STACK_SIZE, &threadState);
  }

  // Execution redirection
  setPC(&threadState, (rword)catchEntrypoint);
  count = THREAD_STATE_COUNT;
  kr = thread_set_state(thread, THREAD_STATE_ID, (thread_state_t)&threadState,
                        count);
  if (kr != KERN_SUCCESS) {
    fprintf(stderr, "Failed to set GPR thread state for redirection: %s\n",
            mach_error_string(kr));
    exit(QBDIPRELOAD_ERR_STARTUP_FAILED);
  }
  return KERN_SUCCESS;
}

void *qbdipreload_setup_exception_handler(uint32_t target, uint32_t mask,
                                          void *handler) {
  task_t target_ = (task_t)target;
  exception_mask_t mask_ = (exception_mask_t)mask;
  exception_handler_func handler_ = (exception_handler_func)handler;
  return setupExceptionHandler(target_, mask_, handler_);
}

int qbdipreload_hook_main(void *main) {
  setEntryBreakpoint((rword)main);
  MAIN_EXCEPTION_HANDLER = setupExceptionHandler(
      mach_task_self(), EXC_MASK_BREAKPOINT, redirectExec);
  return QBDIPRELOAD_NO_ERROR;
}

QBDI_FORCE_EXPORT void intercept_exit(int status) {
  if (!HAS_EXITED && HAS_PRELOAD) {
    HAS_EXITED = true;
    qbdipreload_on_exit(status);
  }
  exit(status);
}
DYLD_INTERPOSE(intercept_exit, exit)

QBDI_FORCE_EXPORT void intercept__exit(int status) {
  if (!HAS_EXITED && HAS_PRELOAD) {
    HAS_EXITED = true;
    qbdipreload_on_exit(status);
  }
  _exit(status);
}
DYLD_INTERPOSE(intercept__exit, _exit)

int qbdipreload_hook_init() {
  // do nothing if the library isn't preload
  if (getenv("DYLD_INSERT_LIBRARIES") == NULL)
    return QBDIPRELOAD_NO_ERROR;

  HAS_PRELOAD = true;
  rword entrypoint = getEntrypointAddress();

  int status = qbdipreload_on_start((void *)entrypoint);
  if (status == QBDIPRELOAD_NOT_HANDLED) {
    status = qbdipreload_hook_main((void *)entrypoint);
  }
  return status;
}
