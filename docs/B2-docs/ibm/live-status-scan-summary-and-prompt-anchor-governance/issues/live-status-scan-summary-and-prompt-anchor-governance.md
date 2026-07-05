# Issue: live-status-scan-summary-and-prompt-anchor-governance

- issue_id: `I-20260421-1530-A`
- title: `Live-status scan summary and prompt anchor governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `live-status-scan-summary-and-prompt-anchor-governance`
- issue-name: `live-status-scan-summary-and-prompt-anchor-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260421/candidates.md#C-20260421-1530-A`
- source_brainstorm: `docs/B1-docs/raw-20260421/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/pre-tests.md`
- tasks_path: `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-live-status-scan-summary-and-prompt-anchor-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md`
  - `docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/issues/application-native-runtime-observation-contract-and-observability-planes.md`
  - `docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- created_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already had two valid but separate truths:

1. `task-source-scan` is the bounded patrol inventory contract
2. `live-status` is the current-state observation plane

What was still missing was a narrow implementation owner that applies the separation in runtime code without reducing capability:

1. prompt lookup on current-state hot paths must prefer explicit session anchors over prompt-history guessing
2. `live-status` should surface advisory patrol inventory from the existing scan JSON instead of pretending prompt history describes unresolved work
3. the change must preserve daemon-start behavior, worker-launch visibility, deep refs, and existing self-heal/read-path contracts

## Scope

1. Keep explicit prompt anchors authoritative for `live-status`, manager handoff, and continuity-gap prompt references.
2. Add an advisory `scan_summary` surface to `live-status` by reading the existing `manager-task-source-scan-latest.json`.
3. Preserve existing `current-state plane` behavior, deep refs, worker-lane visibility, the bounded startup continuity-selection seam, and the startup lifecycle keepalive needed so watchdog recovery does not kill a supervisor while prompt build is still legitimately in flight.
4. Carry the design/materialization chain needed for guarded merge through `test-pre-merge-*` and develop replay.

## Non-Goals

1. Do not redesign the entire status family.
2. Do not build a heavyweight prompt lifecycle index.
3. Do not widen scan into canonical completion truth.
4. Do not remove existing prompt/deep-ref/status fields in this owner.

## Acceptance

1. `live-status` prefers explicit prompt anchors over prompt-history guessing on the relevant prompt surfaces.
2. `live-status` exposes advisory scan summary fields sourced from the existing patrol inventory JSON.
3. Existing current-state, daemon, patrol, worker-launch, and verification-contract regressions still pass.
4. The guarded merge path succeeds through `feature/* -> test-pre-merge-* -> develop`.
5. Develop-side validation still shows bounded daemon-start behavior and no capability regression in status or patrol surfaces.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
- `bash -n docs/system/workspace/scripts/runtime/freely`
- `./bin/governance-check`

## Completion

- `docs/B1-docs/raw-20260421/brainstorms.md`
- `docs/B1-docs/raw-20260421/candidates.md`
- `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/issues/live-status-scan-summary-and-prompt-anchor-governance.md`
- `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/pre-tests.md`
- `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-live-status-scan-summary-and-prompt-anchor-governance.md`
- `docs/B2-docs/ibm/live-status-scan-summary-and-prompt-anchor-governance/code-reviews/20260421-live-status-scan-summary-and-prompt-anchor-verification.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-live-status-includes-scan-summary`
- `docs/system/workspace/scripts/tests/test-freely-live-status-prefers-session-state-prompt-anchor`

## Next

- Finish the canonical `develop` replay for this owner and prove the bounded startup continuity-selection fix still leads into real scan-driven work selection rather than only prompt-build success.
- Keep any future typed scan-item schema, broader status-family field renames, and daemon-start autonomous completion followthrough in later bounded owners if this slice cannot absorb them without widening.
