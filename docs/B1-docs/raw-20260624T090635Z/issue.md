---
local_id: raw-20260624T090635Z35Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T090635Z-A
platform_ids:
  github:
    issue_id: '3417'
    url: https://github.com/chatterzhao/freely/issues/3417
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T09:06:52Z'
updated_at: '2026-06-24T09:06:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 目标
消除 tool-launchers.sh 中 adapter查询、launch_kind、ACP dispatch、tool family 解析的硬编码 case 分支，改为从 tool-registry.toml 读取。

## 要改的位置
- tool_supported_adapters() → read adapters.supported from registry
- tool_supported_launch_kinds_for_adapter() → read adapters.launch_kinds from registry
- tool_run_acp_from_prompt_file() → generalize claude/codex/opencode case branches
- _resolve_tool_family() fallback → scan registry aliases
- tool_supports_add_dir_boundary() → read launch.direct.add_dir_boundary from registry
- monitor-ai-acp.sh: remove hardcoded permission fallback case

## 关联
P1 (probe/boundary/resume) 和 P2 (ai-cli generic) 为后续阶段。
