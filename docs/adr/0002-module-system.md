# ADR 0002: Module System & Namespaces

## Status
Accepted

## Context
As Lala scales to support multi-file projects, we need a way to share code between compilation units. We evaluated whether to inject imported symbols directly into the global namespace (e.g., C/C++ style `#include`) or to maintain explicit namespaces (e.g., Python/JavaScript style).

## Decision
We will implement an explicit module system using a new language keyword `laao` (import) and `bahar` (export).
- **Import Grammar**: `laao ModulePath [as Alias]`
- **Export Grammar**: `bahar lala.kaam random()`
- **Namespace Handling**: Imported modules will NOT inject contents globally. They must be accessed explicitly (e.g., `math.random()`), with support for aliasing (`laao math as m`).
- **Encapsulation**: Only symbols explicitly marked with `bahar` are exposed to importers. Everything else is private to the file.

## Rationale
Explicit namespaces prevent symbol collisions and make the API clearer. By making imports part of the language syntax (`laao math`) instead of runtime calls (`lala.laao`), the compiler can statically analyze dependencies before execution.

## Consequences
- Requires updating the Lexer and Parser for `laao` and `bahar`.
- Standard library must be structured cleanly into top-level namespaces (e.g., `math`, `graphics`, `collections`).
