---
local_id: raw-20260616T141507Z07Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2851'
    url: https://github.com/chatterzhao/freely/issues/2851
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T14:15:23Z'
updated_at: '2026-06-16T14:15:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 核心约定
slot 目录名 = .zshrc alias 名 = config.toml AI_TOOL 值，三者必须一致。目录命名规范: {tool}-{type}-{name}，其中 {type}=apikey(claude/opencode) | account(codex)。Freely 靠 -apikey- / -account- 前缀识别工具族，不可修改。

## Requirements
1. 创建 templates/ai-auth/claude-apikey-EXAMPLE/settings.json.example（model + env + permissions，API key 占位符统一用 your-apikey）
2. 创建 templates/ai-auth/codex-account-EXAMPLE/config.toml.example（model + sandbox + approval_policy + writable_roots，占位符用 your-apikey）
3. 创建 templates/ai-auth/opencode-apikey-EXAMPLE/settings.json.example（model + provider config，opencode API key 不在 settings.json 内需在注释说明）
4. 创建 templates/ai-auth/README.md（slot 体系总览、快速开始、命名约定图解、安全注意事项）
5. 创建 templates/ai-auth/zshrc-aliases.example（三种工具的 alias 格式）
6. freely init 释放 templates/ai-auth/ 到 .freely/ai-auth/ 并输出提示
7. 对齐现有 skill references（tool-config-matrix.md, auth-setup.md）加入交叉引用

每个 .example 文件头部必须有醒目的命名约定注释块。所有 API key 占位符统一用 your-apikey。
