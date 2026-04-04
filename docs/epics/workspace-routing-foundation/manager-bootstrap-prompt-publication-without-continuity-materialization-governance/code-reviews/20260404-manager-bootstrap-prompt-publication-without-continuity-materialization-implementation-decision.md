# Implementation Decision: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- issue_path: `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- branch: `feature/manager-bootstrap-prompt-publication-without-continuity-materialization-20260404-1405`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-1405-feature-manager-bootstrap-prompt-publication-without-continuity-materialization`
- decision_date: `2026-04-04`
- author: `codex`

## Decision

- keep the bounded bootstrap grace check in `docs/system/workspace/scripts/runtime/freely` so the watchdog does not restart a fresh supervisor solely because `ai.pid` has not appeared yet
- extend the continuity parser to treat `## Worker Dispatch` prompt paths as launchable worker handoff evidence, because current manager continuity output uses that heading for the delegated prompt selected in the active round

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
