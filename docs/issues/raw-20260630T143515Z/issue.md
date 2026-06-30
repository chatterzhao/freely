---
local_id: raw-20260630T143515Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T143515Z-A
platform_ids:
  github:
    issue_id: '3663'
    url: https://github.com/chatterzhao/freely/issues/3663
    synced_at: ''
  gitee:
    issue_id: IJXXUD
    url: https://gitee.com/zhaoquan/freely/issues/IJXXUD
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T14:35:36Z'
updated_at: '2026-06-30T14:35:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
get_config 函数不存在，导致 cmd_init() 中平台检查和 _init_acp_tool_setup() config.toml 缓存读取失败。PROJECT_ROOT 在 init 上下文未设置。

## 修复
- L20045: get_config FREELY_REPO_PLATFORMS → python3 读 config.toml
- _init_acp_tool_setup: grep+sed → python3 reader (shell quoting 问题)
- PROJECT_ROOT → project（init 上下文只有 project 变量）

## 测试
- init from scratch: BLOCKED 提示（预期，无 config.toml 时平台检查无法通过）
- init with config: 4 工具从 config.toml 缓存命中，零搜索
- repeat init: 全走 config.toml 缓存
