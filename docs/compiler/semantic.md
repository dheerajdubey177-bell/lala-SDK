# Semantic Analysis

## Purpose
Semantic Analysis validates the meaning of the AST. It ensures variables are declared before use, types match expected signatures, and functions are called with the correct arguments.

## Inputs
The generated `AST` stored in `CompilerContext.ast`.

## Outputs
- Symbol Tables (`CompilerContext.symbol_table`)
- Type Information
- Diagnostics (`CompilerContext.diagnostics`) for semantic violations.

## Ownership
Handled by `semantics/symbols.py` and `semantics/type_checker.py`.

## Invariants
- Passes must implement the `ASTVisitor` pattern.
- If an identifier cannot be resolved, an `L3xxx` error code (e.g., `L3001` for unknown variable) must be reported.
- Passes do not modify the AST. They append to the `CompilerContext`.
