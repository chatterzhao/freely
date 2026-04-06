# PRD: cli-help-and-dry-run-contract-followthrough-governance

## Problem

Freely is CLI-first, but a canonical replay still shows first-hop contract defects:

- some `--help` invocations behave like failures or even enter side-effectful paths
- top-level `freely --help` still looks like an unknown-command error
- `ai switch codex --dry-run --format json` is not a bounded machine-readable dry-run surface

These defects are narrow, reproducible, and directly visible to operators and automation.

## Product Decision

Treat help and dry-run semantics as part of the command contract. Repair only the audited surfaces and pin them with focused regressions.

## Requirements

1. Audited help surfaces must be explicit and side-effect free.
2. Usage-only invocations must return success where no action is requested.
3. Sourced helpers must keep their direct-exec protections while still offering a sourced help path.
4. `ai switch codex --dry-run --format json` must emit one stable JSON result without performing the full mutable switch flow.
