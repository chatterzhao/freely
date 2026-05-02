# PRD: supply-chain-baseline-and-install-intake-audit-governance

## Goal

Turn a real leftover security-baseline topic into machine-enforced truth: lockfile presence, direct dependency intake, explicit lifecycle allowlist enforcement, and workflow pinning should no longer depend on reviewer memory.

## Product Shape

1. A reusable audit script under `docs/system/workspace/scripts/quality/`
2. A stable wrapper under `bin/`
3. `freely doctor` integration
4. Focused regressions proving the baseline

## Non-Goals

1. Package age policy
2. Provenance / trusted publishing verification
3. Transitive vulnerability intelligence
4. Generalized runtime secret scanning
