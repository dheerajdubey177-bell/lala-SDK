# Diagnostics

## Purpose
The Diagnostics engine handles reporting of lexical, syntax, semantic, and structural errors to the user in a consistent format.

## Formats
Diagnostics must present the error code, a clear message, line/column identifiers, and source code highlights.

Example:
```
L3001
Variable 'X' is not declared.
Line 4, Column 10
    lala.agar X > 10:
              ^
```

## Inputs
Requests from anywhere in the compiler pipeline invoking `diagnostics.error()`.

## Outputs
Error states inside `CompilerContext.diagnostics.errors`, optionally printed to `stdout`.

## Ownership
`diagnostics/reporter.py`.

## Invariants
- Uses an Error Code convention (`L1xxx` for syntax/parsing, `L2xxx` for structure, `L3xxx` for semantics).
- If errors are present, the compilation must abort before backend code generation.
