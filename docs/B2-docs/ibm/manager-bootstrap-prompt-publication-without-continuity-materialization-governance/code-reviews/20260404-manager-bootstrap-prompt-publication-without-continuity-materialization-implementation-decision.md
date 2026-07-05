# Implementation Decision: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- issue_path: `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- branch: `feature/manager-bootstrap-prompt-publication-without-continuity-materialization-20260404-1405`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-1405-feature-manager-bootstrap-prompt-publication-without-continuity-materialization`
- decision_date: `2026-04-04`
- author: `codex`

## Implementation Decision Note

- decision: `Keep the bounded bootstrap grace check in docs/system/workspace/scripts/runtime/freely and extend the continuity parser so ## Worker Dispatch prompt paths are treated as launchable worker handoff evidence.`
- why_this: `The observed failure split cleanly into a startup race before ai.pid existed and a post-bootstrap handoff-truth gap where the delegated prompt was written but hidden behind an unparsed continuity heading. Fixing both inside the same runtime contract keeps the owner narrow and restores truthful continuity-to-worker materialization.`
- alternatives_considered: `Considered rewriting manager continuity generation to stop emitting ## Worker Dispatch, and considered a status-only fallback that would regex prompt paths without updating runtime parser helpers. Both options would leave either a broader schema migration or inconsistent manager-launch behavior.`
- boundary_non_goals: `Do not redesign broader watchdog restart policy, operator-stop semantics, continuity schema wholesale, or unrelated worktree cleanup behavior.`
- residual_risk: `If future manager continuities invent another new heading for delegated prompts, runtime status could drift again until the parser is explicitly taught that format. This fix only absorbs the currently observed Worker Dispatch contract.`

## Why

- the observed control-plane failure had two separate boundaries:
  - a startup race before first AI launch
  - a post-bootstrap handoff-truth gap where the delegated prompt existed on disk but runtime status still surfaced `latest_manager_worker_prompts_generated=none`
- both boundaries belong to the same owner because they sit on the exact path from prompt publication to durable continuity and worker-handoff materialization

## Alternatives Considered

- rewrite manager continuity generation to stop emitting `## Worker Dispatch`
  - rejected because it would require a broader prompt/continuity contract migration while the runtime can safely absorb the current heading
- force `live-status` to fall back to raw prompt-path regexes without fixing the parser
  - rejected because manager worker launch, queue inspection, and semantic-loop detection all rely on the same parser helpers; a status-only patch would leave runtime behavior inconsistent
- widen into a general operator-stop semantic redesign
  - rejected because the current evidence is narrower and already actionable without reopening broader restart policy

## Non-Goals

- no broader watchdog redesign
- no generic continuity schema rewrite
- no unrelated worktree cleanup or protected-branch governance changes
