# PRD: develop-push-attempt-followthrough-governance

## Goal

在不引入硬 auto-push 或重试引擎的前提下，让每次 `develop` merge 都自动触发一次受控 push attempt，并把 blocked 结果写回成显式 followthrough truth。

## Why Now

- 现有 `push_pending` / `push_deferred` / urgency / resync truth 已经证明可见性有价值
- 但当前 merge 仍可能没有被实际尝试 remote delivery
- 当前 repo 已多次证明 `develop` local-only canonical truth 会积债

## Product Surface

- `docs/LAWS.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`

## Non-Goals

- hook auto-push
- hidden network side effects in git hooks
- retry-until-success transport automation
- replacing pre-push gate

## Non-Negotiables

- single controlled attempt only
- attempt failure must become explicit followthrough truth
- `push_blocked` must remain manager-consumable and patrol-visible
- lawful defer windows remain valid
- hooks remain gate-only

## Prototype Path

1. introduce `freely develop-push attempt`
2. write blocked-attempt state when `develop` stays ahead after a failed attempt
3. trigger one attempt from the guarded merge path after successful `develop` merge
4. keep failure handling explicit and bounded

## Eval Plan

成功：

- guarded merge into `develop` triggers one attempt
- successful attempt leaves `develop` clean relative to remote
- blocked attempt leaves `push_blocked` with explicit reason
- manager/status surfaces treat `push_blocked` as immediate followthrough

失败：

- merge still requires purely manual push memory
- blocked attempts remain generic `push_pending`
- merge path silently retries push or hides the failure
