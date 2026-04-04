# Brainstorms - 20260403-1201--implementation-decision-note-repair

## Context

- 日期：2026-04-03
- 触发：`governance-merge-gate` 对 legacy code-review 文档的 implementation decision note 字段进行强校验
- 上游关系：该项属于 `C-20260403-1100-A (governance-chain-legacy-repair)` 的子切片，不是独立 owner

## Current Repo Facts

1. gate 期望 implementation-bearing review 至少包含：
   - `decision`
   - `why_this`
   - `alternatives_considered`
   - `boundary_non_goals`
   - `residual_risk`
2. 历史 code-review 文档存在“仅有验证结果、缺少决策字段”的遗留形态
3. 当前仅有 pre-brainstorm 产物，没有 materialized issue/progress

## Problem

- 若直接把该切片标记 promoted 并指向不存在的 issue，会形成新的治理链断裂
- 若不明确字段边界，批量补录容易出现模板化空字段，无法提供真实决策证据

## Scope Boundary

- In scope:
  - 定义 legacy review decision-note backfill 的最小质量线
  - 约束补录方式，避免“空值占位即通过”
  - 准备让 `1100` 主线 owner 吸收执行
- Out of scope:
  - 放宽 gate 对 decision-note 的要求
  - 独立创建新 milestone/owner 体系绕开 `1100`
  - 修改 canonical milestone/issue/progress artifacts

## Route Decision

- 当前保持 pre-brainstorm，candidate 状态应为 `needs_research`
- 下一跳依赖 `1100` owner issue materialization，再决定 absorbed 执行或独立 promote

## Acceptance Targets (Pre-Brainstorm)

- 给出 decision-note 字段补录的最小质量定义
- 给出“可补录样本”与“必须回到 owner issue重写”的判定边界
- 完整补齐 candidate v2 字段与下一跳触发条件
