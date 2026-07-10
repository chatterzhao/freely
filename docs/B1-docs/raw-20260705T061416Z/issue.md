---
local_id: raw-20260705T061416Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T061416Z-A
platform_ids:
  github:
    issue_id: '3742'
    url: https://github.com/chatterzhao/freely/issues/3742
    synced_at: ''
  gitee:
    issue_id: IJYU6B
    url: https://gitee.com/zhaoquan/freely/issues/IJYU6B
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T06:14:37Z'
updated_at: '2026-07-05T17:30:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

1. ~~daemon 启动时 __manager__ 行用 agent_assign 无 slot → slot 列永远为空~~
   - **已于 M-20260703T080443Z-A 独立修复**（改用 acp_session_register + slot）
   - 不属于本 issue 的工作范围
2. dirty 提示中 \`freely-workflow-guarded-execution\` 的 backtick 被 bash 当命令执行
   - 根因：`docs/system/workspace/scripts/runtime/freely:21982` 双引号内 `\\` + 裸反引号触发命令替换
   - 修复：去掉反引号，改为纯文本

## 修复

1. ~~__manager__ 写入改用 acp_session_register~~ → 已在 M-20260703T080443Z-A 完成
2. dirty 提示中的 skill 引用去掉 backtick → 本 issue 实现
   - 文件：`docs/system/workspace/scripts/runtime/freely:21982`
   - 修改：`\\\`freely-workflow-guarded-execution\\\`` → `freely-workflow-guarded-execution`
