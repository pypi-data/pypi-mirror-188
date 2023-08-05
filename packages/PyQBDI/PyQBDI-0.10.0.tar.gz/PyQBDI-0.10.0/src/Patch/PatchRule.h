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
#ifndef PATCHRULE_H
#define PATCHRULE_H

#include <memory>
#include <vector>

#include "QBDI/State.h"
#include "Patch/Patch.h"

namespace llvm {
class MCInst;
} // namespace llvm

namespace QBDI {
class LLVMCPU;
class PatchGenerator;
class PatchCondition;
class RelocatableInst;

/*! A patch rule written in PatchDSL.
 */
class PatchRule {
  std::unique_ptr<PatchCondition> condition;
  std::vector<std::unique_ptr<PatchGenerator>> generators;

public:
  /*! Allocate a new patch rule with a condition and a list of generators.
   *
   * @param[in] condition   A PatchCondition which determine wheter or not this
   *                        PatchRule applies.
   * @param[in] generators  A vector of PatchGenerator which will produce the
   *                        patch instructions.
   */
  PatchRule(std::unique_ptr<PatchCondition> &&condition,
            std::vector<std::unique_ptr<PatchGenerator>> &&generators);

  PatchRule(PatchRule &&);

  ~PatchRule();

  /*! Determine wheter this rule applies by evaluating this rule condition on
   * the current context.
   *
   * @param[in] patch     The Patch to check
   * @param[in] llvmcpu   LLVMCPU object
   *
   * @return True if this patch condition evaluate to true on this context.
   */
  bool canBeApplied(const Patch &patch, const LLVMCPU &llvmcpu) const;

  /*! Generate this rule output patch by evaluating its generators on the
   * current context. Also handles the temporary register management for this
   * patch.
   *
   * @param[in] patch     The Patch where to apply the rule
   * @param[in] llvmcpu   LLVMCPU object
   */
  void apply(Patch &patch, const LLVMCPU &llvmcpu) const;
};

} // namespace QBDI

#endif // PATCHRULE_H
