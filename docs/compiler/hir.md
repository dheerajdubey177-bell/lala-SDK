# High-Level IR (HIR)

## Purpose
The HIR is an intermediate representation that sits between the AST and LIR. It is designed to capture the structural logic of Lala (e.g., control flow structures like `if` and `while`) without tying it to specific C++ syntax. 

## Inputs
AST stored in `CompilerContext.ast`.

## Outputs
Control flow components translated into linear blocks.

## Invariants
- Currently merged closely with LIR in our `IRBuilderPass`, but architecturally represents the structural translation boundary.
- Designed to remain platform-independent.
