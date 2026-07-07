# Compiler Pipeline

## Purpose
The Pipeline dictates how Lala source code transitions into compiled executables. It organizes discrete, decoupled passes into a unified compilation process.

## Architecture
The compiler follows a `PassManager` design pattern, heavily relying on a central `CompilerContext`.

```text
Source -> Lexer -> Parser -> AST -> Semantic Passes -> HIR -> Optimizer -> LIR -> Backend -> C++
```

## Ownership
The `lala_compiler.py` driver owns the `PassManager` configuration. Individual modules do NOT invoke each other; instead, they operate exclusively on the `CompilerContext`.

## Invariants
- Each pass must implement the `CompilerPass` interface.
- Passes must NOT destructively modify the AST. They should append data to the Context (e.g., Symbol Tables, IR graphs).
- If `DiagnosticsReporter` registers an error (e.g., `has_errors()`), the pipeline halts before reaching the Backend to prevent invalid C++ generation.
