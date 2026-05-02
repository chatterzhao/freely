# Verification: supply-chain-baseline-and-install-intake-audit-governance

- issue_id: `I-20260401-0115-A`
- reviewer: `codex`
- verdict: `pass_for_verification`

## Commands

- `bash docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
- `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
- `./bin/governance-check`

## Results

1. The canonical audit now fails when a repo with root `package.json` lacks a recognized root lockfile.
2. The audit fails on disallowed direct dependency intake via `git+`, `github:`, `http(s):`, `file:`, or `link:` specifiers.
3. The audit fails on install-time lifecycle scripts `preinstall`, `install`, `postinstall`, and `prepare` unless the script name is explicitly allowlisted.
4. The audit fails on mutable external GitHub Action refs and accepts full-SHA pins.
5. `freely doctor` replays the same audit, so the baseline no longer depends on manual reviewer memory.
6. `freely init` now seeds the repo-scoped lifecycle allowlist file, so new repos do not depend on operator memory to satisfy the baseline contract.
7. Adjacent `doctor` and intake regressions still pass after the new gate, so the slice does not break existing execution-boundary or chat/bootstrap flows.
8. The slice remains intentionally narrow and does not claim minimum package age, provenance, or transitive vulnerability intelligence.
9. The implementation is merged on `develop` at commit `1d082fc`.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
