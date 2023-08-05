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
#ifndef QBDIPRELOAD_ARM_H
#define QBDIPRELOAD_ARM_H

#include <dlfcn.h>
#include <signal.h>
#include <sys/wait.h>
#include <unistd.h>

#include <QBDI.h>

#define SIGBRK SIGTRAP

static inline void *correctAddress(void *address, long *bytecode, long *mask) {
  if ((((rword)address) & 1) == 0) {
    *bytecode = 0xE7F001F0;
    *mask = 0xFFFFFFFF;
    return address;
  } else {
    // address is Thumb
    *bytecode = 0xDE01;
    *mask = 0xFFFF;
    return (void *)(((rword)address) & ~1);
  }
}

void qbdipreload_threadCtxToGPRState(const void *gprCtx, GPRState *gprState);
void qbdipreload_floatCtxToFPRState(const void *fprCtx, FPRState *fprState);

static inline rword getReturnAddress(GPRState *gprState) {
  return QBDI_GPR_GET(gprState, REG_LR);
}

static inline void fix_ucontext_t(ucontext_t *uap) {
  // nothing to do
}

void prepareStack(void *newStack, size_t sizeStack, ucontext_t *uap);

static inline void setPC(ucontext_t *uap, rword address) {
  uap->uc_mcontext.arm_pc = (address & (~1));
  if ((address & 1) == 1) {
    uap->uc_mcontext.arm_cpsr |= (1 << 5);
  } else {
    uap->uc_mcontext.arm_cpsr &= ~(1 << 5);
  }
}

void removeConflictModule(VMInstanceRef vm, qbdi_MemoryMap *modules,
                          size_t size);

#endif // QBDIPRELOAD_ARM_H
