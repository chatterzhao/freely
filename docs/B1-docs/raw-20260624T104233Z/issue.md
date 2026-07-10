---
local_id: raw-20260624T104229Z33Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T104233Z-A
platform_ids:
  github:
    issue_id: '3427'
    url: https://github.com/chatterzhao/freely/issues/3427
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T10:42:50Z'
updated_at: '2026-06-24T10:42:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题
项目中多处仍写 "stop/start daemon" 作为测试方式，未指向 pre-tests.md。
之前改了 SKILL.md 和 AGENTS.md，但 wt-create 脚本、其他 skill reference、doc 等可能仍有残留。

## 修复范围
全项目搜索以下模式并改为"按 pre-tests.md 中的指导进行测试":
- stop/start daemon
- 启动 daemon
- 启动项目测试
- daemon start
- 其他暗示"测试=启动 daemon"的表述

排除：Freely 自举示例中明确标注为示例的 daemon 引用。
