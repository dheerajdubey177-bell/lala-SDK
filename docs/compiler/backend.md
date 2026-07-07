# Backend

## Purpose
The Backend consumes the optimized LIR and translates it into executable output. The current primary backend targets standard C++.

## Inputs
The LIR CFG stored in `CompilerContext.lir`.

## Outputs
Source strings (e.g., C++ files) or direct binary compilation orchestration.

## Ownership
`backend/cpp_backend.py`.

## Invariants
- The Backend MUST NOT read from the AST directly. All translation must stem from the IR.
- The Backend must perform structured CFG reconstruction. For example, it must re-form `while` loops and `if/else` statements instead of emitting raw `goto` commands, ensuring the generated source is readable and debuggable.
