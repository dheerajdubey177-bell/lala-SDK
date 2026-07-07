# ADR 0004: Cache Format & Incremental Compilation

## Status
Accepted

## Context
Recompiling the entire project on every change is slow. We need an incremental compilation strategy.

## Decision
We will cache intermediate compiler stages (AST, HIR, LIR) in a `.lala_cache/` directory. 
The cache invalidation key will be a hash composed of:
1. Source file contents (SHA256).
2. Compiler version.
3. Language version.
4. Optimization profile.
5. Target backend.

## Rationale
Caching intermediate stages (rather than just skipping files) allows the backend to quickly regenerate executables if only the backend configuration changes. Including environment and compiler versions in the cache key ensures that stale artifacts are correctly invalidated when the SDK upgrades.

## Consequences
- Requires serializing/deserializing intermediate representations (AST, IR).
- Dramatically faster build times for large projects when only leaf nodes in the dependency DAG are modified.
