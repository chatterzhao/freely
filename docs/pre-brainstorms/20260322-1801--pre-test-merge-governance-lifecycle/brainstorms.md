# 预研头脑风暴：pre-test-merge-governance-lifecycle

## 背景

Freely 这次暴露出来的不是单纯的合并冲突，而是 `pre-test-merge` 的职责边界、允许用法、退出条件和批次生命周期都还不够清晰。

我们已经看到几种危险信号：

- `pre-test-merge` 被当成了“临时集成批次”和“事实主线”混用
- `develop` 继续前进后，旧批次仍被拿来比较或回收
- 一些有效实现只能在旧批次里看见，但回到 `develop` 时又可能被误删、误回退或重复引入
- 验证环境、promotion gate、cleanup gate 之间没有形成完整的 machine-readable 生命周期契约

这说明问题不在某个提交，而在 `pre-test-merge` 这一治理对象本身还缺一套清晰的责任模型。

## 为什么现在必须研究

Freely 正在用 Freely 开发 Freely。

这意味着：

- 只把 `pre-test-merge` 当人工临时分支，会不断重复同类问题
- 只修单次 merge，不会解决“旧批次为什么还活着”“什么时候该退休”“什么能 promote”这些更高层问题
- 这类问题一旦不被 materialize 成 Freely 能力，未来每次复杂集成都要靠人脑重新判断

## 当前事实

### 已确认的分支事实

1. `develop` 是长期集成主线。
2. `pre-test-merge` 是临时预集成验证分支，不应固化为长期开发父分支。
3. 复杂集成、短周期验收、冲突收敛、发布前预演可以启用 `pre-test-merge`，但它必须有清晰的批次边界。

### 已确认的治理缺口

1. 还没有明确区分：
- `pre-test-merge` 只做验证
- `develop` 才是最终集成真相

2. 还没有明确回答：
- 一个 `pre-test-merge` 批次什么时候 stale
- 哪些改动必须回到来源 feature worktree
- 哪些改动可以直接推进到 `develop`

3. 还没有形成完整的能力化输出：
- 不能自动解释当前批次归属
- 不能自动提示 stale batch
- 不能自动给出 promote / replay / retire 建议

## 问题定义

需要一条更完整的治理路线，回答：

> 当 Freely 启用 `pre-test-merge` 做预集成验证时，应该如何定义它的职责、允许的操作、失效条件、生命周期结束条件，以及它与 `develop` 的 promotion 关系，才能既保住有效实现，又不把旧批次误当成当前真相？

## 关键张力

1. `pre-test-merge` 是临时验证批次，不该长期承载实现真相。
2. 但多个 feature 的组合行为只能在它这里被看见，不能简单废掉它。
3. `develop` 是最终集成主线，但主线在前进时不能被旧批次的语义拖回去。
4. Git 本身不能天然表达 batch 生命周期，所以 Freely 需要显式治理与状态留痕。

## 预研方向

### 方向 A：明确 `pre-test-merge` 的职责模型

- 它只负责组合验证、冲突暴露、promotion 预演
- 不负责长期保存事实真相
- 不作为新的 feature 开发父分支
- 不作为默认回收旧实现的来源

### 方向 B：明确 `pre-test-merge` 的生命周期模型

- 批次开始
- 批次进行中
- 批次已验证
- 批次已失效
- 批次已退休

每个阶段都需要明确：

- 谁可以推进
- 谁可以读取
- 谁可以 promote
- 谁可以 retire

### 方向 C：把治理经验能力化

Freely 后续应具备能力去判断：

- 当前 `pre-test-merge` 是否仍是有效批次
- 是否已被 `develop` 甩开到需要重建
- 是否存在未回流到来源 worktree 的 protected-env 差异
- 是否能安全 promote，还是只能 replay 来源 feature

## 预期落点

- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/pre-brainstorms/**`
- `docs/milestones.md`

## 需要冻结的开放问题

1. `pre-test-merge` 的唯一职责是什么。
2. `pre-test-merge` 哪些操作允许，哪些绝对禁止。
3. 什么时候一个批次必须判定 stale。
4. 什么时候必须 retire 当前批次并重建。
5. 是否应该把 promote 语义改成“replay 来源 feature”而不是“保留批次快照”。
6. 这套判断要如何变成 Freely 可执行能力，而不是人脑记忆。
