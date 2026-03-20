---
name: worktree-maintenance-governance
description: 当主管需要核清单个 worktree 的真实状态、为多条 worktree 制定安全 merge 顺序、或处理 companion/obsolete worktree 的 salvage_then_retire 时使用。
---

# skill:worktree-maintenance-governance

## 何时使用

- 需要判断某个 worktree 是 `merge-ready`、`research-only`、`companion-only` 还是 `retire-only`
- 需要为一组相关 worktree 做 merge-prep，而不是只看 milestone
- 需要处理 historical / companion / obsolete worktree 的差异摘取与 retirement handoff

## 模式选择

1. 单棵树真实状态核对：读 [references/audit.md](references/audit.md)
2. 多棵树合并预演：读 [references/merge-prep.md](references/merge-prep.md)
3. 历史工位收口与退休：读 [references/retirement-handoff.md](references/retirement-handoff.md)

## 工作流

1. 先跑 `skill:constitution-guard` 和 `skill:laws-enforcer`
2. 若当前承担项目级判断，先结合 `skill:multi-worktree-supervision` 读取工位总览
3. 再根据当前问题选择 `audit / merge_prep / retirement_handoff`
4. 结论必须落成清晰分类或顺序：
   - `merge-ready`
   - `research-only`
   - `companion-only`
   - `retire-only`
5. 若问题只是创建/进入/删除 worktree，回到 `skill:branch-management`
6. 若问题已经升级为高风险文本冲突收敛，切到 `skill:premerge-reconcile`

## 边界

- 不替代 `branch-management` 的创建、promotion 和 cleanup 基础命令
- 不替代 `worktree-hygiene-supervision` 的 dirty-budget / checkpoint 收口
- 不替代 `premerge-reconcile` 的冲突修复
- 不允许只凭 `milestones.md` 单独下结论

## 完成

- 当前问题已被稳定分类，或已有可执行的 merge / retire checklist
- companion / research / completed 的边界不再混淆
