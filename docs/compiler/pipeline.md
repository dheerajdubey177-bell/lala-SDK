# Lala Compiler Pipeline

The Lala compiler is organized into a series of distinct stages. This ensures decoupling between syntax parsing, semantic analysis, and backend code generation.

## Stages

1. **Lexer**: Converts raw source text into a stream of `Token`s.
2. **Parser**: Consumes tokens and builds the immutable Abstract Syntax Tree (`AST`).
3. **Semantic Pipeline**:
    * **Name Resolution**: Binds identifiers to `Symbol`s in hierarchical `Scope`s.
    * **Type Resolution**: Maps AST type annotations to canonical `Type` objects.
    * **Type Checker**: Enforces type invariants and reports semantic errors (e.g., LALA3xxx).
4. **Bound AST Generation**: Collapses the side-tables (Context) into a strictly-typed `BoundNode` tree.
5. **Control Flow Analysis (CFA)**: Analyzes the `Bound AST` for reachability and missing returns.
6. **High-Level Intermediate Representation (HIR)**: Lowers the `Bound AST` into a flat, block-based, SSA-ready instruction set. The compiler's canonical "source of truth".
7. **HIR Optimization**: (Optional in v1.0) Constant folding, dead code elimination.
8. **Machine Intermediate Representation (MIR)**: Lowers HIR into machine-oriented types (`i32`, `f64`).
9. **Backend**: Translates MIR to the final target (e.g., C++, LLVM, WASM).
