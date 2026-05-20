# Brainstorms: Add --source required parameter to wt-create

## Discovery

### 来源
- Raw issue: `raw-20260507T0730Z`
- GitHub issue #244 — platform
- created_at: 2026-05-07T10:46:27Z
- platform_state: open

### 问题陈述
#233 设计了 wt-create 内部自动 scan+pull 流程（步骤 5-7），当前只完成了步骤 1-4：
- 已完成：解析参数、拼分支名、创建工位
- 未完成：查 scan 结果 + source_family 匹配、根据 source 调对应的 pull 方法
- 另外 chat-inbox 来源的 raw issue 物化后没有调 issue-sync create 补 platform_ids

### 当前状态
Raw issue 已确认，详细设计方案已在 issue 中描述，但未进入正式 B1 预研。

### 方案概要
为 `wt-create` 添加 `--source` 必填参数，支持 `chat-inbox` 和 `platform` 两种来源。完整 scan+pull 流程包括：参数校验、分支名拼接、scan 匹配验证、pull 物化、platform_ids 补齐、双工位创建。

### 价值与时效性判断
- `--source` 必填确保 AI 在调用 wt-create 前必须明确 issue 来源
- scan 匹配验证防止来源误判导致的工位创建错误
- platform_ids 补齐确保多平台一致性
- 此功能是 wt-create 完整工作流的关键一环

**结论**: 价值确认，进入 B1 预研流程。

## Status

discovery (needs B1 research)

## Next Action

complete B1 pre-brainstorm — 分析 `--source` 参数的验证逻辑、scan 匹配流程以及与 raw-issue-pull 的集成方案。
