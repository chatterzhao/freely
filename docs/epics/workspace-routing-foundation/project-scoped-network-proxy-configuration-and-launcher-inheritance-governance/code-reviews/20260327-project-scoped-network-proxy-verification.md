# Verification: project-scoped-network-proxy-configuration-and-launcher-inheritance-governance

- issue_id: `I-20260327-0651`
- verification_scope: feature-lane verification before merge to `develop`
- verified_in_worktree: `feature/network-proxy-config-capability-restack`

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
2. `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
3. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
4. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-launcher-inheritance`
5. `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-oauth-inheritance`
6. `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
7. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
8. `./bin/governance-check`

## Result

- `freely init` now writes project-scoped proxy defaults into `.freely/config.env`, so later frontends only need to mutate one config truth source.
- `network-proxy-resolver.sh` now drives both codex launcher inheritance and watchdog OAuth/curl inheritance without falling back to hardcoded localhost defaults.
- OAuth sweep now sends the fuller CodexBar-style request contract, and no-arg `freely ai switch codex` refreshes saved auth inventory before choosing a usable slot.
- Governance remains clean aside from the repository's pre-existing legacy naming warnings.

## 2026-03-27 Missing Config Inherit Addendum

- A later replay through `test-freely-session-rotation` found an untested same-family edge:
  - when `HOME` points at an isolated directory with no `~/.freely/config.env`, the resolver's empty read path aborted under `set -e`
  - codex launch then exited before any `session id` / jsonl evidence was captured, incorrectly forcing `missing_resume_evidence`
- Verification update:
  - `network-proxy-resolver.sh` now treats missing project/global config as empty inherited values rather than a fatal read failure
  - `test-freely-network-proxy-resolver` now asserts missing-config inherit behavior
  - `test-freely-network-proxy-launcher-inheritance` now asserts ambient proxy env survives when both project and global config are absent
  - `test-freely-session-rotation` now completes past the former `context_usage_threshold` failure and passes end-to-end

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
