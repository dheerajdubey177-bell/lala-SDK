# ADR 0001: Compiler Pipeline Architecture v0.4

## Status
Accepted

## Context
As the Lala compiler grows from a direct transpiler to a professional language implementation, it requires a robust, scalable architecture. The initial v0.3 architecture (Lexer -> Parser -> Direct C++ Translation) became difficult to maintain, reason about, and optimize. Semantic information was coupled with AST generation, and control flow had no centralized representation.

## Decision
We decided to adopt a multi-pass pipeline architecture consisting of the following stages:

1. **Frontend**: Lexer and Parser outputting a typed Abstract Syntax Tree (AST).
2. **Semantics**: Non-mutating semantic passes (Symbol Resolution, Type Checking) that traverse the AST and store metadata in a shared `CompilerContext`.
3. **High-Level IR (HIR)**: Preserves language semantics (like `if`, `while`, `for`) using basic blocks. 
4. **Low-Level IR (LIR)**: Simplifies operations into instructions like `LOAD_CONST`, `BINARY_OP`, `JUMP`, and `BRANCH`.
5. **Optimizer**: Modular, independent optimization passes such as Constant Folding and Dead Code Elimination.
6. **Backend**: Platform-specific backends that reconstruct structured control flow (like C++ `while` loops instead of raw `goto`) from LIR to maintain readable and debuggable output.

## Consequences
- **Positive**: Adding new language features is easier due to separation of concerns. New backends (e.g., JavaScript, WebAssembly, LLVM) can be added without modifying the frontend. The language is now capable of performing real optimization.
- **Positive**: Error messages are now robust, contextualized, and centralized using error codes (e.g., `L1004`).
- **Negative**: The compiler is more complex, requiring more infrastructure (PassManagers, Contexts) than before.
