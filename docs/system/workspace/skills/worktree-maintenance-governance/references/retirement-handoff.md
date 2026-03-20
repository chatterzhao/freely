# Retirement Handoff

用于 historical / companion / obsolete worktree 的收口。

## 目标

区分三种情况：

1. `merge whole branch`
2. `salvage_then_retire`
3. `keep research-only`

## 必查面

- 当前树是否还有独有能力
- 独有价值是实现、治理边界，还是仅剩 traceability
- 主线是否已有同题能力完成态
- 是否混入跨能力材料，导致整支 merge 会回退主线

## 输出

- 可摘取的最小差异
- 绝不能整支合并的范围
- retirement 前置条件

## 硬规则

- companion 只能摘自己的历史说明与 traceability，不得再次当主线来源
- obsolete branch 若大部分语义已被主线吸收，只收编独有小能力，然后 retire
- cleanup 前仍必须回到 `skill:branch-management` 的 cleanup lifecycle
