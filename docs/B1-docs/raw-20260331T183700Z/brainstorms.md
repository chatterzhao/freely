# Brainstorms - 20260331-1837--worker-first-hop-role-boundary-regression

## Context

- observed symptom: a worker worktree completed its delegated verification-closeout task, then the next runtime prompt pulled the same worker back into project-level supervision and merge-prep judgement for `develop`
- current live repro:
  - worker runtime: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260330-221339-feature-story-level-pretests-closeout`
  - delegated intake: `20260331-180920-manager-worker-20260331-175545-worker-story-level-pretests-closeout-codex`
  - first worker cycle: `cycle-20260331-180927.log`
  - follow-on worker cycle: `cycle-20260331-181154.log`
- risk: once a feature-worktree worker finishes its assigned issue, the next prompt can re-enter manager-style patrol, fleet reading, merge judgement, and even manager continuity writeback from the worker lane itself

## Confirmed Facts

### 1. The generated worker first-hop prompt still routes through `lead-agent`

`docs/system/workspace/scripts/start-lead-agent.sh` always emits the same top-level instructions:

- `进入 lead-agent，不要绕过首跳代理`
- `由 lead-agent 委托 skill:context-source-skill`
- `首跳代理：workspace/agents/lead-agent.md`

This is true even when:

- `MANAGER_MODE=false`
- current branch is `feature/*`

The current repro prompt files show exactly that:

- `.freely/run/prompt-20260331-180927.txt`
- `.freely/run/prompt-20260331-181154.txt`

Both prompts say:

- `MANAGER_MODE=false`
- current branch is `feature/story-level-pretests-closeout-20260330-221339`
- but still require entry through `lead-agent`

### 2. The product capability truth says `feature/*` sessions default to worker execution

`docs/system/workspace/agents/lead-agent.md` explicitly says:

- if current branch is `feature/*`, the session defaults to `worker-agent` execution responsibility

`docs/system/workspace/agents/worker-agent.md` explicitly says:

- worker does not do project-level worktree scheduling
- worker does not decide merge/freeze/cleanup policy for other worktrees
- worker only returns evidence / blocker / next-hop for its own delegated scope
- completion / cleanup judgement returns to `auto-loop`

So the current prompt contract and the role truth are not aligned.

### 3. The worker actually completed its delegated task before drifting

`cycle-20260331-180927.log` shows the worker did real delegated work:

- verified `I-20260325T033300Z-B`
- updated issue/progress state
- committed `adc87b4`
- reran `./bin/governance-check`

This was not a stalled or idle worker. The delegated lane advanced and then entered a new cycle.

### 4. The next worker cycle began doing manager-style supervision

`cycle-20260331-181154.log` starts by querying:

- `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

That is the root `develop` manager runtime, not just the worker lane.

The same worker tree then wrote:

- `.freely/manager-continuity-20260331-181300.md`

That artifact declares:

- `role: manager`
- `branch: develop`
- project-level merge-prep / cleanup judgement

This is role-boundary leakage, not merely a verbose worker summary.

## Boundary

- this is not just an observability issue
- this is not merely a nicer optimization opportunity
- this is a runtime-facing prompt/role contract regression:
  - worker first-hop prompt generation does not cleanly hand control to `worker-agent`
  - follow-on cycles allow a worker lane to rehydrate manager semantics after delegated work completes

## Bug Or Optimization?

Current judgement: **bug**

Why it is not merely an optimization:

- the capability truth already froze the intended role boundary
- the live repro violated that frozen boundary
- the worker emitted manager-only artifacts from a feature worktree
- the worker started reading root project runtime truth instead of limiting itself to delegated issue followthrough

The only optimization question left is implementation shape, not whether the behavior is acceptable.

## Same-Family Relationship

This is a focused follow-on regression against already completed role-boundary families, especially:

- `I-20260326T183500Z` manager-owner-stance-and-source-patrol-governance
- `I-20260326T172500Z` three-loops-sibling-relationship-and-terminal-governance

But the current dogfood evidence is not just old wording resurfacing in docs. It appears in:

- runtime-facing prompt generation
- worker follow-on session behavior
- emitted non-versioned worker/manager artifacts

So this should not be silently absorbed as “already solved”; it needs a fresh focused lifecycle.

## Open Questions

1. Is the whole defect explained by `start-lead-agent.sh` always entering `lead-agent`, or is there a second bug in how worker follow-on cycles are relaunched after task completion?
2. Should worker post-completion cycles terminate after continuity/blocker writeback unless a new worker-owned delegated intake exists?
3. Should worker lanes be prevented from writing `manager-continuity-*` artifacts entirely, even if the prompt drifts?
4. Is merge-prep judgement for a completed worker lane always manager-owned, or can a worker produce a narrower `merge-ready evidence` artifact without project-level disposition?

## Decision

- keep this line in `pre-brainstorm`
- do not patch `start-lead-agent.sh` yet
- first freeze the minimum bug surface:
  - prompt generation contract for `MANAGER_MODE=false`
  - worker post-completion reentry contract
  - forbidden artifact/role leakage from worker lanes
