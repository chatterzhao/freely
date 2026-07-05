# Pre-Tests: runtime-closeout-selfhost-validation-followthrough-governance

## Unit
- acceptance target: `No narrower executable unit seam is required because the bounded behavior lives in integrated runtime shell and interruption-routing scripts.`
- testing layer: `unit`
- target environment: `feature/checkpoint-runtime-closeout-selfhost-validation-20260419`
- required evidence: `focused shell regressions plus owner verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The preserved checkpoint seam only becomes meaningful across integrated daemon-start, start-lock, and interruption-routing behavior, so a fake lower-level unit seam would be less truthful than the focused shell regressions already present.`
- replacement_evidence: `Focused shell regressions, diff hygiene, governance-check, and owner verification artifacts cover the smallest stable boundary.`

## Integration
- acceptance target: `The checkpoint follow-on preserves lawful daemon reuse, ambiguous start-lock cleanup, and interruption-manager fast-path routing without breaking the generic AI fallback path.`
- testing layer: `integration`
- target environment: `feature/checkpoint-runtime-closeout-selfhost-validation-20260419`
- required evidence: `focused regression output plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-ambiguous-missing-state`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-start-lock-acquires-with-missing-run-dir`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-rejects-when-runtime-already-running`.
6. Run `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`.
7. Run `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`.
8. Run `git diff --check`.
9. Run `./bin/governance-check`.
10. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`.
11. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`.
12. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`.
13. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-handoff-rebinds-cleanup-closeout`.
14. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-only-done-forces-resume`.
15. Run `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`.
16. Run `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-syncs-tooling-before-launch`.
17. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-nonbusy-worker-recovers`.
18. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-writes-continuation-handoff`.
19. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-clears-stale-worker-repair-handoff`.

## End-to-End
- acceptance target: `The bounded owner is documented well enough that a later guarded replay can evaluate it as one lawful feature lane instead of a checkpoint-only branch.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge-runtime-closeout-selfhost-validation-20260419`
- required evidence: `guarded replay plan plus premerge verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Create or select a disposable `test-pre-merge-*` batch only after this owner is ready for guarded replay.
2. Replay the focused regression set there in `premerge-integration`.
3. Record the promote adequacy result in a closeout verification artifact.

## Real-Environment
- acceptance target: `A real self-host replay in the active checkpoint worker worktree can still distinguish lawful daemon reuse from duplicate detached startup before guarded promote.`
- testing layer: `real_environment`
- target environment: `feature/checkpoint-runtime-closeout-selfhost-validation-20260419`
- required evidence: `real self-host replay evidence in the active checkpoint worktree plus owner verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: `pass`
- real_environment_reason: `This owner's truthful real-environment surface is the active checkpoint worker worktree where duplicate detached startup was originally observed. Two real self-host replays there now show repeated daemon start stays on the no-relaunch path across both early bootstrap and post-ai-launch timing windows.`

## Acceptance Items

### Daemon start reuses healthy same-project supervisor
- id: `daemon-start-reuses-live-supervisor`
- requirement: `Repeated daemon start should reuse a healthy same-project supervisor instead of launching another detached runtime chain.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#1`
- case_design: `Start a detached runtime, rerun daemon start, and assert the same supervisor pid is reused without creating another daemon-run process.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260419-runtime-closeout-selfhost-validation-followthrough-verification.md`

### Ambiguous missing-state start lock is cleaned safely
- id: `ambiguous-start-lock-cleans-when-runtime-is-absent`
- requirement: `Ambiguous project start locks with missing state should be cleaned only when no runtime is actually active.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2`
- case_design: `Seed a lock directory without state.env, prove there is no active runtime, and assert freely start cleans the lock before reacquiring it.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260419-runtime-closeout-selfhost-validation-followthrough-verification.md`

