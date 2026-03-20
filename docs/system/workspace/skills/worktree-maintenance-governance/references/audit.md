# Worktree Audit

用于核清单棵 worktree 的真实状态。

## 必查面

1. `git status`
2. `docs/pre-brainstorms/**`
3. `docs/epics/**` 下的 issue / prd / pre-tests / tasks / code-reviews
4. `docs/milestones.md`
5. 相关测试或 runtime 变更

## 输出分类

- `merge-ready`
  - issue / tasks / review / tests / milestone 对齐
- `research-only`
  - 仍停留在 pre-brainstorm / candidate，且 `next_action + revisit_trigger` 清楚
- `companion-only`
  - 只能作为历史 companion 或 traceability，不应独立 promote / merge
- `retire-only`
  - 独有价值已被收编，只剩 cleanup / salvage_then_retire

## 硬规则

- 不只看 milestone
- 不把 `completed` 文案当成唯一真相，必须对照 issue / review / tests
- 若当前树仍有独有实现能力，不得草率判为 retire-only
