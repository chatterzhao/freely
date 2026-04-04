# Brainstorms - 20260403-1000--external-issue-integration-and-self-evolution

## Context

- 日期：2026-04-03
- 触发：
  - Freely 的需求来源已经同时覆盖外部 issue、内部自举缺口与运行中发现的问题
  - 当前仓库里已有 candidate 草案，但缺少与之配套的 pre-brainstorm 收敛文档
  - 如果没有先定义 intake 与状态回写边界，后续会把“外部需求消化”与“Freely 自身演进调度”混成一条不稳定的大议题

## Current Repo Facts

1. `docs/pre-brainstorms/20260403-1000--external-issue-integration-and-self-evolution/candidates.md` 已经提出外部 issue 消化、状态同步、内部需求回流和调度策略四个候选方向
2. 当前 canonical 治理要求 pre-brainstorm 目录中的索引条目必须指向真实存在的 `brainstorms.md` 与 `candidates.md`
3. Freely 正处于研究优先的整合阶段，需求 intake、candidate 吸收和 GitHub/Gitee 状态同步仍属于高不确定性设计问题

## Problem

- 当前 `20260403-1000` 只有 candidate，没有与之对应的 brainstorm truth，导致：
  - `INDEX.md` 引用悬空
  - 门禁无法确认该预研目录是否真正 materialized
  - 候选 issue 缺少问题边界、选项空间与下一跳判断的统一前置上下文

## Scope Boundary

- In scope:
  - 定义外部 issue、内部需求与 Freely 自举发现的问题如何进入同一 intake 语义
  - 定义“来源 issue”和“内部里程碑 issue”的最小映射关系
  - 为后续 skill / runtime / governance 实现确定研究切分方式
- Out of scope:
  - 立即实现 GitHub/Gitee API 同步器
  - 在当前轮次直接确定最终的多平台协议抽象
  - 把该议题直接 materialize 成单一 mega-owner 并跳过研究拆分

## Option Space

### Option A：只处理外部 issue intake

- 优点：范围最小，容易先产出 GitHub/Gitee 扫描能力
- 缺点：无法解释 Freely 自举中发现的问题该如何回流，后续仍会出现双轨治理

### Option B：把外部 intake、内部回流、状态同步、调度策略一次性打包

- 优点：看起来完整
- 缺点：议题跨度过大，会把研究、治理和实现能力耦合在一起

### Option C：先统一生命周期语义，再拆成可吸收的候选方向

- 优点：能先澄清 intake / mapping / sync / scheduling 四类问题的边界
- 缺点：需要接受短期内是多 candidate 并行收敛，而不是单 issue 直推实现

## Route Decision

- 采用 Option C
- 当前 `20260403-1000` 应作为 research umbrella，先承接以下候选方向：
  - 外部 issue 消化与候选 issue 闭环流程
  - GitHub issue 扫描与状态同步能力
  - 内部需求回流机制
  - Freely 自身迭代与用户项目开发调度策略

## Acceptance Targets (Pre-Brainstorm)

- 明确外部来源 issue、内部里程碑 issue、内部候选 issue 三者的角色边界
- 明确哪些问题属于治理真相，哪些问题属于 runtime/skill 能力实现
- 保持研究阶段拆分，不提前承诺最终 API、平台覆盖或调度架构

## Open Questions

1. 来源 issue 与内部里程碑 issue 的映射关系，应优先保存在文档真相、runtime 状态还是外部平台 comment/label 中？
2. Freely 自举发现的问题，何时必须同步回公开 issue，何时只保留内部治理痕迹？
3. intake/sync/scheduling 三类能力应该拆成多个 issue，还是由单一 umbrella owner 吸收后再分发实现？
