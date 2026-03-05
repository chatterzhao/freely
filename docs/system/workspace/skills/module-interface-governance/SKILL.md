---
name: module-interface-governance
description: Apply plug-in module and interface version governance for parallel evolution. Use when AI introduces replacements, versioned contracts, or migration paths across modules.
---

# skill:module-interface-governance

## Workflow
1. Define module boundary and current contract version.
2. If third-party API is involved, treat provider contract as external source of truth and design local adapter around it.
3. For breaking changes, create versioned contract and migration path.
4. Keep rollback path to stable implementation.
5. Validate contract compatibility with tests (including third-party API integration semantics when applicable).
6. Record active version and switch strategy.

## Done
- Module evolution is versioned, testable, reversible, and aligned to third-party API contracts when used.
