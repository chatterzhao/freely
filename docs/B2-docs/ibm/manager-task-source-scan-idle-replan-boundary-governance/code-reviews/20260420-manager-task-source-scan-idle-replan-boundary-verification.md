# Verification: manager-task-source-scan-idle-replan-boundary-governance

- issue_id: `I-20260420-1130-A`
- issue_path: `docs/B2-docs/ibm/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md`
- verification_date: `2026-04-20`
- verifier: `codex`
- branch: `feature/startup-task-source-patrol-and-reconcile-20260420`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`

## Scope Verdict

- `PASS`: the owner stays bounded to manager idle/replan patrol regeneration, suppression, and standing-surface patrol seed truth rather than widening into provider automation.
- `PASS`: focused patrol regressions prove milestone patrol seed inclusion, idle-after-continuity regeneration, active-worker suppression, stale delegated filtering, and runtime script validity.
- `PASS`: live self-host evidence shows the product-level success standard behind this owner is real: after startup, the manager found work autonomously, dispatched a worker, and kept broad patrol suppressed while that worker remained active.
- `PASS`: the remaining protected-branch step is governance-only closeout through the authoritative `test-pre-merge-20260420-autonomous-task-governance` batch.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-includes-milestone-patrol-seed`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-suppresses-broad-patrol-while-worker-active`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`
5. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-provider-hints`
6. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
7. `bash docs/system/workspace/scripts/tests/test-start-lead-agent-verification-metadata-contract`
8. `bash -n docs/system/workspace/scripts/runtime/freely`
9. `./bin/governance-check`
10. Runtime evidence review:
   - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-external-issue-source-lifecycle-governance/.freely/run/worker-continuity-20260420-200317-external-issue-verification-closeout.md`
   - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-external-issue-source-lifecycle-governance/.freely/logs/runtime-events.log`
   - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-test-pre-merge-autonomous-task-governance/.freely/logs/runtime-events.log`

## Results

1. The focused patrol regressions passed on the bounded runtime/script seam that introduced `task-source-scan` and its manager prompt consumption contract.
2. `task-source-scan` remains an idle/replan step rather than an every-cycle scan, and the same regressions show active-worker rounds suppress broad patrol regeneration.
3. `test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor` proves stale pre-stop continuity no longer hijacks current patrol seed truth.
4. `test-freely-task-source-scan-provider-hints` keeps provider setup guidance non-blocking, which preserves this owner's boundary: provider automation remains a follow-on seam rather than a prerequisite for patrol scan itself.
5. `test-freely-task-source-scan-python-compat` proves the runtime entrypoint can import the patrol scanner under `python3` without evaluating unsupported annotation syntax.
6. `test-start-lead-agent-verification-metadata-contract` proves launch-time prompt composition still carries the machine-readable verification metadata required by the current guarded worker-launch path.
7. Runtime evidence from the feature and authoritative premerge lanes shows the product-level question for this owner is already answered `yes`: after startup, the manager found work, consumed the bounded patrol input, and dispatched a worker without requiring a human to seed a fixed task list.

## Implementation Decision Note

- decision: `Materialize the idle/replan patrol seam as its own bounded owner, with machine-readable task-source scan truth and explicit suppression/regeneration triggers, instead of leaving it as candidate-only pre-research or widening into provider automation.`
- why_this: `The observed failure was not missing sources; it was missing runtime-owned replan boundaries. A bounded owner is required because the repo already contains real runtime/tests/skills changes for this seam, and candidate-only evidence would leave guarded develop promote without a canonical owner chain.`
- alternatives_considered: `Keep the work in pre-brainstorm only; absorb it into the older completed source-patrol owner; widen the same lane into GitHub/Gitee provider scan and writeback automation.`
- boundary_non_goals: `This owner does not implement provider APIs, does not redesign generic recovery/fleet orchestration, and does not collapse standing surfaces into new raw-source families.`
- residual_risk: `A later owner may still need to bring recovery or provider writeback into the same patrol transaction, but that should happen only if those seams can no longer stay outside this bounded idle/replan contract.`
