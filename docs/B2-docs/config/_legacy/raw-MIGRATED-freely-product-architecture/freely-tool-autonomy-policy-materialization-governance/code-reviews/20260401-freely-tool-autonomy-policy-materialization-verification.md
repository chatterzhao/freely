# Verification: freely-tool-autonomy-policy-materialization-governance

- issue_id: `I-20260401-1303-A-2`
- reviewer: `codex`
- verdict: `pass_for_verification`

## Commands

- `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `./bin/governance-check`

## Results

1. `freely init` now materializes project-scoped Codex posture through a mode-aware `.codex/config.toml` path, and `auto` writes `approval_policy = "never"` without turning `sandbox_mode = "workspace-write"` or `network_access = false` into Freely hard blockers.
2. focused `init` regressions confirm the blocking activation-consent contract and project-local Codex/Claude configuration paths still behave correctly after the materialization change.
3. `tools.md` now distinguishes project-local Codex baseline materialization from launch-time auto posture injection, and it describes Claude Code surfaces as launch-time materialization rather than fake project-local config owners.
4. the remaining worker-reactivation/local-reentry runtime residuals are no longer carried by this owner; they were split to `I-20260401-1831-A`, so this verification stays bounded to tool policy materialization.

## Evidence

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
