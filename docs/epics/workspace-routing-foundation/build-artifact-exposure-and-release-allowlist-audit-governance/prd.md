# PRD: build-artifact-exposure-and-release-allowlist-audit-governance

## Objective

Turn the already-agreed security principle of “automation and enforced workflow over operator memory” into a first executable capability slice by auditing build outputs for forbidden artifacts and enforcing an explicit release allowlist.

## Product Slice

1. Reusable audit script for build output directories.
2. Repo-scoped allowlist consumed by the audit.
3. `freely doctor` integration.
4. Build-path integration for the current repo.
5. Explicit production sourcemap posture.

## Out of Scope

1. Full supply-chain policy
2. Full runtime secret scanning
3. External vendor scanner integrations
4. Broader execution-boundary review flows already owned elsewhere
