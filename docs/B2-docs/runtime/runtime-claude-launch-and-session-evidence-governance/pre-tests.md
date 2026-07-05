# Pre-Tests: runtime-claude-launch-and-session-evidence-governance

## Unit
- acceptance target: `No narrower truthful unit seam exists because the bug lives in shell launcher invocation plus runtime session-anchor persistence.`
- testing layer: `unit`
- target environment: `feature/fix-tool-switch-noninteractive-state-20260419-2315`
- required evidence: `focused shell regressions plus owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The failing contract crosses CLI argv/stdin composition and runtime resume-target truth, so fake lower-level units would be less truthful than the focused shell tests already present.`
- replacement_evidence: `Focused shell regressions, syntax checks, manual CLI replay, diff hygiene, governance-check, and owner verification artifact cover the smallest stable boundary.`

## Integration
- acceptance target: `Claude-family fallback launches succeed non-interactively and resume-target truth only persists verified evidence.`
- testing layer: `integration`
- target environment: `feature/fix-tool-switch-noninteractive-state-20260419-2315`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-tool-launchers-cc-stdin-add-dir`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-claude-resume-target-requires-evidence`.
3. Run `bash -n docs/system/workspace/scripts/runtime/tool-launchers.sh`.
4. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
5. Run `git diff --check`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `The guarded promotion path preserves the same Claude-family launch and session-evidence behavior before develop absorbs the owner.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-tool-switch-20260419-2359`
- required evidence: `guarded replay plan plus premerge verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge the feature lane into the disposable `test-pre-merge-tool-switch-20260419-2359` batch.
2. Replay the focused regression set and governance-check there in `premerge-integration`.
3. Promote that batch into `develop` only after the owner evidence remains aligned.

## Real-Environment
- acceptance target: `A real Claude CLI invocation with runtime-equivalent flags succeeds after the fix, and a resume launch without evidence falls back cleanly.`
- testing layer: `real_environment`
- target environment: `feature/fix-tool-switch-noninteractive-state-20260419-2315`
- required evidence: `manual CLI replay plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `Real Claude CLI replay and runtime-equivalent fresh/resume launcher replays already ran in this feature lane on 2026-04-19, proving the bounded launch-contract and session-evidence repair against the actual tool binary.`
1. Run `printf 'say hi\n' | claude -p --permission-mode bypassPermissions --add-dir /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees`.
2. Run a runtime-equivalent fresh launcher replay and confirm it returns content.
3. Run a runtime-equivalent resume replay with no verified evidence and confirm it falls back to fresh execution.

## Acceptance Items

### Claude print-mode with add-dir accepts stdin-fed prompts
- id: `claude-print-mode-add-dir-stdin-contract`
- requirement: `Claude-family print-mode fallback should accept the runtime launch when prompt content is sent through stdin under --add-dir.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1`
- case_design: `Intercept the launcher path, replay the command with --add-dir, and assert the prompt reaches Claude on stdin instead of as broken argv text.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/code-reviews/20260419-runtime-claude-launch-and-session-evidence-verification.md`

### Claude resume target requires verified session evidence
- id: `claude-resume-target-requires-evidence`
- requirement: `Claude-family resume launches should only reuse a session target when project-local session evidence exists.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2,tasks.md#3`
- case_design: `Simulate fresh and resume cycles without Claude jsonl evidence, then assert stale session ids are rotated or cleared instead of becoming resumable truth.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/code-reviews/20260419-runtime-claude-launch-and-session-evidence-verification.md`

### Guarded promote preserves Claude fallback adequacy
- id: `guarded-promote-preserves-claude-fallback-adequacy`
- requirement: `The premerge replay must preserve stdin-fed Claude-family launch behavior and verified session-evidence gating before develop absorbs this owner.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#1,tasks.md#2,tasks.md#3,tasks.md#4`
- case_design: `Replay the focused regression set plus governance-check in the disposable premerge batch and confirm the guarded promote path still carries the same bounded repair.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/code-reviews/20260419-runtime-claude-launch-and-session-evidence-verification.md`
