# Optimization Manifest

This document describes the optimization passes available in the compiler pipeline. All optimization passes operate on the **High-Level Intermediate Representation (HIR)** and adhere to the following invariants:
1. They take a `Program` and return a new `Program` (utilizing structural sharing for performance).
2. They do not mutate existing `BasicBlock` or `Instruction` objects in place.
3. They must produce a valid HIR that passes the `HIRValidator`.
4. They report metrics on what they accomplished (e.g. `{"folded": 10}`).

---

## 1. ConstantFoldingPass

* **Purpose**: Evaluates mathematical and logical operations where all operands are compile-time constants.
* **Preconditions**: Valid HIR.
* **Postconditions**: Any `BinaryOp` or `UnaryOp` whose inputs are `Constant`s are replaced with a single `Constant` instruction.
* **Preserves**: Control flow graph, observable side-effects.

---

## 2. ConstantBranchFoldingPass

* **Purpose**: Evaluates conditional `Branch` terminators where the condition is a known `Constant` boolean.
* **Preconditions**: Valid HIR.
* **Postconditions**: Any `Branch` with a constant condition is replaced with an unconditional `Jump` to the guaranteed target block.
* **Preserves**: Data flow, observable side-effects.

---

## 3. DeadCodeEliminationPass

* **Purpose**: Removes instructions that perform no meaningful work and have no side effects.
* **Preconditions**: Valid HIR.
* **Postconditions**: Any instruction where `is_pure == True` AND whose `target` is never referenced by another instruction in the function is removed.
* **Preserves**: Side effects (instructions like `Allocate`, `Store`, `IntrinsicCall`, and `RuntimeCall` are never removed by this simple pass).

---

## 4. UnreachableBlockRemovalPass

* **Purpose**: Removes entire `BasicBlock`s that cannot be reached from the function's entry block.
* **Preconditions**: Valid HIR.
* **Postconditions**: Any block with no predecessors (except the entry block) is deleted from the `Program`.
* **Preserves**: Reachable code and data flow.

---

## 5. CFGSimplificationPass

* **Purpose**: Normalizes the control-flow graph by removing redundant jump sequences.
* **Preconditions**: Valid HIR.
* **Postconditions**: Resolves jump threading (`A -> B -> C` where `B` is empty becomes `A -> C`). Simplifies redundant branches (`branch cond ? B : B` becomes `jump B`).
* **Preserves**: Reachable code and data flow. Does not explicitly split critical edges.
