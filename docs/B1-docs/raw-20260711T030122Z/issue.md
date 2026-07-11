---
local_id: raw-20260711T030122Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3879'
    url: https://github.com/chatterzhao/freely/issues/3879
    synced_at: ''
  gitee:
    issue_id: IK0B8Z
    url: https://gitee.com/zhaoquan/freely/issues/IK0B8Z
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-11T03:01:43Z'
updated_at: '2026-07-11T03:01:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

三个 agent 文档风格不统一:
- manager-agent.md 已重构（身份优先、工具箱统一、判断链清晰）
- worker-agent.md 仍是旧格式（机械式、skill 重复列举、缺少自主问题解决指引）
- reviewer-agent.md 技术细节充足但结构与其他两个不统一

## 修复

1. worker-agent.md: 身份优先 + 统一工具箱 + 明确边界 + gate 处理指南
2. reviewer-agent.md: 结构对齐 manager 新版风格（保持原有技术细节）
3. 三文档统一: 身份→职责→工具箱→工作方式→边界→与其他 Agent 交互
