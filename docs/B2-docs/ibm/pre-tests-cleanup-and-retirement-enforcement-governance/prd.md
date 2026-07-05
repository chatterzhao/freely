# PRD: pre-tests-cleanup-and-retirement-enforcement-governance

## Goal

把 cleanup / retirement 决策统一绑定到 issue-bound `pre-tests.md`，补齐 completion / merge 之后的 lifecycle closure 测试闭环。

## Why Now

当前 completion gate 和 `test-pre-merge-* -> develop` promote gate 都已经消费 `pre-tests.md`，但 cleanup / retirement 仍未统一消费同一真源。这是真缺口，但属于明确 deferred，不是功能回退。

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/`
- `docs/system/workspace/hooks/`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`

## Non-Goals

- 不做 adequacy schema v2
- 不做 launch-time verification hard gate
- 不新增 `tests.md`
- 不做全仓 pre-tests retirement audit

## Non-Negotiables

- cleanup / retirement 必须读取 issue `pre_tests_path`
- gate 失败时必须阻止 retirement，并返回 item-level 缺口
- completion / merge 既有 gate 不能回退
- deferred 历史必须保留为 deferred，不得写成 regression 叙事
