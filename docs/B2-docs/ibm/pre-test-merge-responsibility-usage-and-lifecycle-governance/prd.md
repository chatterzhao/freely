# PRD: pre-test-merge-responsibility-usage-and-lifecycle-governance

## Compatibility Note

- 历史 PRD/path 保留 `pre-test-merge` 命名，避免破坏既有引用。
- 当前 canonical 语义已经升级为 `test-pre-merge-*` 测试批次前缀族。
- 下文出现的 `pre-test-merge` 都按 `test-pre-merge-*` 前缀族理解。

## Problem

Freely 已经把 `pre-test-merge` 定位成临时预集成验证分支，但当前真源还没有把它的职责边界、允许操作、stale/retire 条件和 promotion 默认语义写成一致的治理定义，导致狗粮过程中不断出现：

- 把验证批次误当成事实主线
- 把旧批次拿来和新 `develop` 直接比较或回收
- 无法明确判断何时应 replay 来源 feature，何时可以继续保留当前批次

## Users

- manager-agent
- branch-management / worktree-maintenance / patrol related skills
- 在 Freely 中开发 Freely 的 human/operator

## Goals

1. 把 `pre-test-merge` 的唯一职责写清。
2. 把允许/禁止操作写清。
3. 把 lifecycle stage 与 stale/retire/rebuild 信号写清。
4. 把 promotion 默认语义写清，避免再把批次快照误当成长期真相。

## Non-goals

1. 不在本 issue 中直接实现 runtime/status 的 batch freshness 能力。
2. 不在本 issue 中直接补所有 machine-readable 检测逻辑。
3. 不在本 issue 中处理某个具体 feature 的 merge 冲突。

## Acceptance shape

- 宪法、法律、branch-management、cleanup 和 patrol 真源的 wording 一致
- 规则允许 manager 明确判断：
  - 当前批次是否 still-valid
  - 是否必须 stale/retire
  - 是否应 replay 来源 feature
- follow-on capability issue 保持独立，不与本 issue 混 scope
