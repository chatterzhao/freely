# Issue: three-loop-lifecycle-single-source-governance-followthrough

- issue_id: `I-20260419-0915-A`
- title: `Three-loop lifecycle single-source governance followthrough`
- phase_state: `done`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `three-loop-lifecycle-single-source-governance-followthrough`
- issue-name: `three-loop-lifecycle-single-source-governance-followthrough`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260419/candidates.md#c-20260419-0915-a`
- source_brainstorm: `docs/B1-docs/raw-20260419/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- reopen_reason: `the original three-loop model owner already completed, but this follow-on governance pass still needs to land the single detailed truth rule and consumer read/sync contract through a lawful protected-branch path`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-three-loop-lifecycle-single-source-governance-followthrough.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/lead-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- created_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The whole-app lifecycle model is important enough that Freely should maintain exactly one detailed truth source for it. The active docs refactor already pushes the detailed semantics into `docs/system/workspace/three-loop-capability-lifecycle.md` and reduces other consumer documents to lighter references plus read/sync expectations.

Because the earlier three-loop architecture owner is already `completed`, this governance-only closeout still needs its own lawful owner chain before `develop` can absorb the diff. The work is not a new architecture redesign; it is a bounded followthrough that prevents multi-truth drift.

## Scope

1. Make `docs/system/workspace/three-loop-capability-lifecycle.md` the sole detailed whole-app lifecycle specification in the active truth set.
2. Require downstream skill and agent docs to read and sync against that canonical lifecycle truth when loop semantics matter, instead of co-maintaining parallel detailed restatements.
3. Carry the minimum candidate -> issue -> progress -> verification lifecycle evidence needed for guarded develop replay.
4. Retire the temporary feature and test-pre-merge worktrees after canonical `develop` absorbs the governance-only closeout.

## Non-Goals

1. Do not reopen the broader three-loop architecture decision from `I-20260324-0405`.
2. Do not add runtime behavior, product logic, or test-surface changes unrelated to documentation governance.
3. Do not create another detailed lifecycle specification elsewhere in the repo.
4. Do not leave the temporary merge worktrees active after the guarded replay succeeds.

## Acceptance

1. `docs/system/workspace/three-loop-capability-lifecycle.md` remains the only detailed whole-app lifecycle spec among the active truth files touched by this lane.
2. `docs/PROJECT_INTENT.md`, `docs/LAWS.md`, and the touched agent/skill docs reference or defer to the canonical lifecycle doc instead of restating detailed loop semantics in parallel.
3. The touched skill/agent docs state the consumer contract clearly enough that authors know to read and sync to the canonical lifecycle doc when they need loop semantics or when they update related behavior.
4. `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md` passes.
5. `./bin/governance-check` passes.
6. Guarded replay through `test-pre-merge-three-loop-governance-20260419` and then `develop` succeeds, followed by retirement of the temporary feature and test-pre-merge worktrees.

## Verification

- `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- `./bin/governance-check`
- `git diff --check`
- `rg -n "three-loop-capability-lifecycle|canonical lifecycle truth|read and sync" docs/PROJECT_INTENT.md docs/LAWS.md docs/system/workspace/three-loop-capability-lifecycle.md docs/system/workspace/agents docs/system/workspace/skills`

## Completion

- `docs/B1-docs/raw-20260419/brainstorms.md`
- `docs/B1-docs/raw-20260419/candidates.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/pre-tests.md`
- `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/tasks.md`
- `docs/progress/workspace-routing-foundation/p-three-loop-lifecycle-single-source-governance-followthrough.md`
- `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260419-three-loop-lifecycle-single-source-followthrough-verification.md`
- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/lead-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/system/workspace/skills/doc-pre-brainstorm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
