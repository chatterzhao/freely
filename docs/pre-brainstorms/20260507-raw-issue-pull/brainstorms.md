# Brainstorms: Pull raw issues from platform to local docs/issues/

## Discovery

### 来源
- Raw issue: `raw-20260507T0600Z`
- GitHub issue #279 — zhaoquan
- created_at: 2026-05-07 06:00 UTC
- platform_state: open

### 问题陈述
从平台（GitHub/Gitee）拉取 raw issue 到本地 `docs/issues/` 目录的功能需要实现。当前平台上的 issue 无法自动同步到本地文件系统，导致本地治理流程无法消费平台来源的 issue。

### 当前状态
Raw issue 已确认，功能需求明确但未进入正式预研。需要设计平台到本地的拉取流程和存储格式。

### 价值与时效性判断
- 平台 issue 的本地化是 B1_IBM 流程的前提条件
- 当前大部分 issue 创建在 GitHub 上，但本地 `docs/issues/` 中缺乏对应条目
- 缺少此功能会导致平台与本地 issue 体系脱节，影响治理一致性

**结论**: 价值确认，进入 B1 预研流程。

## Status

discovery (needs B1 research)

## Next Action

complete B1 pre-brainstorm — 分析平台拉取的架构方案、与现有 issue-sync 体系的集成方式以及存储格式设计。
