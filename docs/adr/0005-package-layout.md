# ADR 0005: Package Layout & Namespaces

## Status
Accepted

## Context
As the Lala ecosystem grows, we need standard conventions for how projects are structured and how external packages are identified to avoid future fragmentation.

## Decision
All Lala projects must follow a standardized structure, scaffolded by `lala init`:
```text
project/
  src/
  tests/
  packages/
  build/
  .lala_cache/
  lala.json
```

The `lala.json` manifest will strictly define `language`, `compiler`, and `sdk` versions independently to support future uncoupling.

For packages, we will adopt a publisher-prefixed namespace convention: `<publisher>/<package>` (e.g., `official/math`, `community/sqlite`).

## Rationale
Consistency early prevents fragmentation. Reserving publisher prefixes solves namespace collisions before a remote registry even exists.

## Consequences
- Users are guided into a uniform project structure, making open-source collaboration easier.
