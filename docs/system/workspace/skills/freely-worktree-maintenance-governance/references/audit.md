# Worktree Audit

用于核清单棵 worktree 的真实状态。

若当前问题已经变成“检查所有 active worktree 是否完成、哪些该 merge、哪些该 cleanup”，切到 [fleet-closure.md](fleet-closure.md)，不要用单树 audit 假装完成项目级判断。

## 必查面

1. `git status`
2. `docs/B1-docs/**`
3. `docs/B2-docs/**` 下的 issue / prd / pre-tests / tasks / code-reviews
4. `docs/milestones.md`
5. 相关测试或 runtime 变更

## 输出分类

- `merge-ready`
  - issue / tasks / review / tests / milestone 对齐
- `research-only`
  - 仍停留在 pre-brainstorm / candidate，且 `next_action + revisit_trigger` 清楚
  - 长期保留的是 canonical 文档，不是当前 research worktree
- `companion-only`
  - 只能作为历史 companion 或 traceability，不应独立 promote / merge
- `retire-only`
  - 独有价值已被收编，只剩 cleanup / salvage_then_retire

## 硬规则

- 不只看 milestone
- 不把 `completed` 文案当成唯一真相，必须对照 issue / review / tests
- 若当前树仍有独有实现能力，不得草率判为 retire-only
- 若当前树是 research-only，还必须继续判断：
  - canonical brainstorm / candidates / milestone candidate 区是否已完整回写
  - 若已回写完成，这棵树的正确 disposition 通常不是“继续挂着”，而是进入 `retirement_handoff`
