# 研究：context-compaction 分支收编与退休

## Context

- 日期：2026-03-19
- 触发：`feature/context-compaction-delegation-governance-20260318` 相对 `develop` 已落后较多，但仍保留一小块独有 continuity guard 能力。
- 当前事实：
  - `develop` 已经具备 token-efficient continuity 主线、manager/worker continuity 分流、trigger-owner 矩阵。
  - 旧分支真正独有的，只剩：
    - `previous_context_compacted`
    - `Continuity Guard`
    - 首跳 prompt 的 compact/continuity 提醒
    - 对应测试断言

## Problem

- 继续沿旧分支推进，会把已经过时的治理口径继续保留成第二真相。
- 直接删除旧分支，又会丢掉还值得保留的小能力。

## Decision

采用“收编独有能力，然后退休旧工位”：

1. 在新工位记录 salvage/retirement 预研与 issue。
2. 只收编旧分支独有的 continuity guard 小能力。
3. 不重复引入主线已具备的 continuity/rotation 设计。
4. 收编并验证后，退休旧 `context-compaction` worktree 与分支。

## Acceptance

- `develop` 吸收旧分支独有 continuity guard。
- 旧分支/worktree 完成 retirement。
