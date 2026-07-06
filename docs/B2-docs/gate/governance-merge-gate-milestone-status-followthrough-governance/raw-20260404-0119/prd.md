# PRD: governance-merge-gate-milestone-status-followthrough-governance

## Goal

修复 `governance-merge-gate` 对 `docs/milestones.md` 的 milestone 状态解析边界，使 active milestone 不会被 nested queue item status 误降级。

## Why Now

这条问题已经真实阻断了 runtime bootstrap owner 的 canonical replay。若不先修 parser，后续 develop-bound merge 仍会对合法 active milestone 产生 false negative。

## Product Surface

- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/scripts/tests/test-governance-merge-gate`

## Non-Goals

- 不改 milestone 排程语义
- 不重写 queue item metadata contract
- 不吸收 runtime `/bin/ps` fallback 逻辑

## Non-Negotiables

- milestone 顶层 `status` 必须只来自 milestone 顶层字段
- nested queue item metadata 不能改写 parent milestone truth
- 回归测试必须覆盖真实误报形状，而不是只做抽象单元断言

## Decomposition

1. materialize narrow followthrough owner
2. fix milestone-status parser boundary
3. add focused regression
4. replay into develop, then retry blocked runtime lane
