---
local_id: raw-20260624T090635Z51Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T090651Z-A
platform_ids:
  github:
    issue_id: '3418'
    url: https://github.com/chatterzhao/freely/issues/3418
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T09:07:08Z'
updated_at: '2026-06-24T09:07:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 目标
将 probe 命令、resume_target 判断、capabilities/policy 默认值迁移为注册表驱动。

## 要改
- _cmd_switch_auto() probe → test_command
- tool_accepts_explicit_resume_target() → 从 session.cli.resume 推断
- tool_requires_explicit_resume_target() → 同上
- tool_default_capabilities/policy() → registry 可选字段

## 涉及
- ai-cli, tool-launchers.sh, tool-registry.toml

## 关联
P0 (adapter/ACP dispatch) 先决条件。
