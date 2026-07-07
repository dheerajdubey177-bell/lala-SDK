# ADR 0003: Build Manager & CLI

## Status
Accepted

## Context
Previously, compilation was invoked via `python bin/lala_compiler.py <file>`. As we introduce multi-file projects, a monolithic script is insufficient to handle dependency resolution and incremental builds. We also need a unified entry point for all ecosystem tools.

## Decision
We will introduce a `BuildManager` class and a unified `lala` CLI driver.
The `BuildManager` explicitly handles:
1. Project Discovery & Manifest Validation (`lala.json`).
2. Dependency Graph Construction & Cycle Detection.
3. Compilation Scheduling (DAG traversal).
4. Cache Resolution.
5. Invoking the Backend and Linking.

The unified CLI will reserve commands: `init`, `build`, `run`, `check`, `clean`, `test`, `fmt`, `lint`, `doc`, `graph`, `version`.

## Rationale
Separating the build logic from the compiler pipeline ensures that `PassManager` remains entirely focused on compiling a single file unit, while `BuildManager` handles the ecosystem context. A unified CLI prevents command bloat and standardizes developer workflow.

## Consequences
- Multi-file projects will compile safely and predictably based on DAG ordering.
- Cycle detection will prevent infinite loops in imports.
