---
local_id: raw-20260626T075106Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3542'
    url: https://github.com/chatterzhao/freely/issues/3542
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T07:51:26Z'
updated_at: '2026-06-26T07:51:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T075106Z-A
source_candidate: docs/B1-docs/raw-20260626T075106Z/candidates.md#C-20260626T075106Z-A
---

## 问题

`_resolve_tool_family` 及其关联函数（`_tool_session_dir`、`tool_uses_claude_session_id`、`tool_prefers_explicit_resume_target` 等）通过硬编码 `case` 语句匹配工具名。增加第 5 个工具（如 cline）需要改代码，不符合 registry 单一数据源原则。

## 当前硬编码位置

- `_resolve_tool_family`: binary → family 映射（缺 cline）
- `_tool_session_dir`: family → session 目录（缺 cline）
- `tool_uses_claude_session_id`: 判断 UUID session ID 格式
- `tool_prefers_explicit_resume_target`: 判断 resume 行为
- `tool_supports_auto_same_tool_slot_recovery`: 同 tool slot 恢复

## 改造方向

registry 已有全部所需字段：
- `[tool].session.id_format` → 替代 `tool_uses_claude_session_id`
- `[tool].session.directory_template` → 替代 `_tool_session_dir`
- `[tool].acp.binary` + `[tool].launch.direct.binary` → 反向查找替代 `_resolve_tool_family`

改造后增加工具只需编辑 `tool-registry.toml`，零代码改动。

## 约束

- 不能删掉现有判断逻辑，只能改为从 registry 读取
- 未来工具可能有不同行为，registry 字段要能表达差异
