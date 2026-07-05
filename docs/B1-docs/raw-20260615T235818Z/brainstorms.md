# Brainstorms: config.toml Migration

## 2026-06-15: Initial analysis

Problem: `.freely/config.env` uses shell `source` format which is:
1. Only readable by shell — Python scripts must parse manually
2. No type safety — all values are strings
3. No structure — flat key=value, no nesting
4. `source config.env` executes arbitrary shell code — security risk

Proposed: Migrate to `.freely/config.toml` using Python's `tomllib` (3.11+).
