# Brainstorms - 20260403-1202--candidate-touched-repair

## Context

- 日期：2026-04-03
- 触发：`governance-merge-gate` 检测到 review 文件的 issue 引用字段不一致
- 当前工位：`feature/candidate-touched-repair-20260403-1202`
- 父治理链：`feature/governance-chain-legacy-repair-20260403-1100`

## Current Repo Facts

1. `governance-merge-gate` 会校验 review 元数据字段，历史文档里同时存在 `issue:` 与 `issue_id:`
2. 本分支已经批量修复了多份 review 文档字段命名，但尚未形成 issue/progress 生命周期锚点
3. 该问题属于 `20260403-1100` 的治理链修复子切片，不应独立伪装为已 materialized 的 owner issue

## Problem

- review 文档字段命名不统一会触发治理检查失败
- 当前 pre-brainstorm 文档过薄，且候选项声称已 promoted 到不存在的 issue 路径，生命周期表述失真

## Boundary

- In scope:
  - 统一 review 文档中的 issue 标识字段格式
  - 把该子切片回挂到 `20260403-1100` 父治理链
  - 在 materialize 前保持 candidate 为 `needs_research`
- Out of scope:
  - 独立创建并推进 `candidate-touched-repair` 新 owner issue
  - 修改里程碑编排与 shared issue/progress 真源

## Proposed Route

1. 保留本条作为 `20260403-1100` 的子问题候选，不单独宣称 promoted issue
2. 先在父治理链统一决定是 absorb 到单一 owner，还是拆成多个 milestone-owned issue
3. 待父链给出 materialization 决策后，再更新本候选状态与 issue 路径

## Acceptance Criteria (candidate-level)

- 当前候选字段满足 `candidate_format_version: v2` 最小质量线
- 不再引用不存在的 promoted issue 路径
- 明确 parent-child 关系与下一跳动作，不让子切片从里程碑视图里“消失”
