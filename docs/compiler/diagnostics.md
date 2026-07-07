# Diagnostics

Lala implements a robust diagnostic reporting system. Errors and warnings are categorized by numeric blocks.

## Severities
* **Error**: Compilation cannot proceed to code generation.
* **Warning**: Compilation succeeds, but the compiler flags potentially dangerous or inefficient code.
* **Info**: Helpful suggestions (not fully utilized in v1.0).

## Error Categories

### Lexical & Parsing (LALA1xxx)
* `LALA1001`: Invalid syntax.

### Name Resolution (LALA2xxx)
* `LALA2001`: Undefined variable.
* `LALA2002`: Duplicate declaration.

### Type System (LALA3xxx)
* `LALA3001`: Type mismatch.
* `LALA3002`: Invalid operation.

### Runtime Binding (LALA4xxx)
* `LALA4001`: Unknown module.
* `LALA4002`: Unknown function.

### Control Flow & Warnings (LALA5xxx)
* `LALA5001`: Unused variable.
* `LALA5002`: Unused import.
* `LALA5003`: Unreachable code.
* `LALA5004`: Missing return.
