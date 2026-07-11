---
local_id: raw-20260711T023009Z
kind: raw
phase_state: proposed
platform_ids:
  gitee:
    issue_id: IK0AZG
    url: https://gitee.com/zhaoquan/freely/issues/IK0AZG
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-11T10:30:44+08:00'
updated_at: '2026-07-11T10:30:44+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 问题

three-loop-lifecycle.svg 多处与当前实现不一致：
- Worker skills: fix-execution 已不存在，缺少 test-RED/test-execution
- Manager skills: 引用不存在的 milestone-planning, auto-loop-orchestrator
- ACP timeout: 900s → 实际 180s
- 单 ACP Bridge → 实际 per-tool (claude/opencode/cline)
- 缺少 Reviewer Agent role 框
- 缺少 A2A Server 实体标签
- 缺少 SSE/watchdog/agent-working 数据流
- session/fork 流程未体现

## 修复原则
以实现为准。对齐 agent-roles.toml 的 skill 注册。
统一使用 freely-workflow-guarded-execution 替代旧 fix/feature skill。
补充 per-tool bridge、A2A SSE、session/fork 链路。

## 验收
SVG 中所有 skill 名与 agent-roles.toml 一致
ACP 超时标注 180s
per-tool bridge 架构正确展示
