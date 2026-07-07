# High-Level Intermediate Representation (HIR)

HIR is the canonical compiler IR. It is designed to be flat, typed, validated, and backend-independent.

## Core Concepts

* **Flat Instructions**: Unlike the deeply nested AST, HIR consists of a flat list of explicit instructions.
* **Basic Blocks**: Instructions are grouped into Basic Blocks. Every block ends with exactly one terminator (Jump, Branch, Return).
* **Value IDs**: Variables and intermediate expressions are represented by stable `ValueID`s (e.g., `v17`).
* **Explicit Types**: Every HIR instruction knows its exact type, eliminating the need for the backend to perform type inference.

## Instruction Set

* `Load` / `Store` / `Move`
* `Call` (User-defined functions)
* `RuntimeCall` (e.g., `GRAPHICS_CIRCLE`)
* `IntrinsicCall` (e.g., `INTRINSIC_PRINT`)
* `Compare`
* `Branch` / `Jump` / `Return`
* `Allocate`
* `Constant`

## Validation

All HIR must pass the Validation pass, ensuring:
1. Terminator integrity.
2. Valid jump targets.
3. Defined `ValueID` usage.
4. Valid intrinsic and runtime IDs.
