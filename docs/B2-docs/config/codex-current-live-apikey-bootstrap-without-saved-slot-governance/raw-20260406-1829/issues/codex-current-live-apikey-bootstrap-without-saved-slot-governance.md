# Issue: codex-current-live-apikey-bootstrap-without-saved-slot-governance

- issue_id: `I-20260406-1829-A`
- title: Codex current-live apikey bootstrap without saved-slot inventory governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-current-live-apikey-bootstrap-without-saved-slot-governance`
- issue-name: `codex-current-live-apikey-bootstrap-without-saved-slot-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260406T110500Z/candidates.md#c-20260406-1829-a`
- source_brainstorm: `docs/B1-docs/raw-20260406T110500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- verification_artifact_dir: docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829/code-reviews

## Why

Freely still needs a bounded owner for the case where current live Codex auth is a usable API key but saved-slot inventory is empty. This execution lane absorbs that remaining truth from the old residual tree without reopening reconnect fast-fail or interactive login UX.

## Scope

1. Accept a usable current live Codex API-key auth in `ai switch codex` without requiring saved-slot inventory.
2. Accept the same bounded current-live identity for manager bootstrap/readiness.
3. Keep live auth truth separate from saved-slot truth; do not synthesize a fake slot.
4. Lock the path with issue-bound regressions.

## Acceptance

1. `ai switch codex` surfaces a bounded success path for usable current live apikey auth with `slot=null`.
2. manager bootstrap can wake from a usable current-live apikey path and records `current-live` identity when inventory is empty.
3. issue-bound regressions and governance gates pass.

## Verification

- `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-verification.md`
- `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-implementation-decision.md`
- `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/raw-20260406-1829code-reviews/20260406-codex-current-live-apikey-bootstrap-without-saved-slot-canonical-closeout-verification.md`

## Retirement Handoff

- `feature/fix-codex-apikey-availability-lock` is now `retire-only`.
- This owner absorbs the old residual watchdog/bootstrap slice:
  - `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `docs/system/workspace/scripts/tests/test-ai-cli-switch-current-live-apikey-without-saved-slot`
  - `docs/system/workspace/scripts/tests/test-freely-ensure-manager-current-live-apikey-without-saved-slot`
- The old residual `docs/system/workspace/scripts/runtime/ai-cli` patch is superseded by the stronger current-live switch path already present in this lane; do not transplant it verbatim during cleanup.
- The old residual `docs/system/workspace/scripts/runtime/freely` plus `docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter` belong to `I-20260406-0901-A`, not to this owner.

## Next

- Completed on canonical `develop` through `test-pre-merge-codex-current-live-apikey-bootstrap-20260406-2000` and guarded merge `4b6e0a9`.
- Post-merge followthrough passed on canonical `develop`; the retired residual tree no longer carries canonical truth for this boundary.
