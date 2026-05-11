# Merge Prep

用于一组相关 worktree 的安全合并预演。

## 输入

- 相关 worktree 列表
- 每条工位的 issue / candidate / review / tests
- `git diff --name-only develop...<branch>`
- 必要时的 `git merge-tree`

若当前问题不是平面的一组相关工位，而是存在明确父子依赖链，先切到：

- [stacked-merge-chain.md](stacked-merge-chain.md)

## 输出

1. 安全顺序
2. 共享真源文件
3. 实际冲突面
4. 每步回归测试
5. anti-retrogression 结论

## 必查面

- 是否有共享真源：
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - `start-lead-agent.sh`
  - `test-routing-foundation-loop`
  - `three-loop-capability-lifecycle.md`
- 是否存在主线 / 增量 / companion 关系
- 是否有 branch 只是 research-only，不应强行 merge
- 若多个 worktree 涉及相近能力，必须比较：
  - 哪条分支的行为边界更清楚
  - 哪条分支的测试/verification 更完整
  - 哪条分支显式移除了旧 candidate / companion 残影
  - 哪条分支保留了更好的用户语义或更小的越权面

## Anti-retrogression rule

当多个 worktree 涉及类似功能时，不能只因为：

- 某条分支更早出现
- 某条分支更接近 `develop`
- 某条分支改动更少

就默认保留它。

必须先写清：

1. `baseline behavior`
   - 当前仓库里哪条线已经代表更好的能力基线

2. `regression risk`
   - 另一条线若直接 merge，会把哪些行为、验证门、提示词或治理状态拉回旧版本

3. `keep / drop / salvage`
   - 哪些文件应保留为主线
   - 哪些只应摘取少量差异
   - 哪些必须明确丢弃

若这三点写不清，就不算完成 merge-prep。

## 硬规则

- 先定顺序，再谈冲突修复
- 若已知存在 child/parent 依赖链，不得把它压平成“平面多棵树”直接谈顺序；必须先跑 stacked merge-chain 判断
- completed 主线不得被 companion / candidate 视图回拉
- merge-prep 可以合法检查 sibling worktree 的 dirty / readiness / conflict 面，但这不自动授予当前 actor 跨树 mutate authority；发现 blocker 后必须先回 manager arbitration
- 当存在“两个分支都碰相近功能”时，默认先保留设计更优、验证更强、边界更清楚的那条；另一条只允许 salvage 差异，不允许把主线拉回旧设计
- 若只是共享真源叠加语义，先按顺序 merge，不提前进入 `premerge`
- 若已出现高风险冲突，再切 `skill:freely-freely-premerge-reconcile`
