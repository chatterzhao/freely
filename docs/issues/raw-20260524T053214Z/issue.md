---
kind: raw
local_id: raw-20260524T053214Z
priority: P1
phase_state: absorbed
absorbed_into: I-20260524T053214Z-A
source: chat-inbox
created_at: '2026-05-24T05:32:14Z'
title: ACP session 生命周期接入 tool_switch_events
platform_ids: {}
primary_platform: github
updated_at: '2026-06-13T10:51:37Z'
platform_state: closed
---

## 摘要

Freely 运行时死锁——tool_switch_events 已实现但 ACP 路径未接入，导致 session 切换和 bridge 重启后无限循环。
