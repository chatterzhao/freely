# Brainstorms - 20260403-1200--verification-artifact-dir-repair

## Context

- 日期：2026-04-03
- 触发：`governance-merge-gate` 检测到 legacy issue 文档缺少 `verification_artifact_dir` 字段
- 上游关系：该项是 `C-20260403-1100-A (governance-chain-legacy-repair)` 的子切片，不是独立 owner 生命周期

## Current Repo Facts

1. `governance-merge-gate` 会校验 issue front matter 是否声明 `verification_artifact_dir`
2. 现有失败样本集中在历史 issue 文档，缺口形态是“issue 已有 review 目录但 front matter 缺字段”
3. 当前分支只有 pre-brainstorm 证据，没有 materialized issue/progress，可见它仍处于 pre-brainstorm 收敛阶段

## Problem

- 历史 issue 文档字段缺失会阻断治理检查
- 该缺口目前尚未绑定到一个正式的 issue/progress owner，因此不能把当前 candidate 直接标记为 promoted

## Scope Boundary

- In scope:
  - 为缺少字段且已存在 review 目录的 legacy issue 补录 `verification_artifact_dir`
  - 形成“字段值如何映射到 code-reviews 目录”的固定规则，供 `1100` 主线吸收
- Out of scope:
  - 放宽 `governance-merge-gate` 规则
  - 单独开新 owner issue 并脱离 `1100` 主线推进
  - 修改 milestone/issue/progress canonical artifacts（本切片当前不承载该权限）

## Route Decision

- 当前路由保持在 pre-brainstorm，candidate 状态应为 `needs_research`
- 进入下一环前提：
  - `1100` 主线先 materialize 出正式 owner issue
  - 本切片完成缺口清单与映射规则，并由 owner issue 决定吸收路径

## Acceptance Targets (Pre-Brainstorm)

- 产出可复查的缺口类型定义与样本
- 明确吸收边界：仅补字段，不改 gate 强度
- 在 candidate 中补全 v2 必需字段与下一跳条件
