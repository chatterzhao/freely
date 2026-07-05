# Pre-Tests: runtime-supervisor-attach-reuse-followthrough-governance

## Unit
- acceptance target: `No narrower executable unit seam is required because the preserved behavior lives in integrated runtime shell and tool-launcher behavior.`
- testing layer: `unit`
- target environment: `feature/checkpoint-lifecycle-trace-debuggability-20260419`
- required evidence: `focused shell regressions plus owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The preserved seam crosses runtime-shell attach logic and launcher environment setup, so a fake lower-level unit boundary would be less truthful than the focused integration regressions already present.`
- replacement_evidence: `Focused shell regressions, diff hygiene, governance-check, and owner verification artifacts cover the smallest stable boundary.`

## Integration
- acceptance target: `The checkpoint preserves healthy supervisor reuse/attach behavior and Claude runtime-home isolation without relaunching duplicate runtimes.`
- testing layer: `integration`
- target environment: `feature/checkpoint-lifecycle-trace-debuggability-20260419`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-live-supervisor-between-ai-cycles`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-when-ps-is-unavailable`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-cc-launch-isolates-home-under-project-runtime`.
5. Run `git diff --check`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `The bounded checkpoint can later be replayed through a lawful protected-lane path instead of remaining branch-local truth.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-runtime-supervisor-attach-reuse-20260419`
- required evidence: `guarded replay plan plus premerge verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Create or select a disposable `test-pre-merge-*` batch only after this owner is ready for guarded replay.
2. Replay the focused regression set there in `premerge-integration`.
3. Record the promote adequacy result in a closeout verification artifact.

## Real-Environment
- acceptance target: `No real-repo replay is required for this round because the bounded seam is already covered by deterministic project-local shell fixtures.`
- testing layer: `real_environment`
- target environment: `feature/checkpoint-lifecycle-trace-debuggability-20260419`
- required evidence: `focused fixture coverage plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `This owner's truthful risk surface is the project-local runtime reuse and launcher-home isolation already exercised by the focused shell fixtures, so an extra real-repo replay is not needed before materializing the owner.`

## Acceptance Items

### Daemon start reuses a live supervisor
- id: `daemon-start-reuses-live-supervisor`
- requirement: `Repeated daemon start should reuse a healthy same-project supervisor instead of launching another daemon-run process.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1`
- case_design: `Start a detached runtime, rerun daemon start, and assert the same supervisor pid is reused without creating another daemon-run process.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews/20260419-runtime-supervisor-attach-reuse-followthrough-verification.md`

### Foreground start attaches between AI cycles
- id: `foreground-start-attaches-between-ai-cycles`
- requirement: `Foreground freely start should attach to the same live supervisor between AI cycles instead of repairing it.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2`
- case_design: `Start a detached runtime, wait for a between-cycles state with missing ai.pid, then assert a foreground start reuses the same supervisor and records already_running_attach.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews/20260419-runtime-supervisor-attach-reuse-followthrough-verification.md`

### Attach still works when ps is unavailable
- id: `attach-persists-when-ps-is-unavailable`
- requirement: `Attach should still reuse the healthy project runtime when ps is unavailable but cwd ownership is provable.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#3`
- case_design: `Stub ps to fail, keep supervisor and watcher pids alive under the project cwd, and assert freely start still records supervisor_attach_reuse.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews/20260419-runtime-supervisor-attach-reuse-followthrough-verification.md`

### Claude launcher HOME stays project-local
- id: `claude-home-isolated-under-project-runtime`
- requirement: `Claude launcher HOME should be isolated under the project runtime tree.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#4`
- case_design: `Intercept a Claude launch, inspect HOME and argv, and assert the launcher materializes project-local runtime-home directories.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews/20260419-runtime-supervisor-attach-reuse-followthrough-verification.md`

### Guarded promote preserves supervisor attach/reuse adequacy
- id: `guarded-promote-preserves-supervisor-attach-reuse-adequacy`
- requirement: `The guarded test-pre-merge replay keeps daemon reuse, foreground attach windows, ps-degraded ownership proof, and Claude runtime-home isolation intact before develop absorbs this owner.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#1,tasks.md#2,tasks.md#3,tasks.md#4`
- case_design: `Merge the checkpoint owner into the current test-pre-merge-runtime-lifecycle-20260419 batch, rerun the bounded regression set plus governance-check there, and confirm the guarded promote path still carries the same attach/reuse behavior.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-supervisor-attach-reuse-followthrough-governance/code-reviews/20260419-runtime-supervisor-attach-reuse-followthrough-verification.md`
