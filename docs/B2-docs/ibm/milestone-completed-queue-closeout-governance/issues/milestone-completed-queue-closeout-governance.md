# Issue: milestone-completed-queue-closeout-governance

- issue_id: `I-20260406-1105-A`
- title: Milestone completed-queue closeout governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `milestone-completed-queue-closeout-governance`
- issue-name: `milestone-completed-queue-closeout-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260406-1105/candidates.md#c-20260406-1105-a`
- source_brainstorm: `docs/B1-docs/raw-20260406-1105/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-milestone-completed-queue-closeout-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/milestone-completed-queue-closeout-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/governance-merge-gate-milestone-status-followthrough-governance/issues/governance-merge-gate-milestone-status-followthrough-governance.md`
  - `docs/system/workspace/scripts/quality/governance-check`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The active milestone still keeps several completed owners in `committed_issues`. That conflicts with milestone policy and leaves the main orchestration surface with stale sequencing truth.

`governance-merge-gate` is not the missing contract here, because it only evaluates the current develop-bound diff. The missing contract is a baseline repo-wide audit that can detect historical queue drift already present on canonical `develop`.

## Scope

1. Repair canonical `docs/milestones.md` so the completed owners live only under `completed_issues`.
2. Add a repo-wide `governance-check` audit that compares milestone queue placement with the referenced issue `phase_state`.
3. Add a focused regression for the completed-in-committed failure mode.

## Non-Goals

1. Do not redesign milestone format.
2. Do not add queue auto-repair.
3. Do not widen into lifecycle automation.
4. Do not reopen the parser scope of `I-20260404-0119-A`.

## Acceptance

1. The active milestone no longer leaves completed owners in `committed_issues`.
2. `./bin/governance-check` fails when a milestone issue entry is in the wrong queue for its issue `phase_state`.
3. The focused regression proves both the failure and the repaired pass path.
4. The owner remains narrow: queue closeout plus baseline audit.

## Verification

- `bash docs/system/workspace/scripts/tests/test-governance-check-milestone-phase-queue-alignment`
- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `./bin/governance-check`
- `git diff --check`

## Next

- Re-open only if canonical milestone queue drift reappears without a develop-bound diff for merge-gate to catch, or if another queue artifact starts carrying the same sequencing truth.
