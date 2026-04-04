# Brainstorms - 20260403-1203--issue-id-key-repair

## Context

- 日期：2026-04-03
- 触发：`governance-merge-gate` 检测到 candidate 的 issue id key 不匹配问题
- 当前工位：`feature/issue-id-key-repair-20260403-1203`
- 父治理链：`feature/governance-chain-legacy-repair-20260403-1100`

## Current Repo Facts

1. `governance-merge-gate` 要求 candidate id 与 promoted issue 的 key 可追溯
2. 历史候选项存在 id/key 不一致，需要通过 `legacy_id_mapping` 显式补录映射
3. 本切片已批量补录 `legacy_id_mapping` 和部分 `next_action/revisit_trigger`，但尚未 materialize 对应 owner issue
4. 当前 pre-brainstorm 若继续声称 promoted 到不存在路径，会形成新的治理链失真

## Problem

- candidate 与 issue key 不一致会触发治理检查失败
- 子切片状态与产物不一致：文档声明 promoted，但分支内不存在该 issue 生命周期文件

## Boundary

- In scope:
  - 为历史候选补录 `legacy_id_mapping`
  - 补全 `needs_research/proposed` 候选的可执行字段
  - 将该子切片明确挂接到 `20260403-1100` 父治理链
- Out of scope:
  - 独立创建并推进 `issue-id-key-repair` 新 owner issue
  - 修改里程碑或 shared issue/progress 真源

## Proposed Route

1. 在 materialization 决策前，将本候选维持为 `needs_research`
2. 把修复结果作为父治理链的 evidence 子切片，不伪造独立 owner
3. 父链确定收口策略后，再决定 absorb 还是拆分成独立 issue

## Acceptance Criteria (candidate-level)

- 候选项满足 `candidate_format_version: v2` 最小字段质量线
- 不再引用不存在的 promoted issue 路径
- 与 `C-20260403-1100-A` 的父子关系和下一跳动作明确可追溯
