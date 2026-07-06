# Issue: runtime-human-readable-time-display-governance

- issue_id: `I-20260402-0308-A`
- title: Runtime human-readable time display governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-human-readable-time-display-governance`
- issue-name: `runtime-human-readable-time-display-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260402T191200Z/candidates.md#c-20260402-0308-a`
- source_brainstorm: `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/runtime/runtime-human-readable-time-display-governance/raw-20260402-0308/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-human-readable-time-display-governance.md`
- verification_artifact_dir: docs/B2-docs/runtime/runtime-human-readable-time-display-governance/raw-20260402-0308/code-reviews
- depends_on:
  - `docs/B2-docs/human/tui/raw-20260308-1244issues/frontend-probe-v0.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already proved the correct boundary: keep naming truth in UTC, keep stored event/reset truth in epoch or RFC3339, and format human-readable timestamps in the host system timezone with a timezone label. The problem is that this rule was only partially materialized. `frontend-probe-v0` absorbed the Probe display slice, and `ai-cli` plus watchdog cooldown strings already changed, but core runtime status surfaces still exposed raw ISO/UTC truth to humans and the runtime-side slice had no owner.

This owner closes that gap without reopening the frontend owner or rewriting machine truth.

## Continuation Note

After the first merge, a follow-up review found a narrow tail of runtime status fields that still printed raw UTC/RFC3339 values in `baseline-status` and `live-status`. This issue continues to own that closeout because the remaining work stays inside the same boundary: localize human-readable runtime display only, preserve stored truth and naming truth unchanged.

After the status-tail closeout landed, a runtime follow-up found one more consistency gap inside the same owner boundary: runtime code still minted "current time" strings through multiple ad hoc call sites. This continuation keeps the scope narrow by consolidating those runtime-side call sites onto one local-display helper and one UTC machine-truth helper, without changing stored truth, filenames, or timezone policy.

## Scope

1. Materialize a dedicated runtime/workspace owner for human-readable time display.
2. Render host-local time with timezone label for user-facing `freely` status outputs:
   - `last_state_updated_at`
   - `activation_consent_recorded_at`
   - intake snapshot `created_at`
   - `develop_push_followthrough_defer_updated_at`
3. Preserve raw stored truth in config/state/intake payloads.
4. Keep `freely ai status` dual-surfaced:
   - raw truth in `refreshed_at`
   - human display in `refreshed_at_human`
5. Treat watchdog cooldown human text the same way: local display, unchanged machine truth.

## Non-Goals

1. Do not rewrite `.bak` or governance naming timestamps away from UTC.
2. Do not rewrite stored `created_at`, `occurredAt`, `reset_at`, or other RFC3339/epoch truth.
3. Do not reopen `frontend-probe-v0`; that owner only keeps the Probe display slice.
4. Do not add user-selectable timezone preferences in this slice.
5. Do not claim repo-wide shared formatter parity across future TUI/GUI surfaces.

## Acceptance

1. `freely live-status` shows the in-scope human-facing timestamps in host-local time with timezone label.
2. `freely baseline-status` shows `activation_consent_recorded_at` in host-local time with timezone label.
3. `freely develop-push status` shows `develop_push_followthrough_defer_updated_at` in host-local time with timezone label.
4. Intake status output shows human-facing `created_at` in host-local time with timezone label without rewriting intake metadata truth on disk.
5. `freely ai status` preserves raw refresh truth and also exposes `refreshed_at_human`.
6. Watchdog cooldown human text remains host-local with timezone label.
7. Tests prove the display layer changed while raw truth remains ISO/epoch/UTC-backed.
8. Remaining runtime status tail fields also follow the same rule:
   - baseline snapshot rate-limit reset timestamps
   - slot switch timestamp
   - delegated continuation consumed timestamps
   - restart storm signal/escalation timestamps

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260402T191200Z/candidates.md`
- `docs/B1-docs/raw-20260402T191200Z/brainstorms.md`
- `docs/B1-docs/raw-20260402T191200Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/issues/runtime-human-readable-time-display-governance.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/brainstorms/b-runtime-human-readable-time-display-governance.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/prd.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/pre-tests.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/tasks.md`
- `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/code-reviews/20260402-runtime-human-readable-time-display-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-human-readable-time-display-governance.md`
- `docs/B2-docs/human/tui/raw-20260308-1244code-reviews/20260401-frontend-probe-v0-terminal-attach-validation.md`
- `docs/progress/frontend-probe-dogfooding-loop/p-frontend-probe-v0.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
- `docs/system/workspace/scripts/tests/test-freely-develop-push-status-time-display`
- `docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `docs/system/workspace/scripts/tests/test-freely-current-timestamp-local-display-format`
- `docs/system/workspace/scripts/tests/test-freely-human-display-time-format-uses-shared-helper`
- `docs/system/workspace/scripts/tests/test-freely-machine-time-format-uses-shared-helper`
- `docs/system/workspace/scripts/tests/test-freely-manager-startup-continuity-stub-materialization`
- `docs/system/workspace/scripts/tests/test-freely-stop-materializes-missing-manager-continuity`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
- `bash docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-execution-boundary-audit`
- `bash docs/system/workspace/scripts/tests/test-freely-develop-push-status-time-display`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `./bin/governance-check`

## Next

- Keep this owner narrow to human-readable time display on runtime/workspace surfaces.
- If Freely later needs user-selectable timezone preferences or a shared formatter across future TUI/GUI/runtime surfaces, materialize a new follow-on owner instead of stretching this one.