### Interruption manager fast paths stay bounded
- id: `interruption-manager-fast-paths-stay-bounded`
- requirement: `Cleanup-oriented and broad-supervision prompts take the new fast paths, while generic prompts still invoke the AI fallback path for codex and cc.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#3`
- case_design: `Replay cleanup, manager-supervision, and generic prompts against interruption-manager-handler, then assert direct fast-path output only where intended and prompt generation still happens for generic codex/cc fallback cases.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260419-runtime-closeout-selfhost-validation-followthrough-verification.md`

### Guarded promote preserves closeout selfhost adequacy
- id: `guarded-promote-preserves-closeout-selfhost-adequacy`
- requirement: `The guarded test-pre-merge replay keeps the new exit-contract repair prompt ordering and the existing exit-contract repair directives intact before develop absorbs this owner.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#6`
- case_design: `Merge this owner into test-pre-merge-20260424-worker-exit-contract-repair-focus, rerun the repair-first prompt regression plus the two existing exit-contract regressions and governance-check there, and confirm the guarded promote path preserves the narrow repair contract ordering.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-exit-contract-repair-focus-verification.md`

### Exit-contract repair prompt stays repair-first
- id: `exit-contract-repair-prompt-stays-repair-first`
- requirement: `When runtime resumes a worker or manager specifically for exit-contract repair, the repair contract must render ahead of the broad lead-agent preamble so the resumed lane repairs the contract before any wider patrol.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#6`
- case_design: `Seed a worker repair session handoff, build the prompt, and assert the repair-first override appears before the lead-agent body while the broader exit-contract directive and resume-repair enforcement still pass.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-exit-contract-repair-focus-verification.md`

### Cleanup repair round cannot short-circuit closeout
- id: `cleanup-repair-round-cannot-short-circuit-closeout`
- requirement: `A retained cleanup worker resumed only to repair its exit contract must re-enter the original cleanup closeout gate and may not stop with a repair-only worker_done backed solely by runtime repair artifacts.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#6`
- case_design: `First prove in feature-local that a cleanup worker prompt with authoritative verification metadata rewrites the repair handoff back onto the original closeout gate, then replay the same regressions in the guarded test-pre-merge lane and confirm runtime still rejects a repair-only worker_done that cites only the handoff plus rewritten contract.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-cleanup-reentry-verification.md`

### Worker recovery syncs canonical tooling before launch
- id: `worker-recovery-syncs-canonical-tooling-before-launch`
- requirement: `When manager runtime restarts an expected-running worker, it must sync canonical tooling into that worktree before launching the worker supervisor so newly merged runtime fixes are not bypassed by stale worktree scripts.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#7`
- case_design: `Seed a target worktree with a stale local bin/freely, invoke the runtime launch helper from a canonical source project, and assert the launched supervisor executes the synced replacement instead of the stale script.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-worker-recovery-sync-verification.md`

### Manager cleanup resume stays on continuation truth
- id: `manager-cleanup-resume-stays-on-continuation-truth`
- requirement: `A valid manager resume_manager contract for retained cleanup followthrough must write a continuation handoff rather than dropping the next round back into exit-contract repair semantics.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#8`
- case_design: `Seed a valid cleanup-governance resume_manager contract, run the exit-contract consumer, and assert runtime writes a continuation handoff plus cleanup followthrough evidence instead of a repair handoff.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-manager-resume-and-stale-worker-handoff-verification.md`

### Authoritative worker relaunch clears stale repair handoff
- id: `authoritative-worker-relaunch-clears-stale-repair-handoff`
- requirement: `When manager re-delegates the retained cleanup worker with a fresh authoritative prompt, runtime must clear any stale worker exit-contract repair handoff so the next worker round follows the cleanup prompt instead of replaying repair-only semantics.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#8`
- case_design: `Seed a retained worker worktree with an old worker_exit_contract_repair handoff, relaunch it through an authoritative manager prompt, and assert the stale handoff is cleared before the next worker round while the adjacent repair-first and invalid-contract regressions still pass in protected replay.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-manager-resume-and-stale-worker-handoff-premerge-verification.md`
