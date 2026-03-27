# Brainstorm: pre-test-merge-responsibility-usage-and-lifecycle-governance

## Compatibility Note

- 历史 brainstorm/path 保留 `pre-test-merge` 命名，避免破坏既有引用。
- 当前 canonical 语义已经升级为 `test-pre-merge-*` 测试批次前缀族。
- 下文出现的 `pre-test-merge` 都按 `test-pre-merge-*` 前缀族理解。

## Source freeze

- `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`

## Stable boundary

当前已经足够稳定进入 IBM 的边界只有一条：

- 定义 `pre-test-merge` 作为治理对象的职责、允许用法、stale/retire/rebuild 规则，以及 promotion 默认语义。

当前不纳入本 issue 的内容：

- runtime/status 如何暴露 batch freshness
- branch-management / patrol 具体怎样能力化检测 stale batch
- protected-env 差异如何 machine-readable surfaced

这些都属于下一条 lifecycle：历史名称仍写作 `pre-test-merge lifecycle management capability for Freely`，但语义上指向 `test-pre-merge-*` 批次族的后续能力化。

## Key decisions for IBM

1. `pre-test-merge` 是临时预集成验证批次，不是长期开发父分支。
2. `pre-test-merge` 是 protected validation environment，不承担真实 feature 开发。
3. `develop` 才是长期集成真相；`pre-test-merge` 只是一轮验证批次中的临时观察面。
4. 当 `develop` 已经前进、批次出现 protected-env 独有差异、或 promotion/cleanup 证据断裂时，当前批次必须允许被判定 stale。
5. stale batch 后默认优先 replay 来源 feature，而不是继续把旧批次快照当作 promote 单位。

## IBM focus

- 把以上治理定义写进真源文档
- 保持与现有三层 loop、branch/worktree、cleanup 和 patrol 语义一致
- 明确后续能力化问题仍是下一条独立生命周期
