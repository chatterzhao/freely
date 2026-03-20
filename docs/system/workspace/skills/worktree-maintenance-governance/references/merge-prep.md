# Merge Prep

用于一组相关 worktree 的安全合并预演。

## 输入

- 相关 worktree 列表
- 每条工位的 issue / candidate / review / tests
- `git diff --name-only develop...<branch>`
- 必要时的 `git merge-tree`

## 输出

1. 安全顺序
2. 共享真源文件
3. 实际冲突面
4. 每步回归测试

## 必查面

- 是否有共享真源：
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - `start-lead-agent.sh`
  - `test-routing-foundation-loop`
  - `three-loop-capability-lifecycle.md`
- 是否存在主线 / 增量 / companion 关系
- 是否有 branch 只是 research-only，不应强行 merge

## 硬规则

- 先定顺序，再谈冲突修复
- completed 主线不得被 companion / candidate 视图回拉
- 若只是共享真源叠加语义，先按顺序 merge，不提前进入 `premerge`
- 若已出现高风险冲突，再切 `skill:premerge-reconcile`
