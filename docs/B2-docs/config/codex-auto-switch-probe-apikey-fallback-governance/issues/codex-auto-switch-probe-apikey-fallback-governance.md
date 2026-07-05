# Issue: codex-auto-switch-probe-apikey-fallback-governance

- issue_id: `I-20260407-0023-A`
- title: Codex auto switch probe apikey fallback governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-auto-switch-probe-apikey-fallback-governance`
- issue-name: `codex-auto-switch-probe-apikey-fallback-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260407/candidates.md#c-20260407-0023-a`
- source_brainstorm: `docs/B1-docs/raw-20260407/brainstorms.md`
- execution_base: `feature/codex-auto-switch-probe-apikey-fallback-20260406-2138`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-auto-switch-probe-apikey-fallback-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/codex-apikey-slot-bundle-and-provider-aware-probe-governance.md`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Codex account/apikey bundle truth is already owned, but dogfooding exposed one remaining fallback gap after that owner closed: if the OAuth sweep returns `all_unavailable:*`, Freely still stops before exec-probing saved `apikey-*` slots. That violates the narrower contract that apikey slots use `codex exec` truth and makes no-arg `switch codex` disagree with explicit apikey switching.

## Scope

1. Keep `ai switch codex` auto mode probing saved `apikey-*` slots when OAuth inventory says saved account slots are all unavailable.
2. Keep watchdog recovery on the same fallback contract instead of returning early on the shared `all_unavailable:*` result.
3. Lock the behavior with a focused regression that proves the unavailable account slot is not falsely selected while the saved apikey slot is still probed and chosen.
4. Replay the narrow Codex switch regressions and governance gates needed for promotion.

## Non-Goals

1. Do not reopen the completed Codex auth bundle owner for new IBM scope.
2. Do not widen into unsaved current-live apikey bootstrap, interactive login UX, or reconnect fast-fail classification.
3. Do not investigate the external TLS/certificate failures observed on live account `codex exec`; that remains environment evidence unless Freely needs a new diagnosis surface.

## Acceptance

1. `freely ai switch codex` auto mode treats `all_unavailable:*` as a reason to continue exec-only probing when saved `apikey-*` slots exist.
2. Watchdog recovery follows the same rule and does not stop early if the only usable candidate is a saved apikey slot.
3. Focused regressions, governance checks, and issue-bound verification artifacts pass in the dedicated feature worktree.

## Verification

- `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-verification.md`
- `docs/epics/workspace-routing-foundation/codex-auto-switch-probe-apikey-fallback-governance/code-reviews/20260407-codex-auto-switch-probe-apikey-fallback-canonical-closeout-verification.md`

## Retirement Handoff

- `feature/codex-auto-switch-probe-apikey-fallback-20260406-2138` and `test-pre-merge-codex-auto-switch-probe-apikey-fallback-20260407-0029` are retire-only after the canonical closeout writeback lands.
- Residual environment-level account TLS/certificate failures are explicitly out of scope for this completed owner.

## Next

- Completed on canonical `develop` through `test-pre-merge-codex-auto-switch-probe-apikey-fallback-20260407-0029` and guarded merge `1b33131`.
- Post-merge followthrough passed on canonical `develop`; reopen only if saved-apikey fallback regresses after an `all_unavailable:*` account sweep.
