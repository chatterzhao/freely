---
local_id: raw-20260531T125837Z37Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2371'
    url: https://github.com/chatterzhao/freely/issues/2371
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T12:58:53Z'
updated_at: '2026-05-31T12:58:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题
ensure-manager 通过 8 层 grace chain (L220-L240) + ai.pid 文件推断 supervisor 状态，存在竞态条件，导致 supervisor 被误杀、L240 死锁。

## 修复
1. supervisor 启动后台心跳进程，每 2s 更新 supervisor-heartbeat 文件
2. ensure-manager 移除全部 grace chain，仅检查心跳 mtime（120s 超时）
3. 心跳在 supervisor 等待 AI、构建 prompt 等阻塞期间持续更新
4. 移除 ai.pid 依赖进行 liveness 判断

## 效果
- ensure_manager_once: 147 行 → ~80 行
- grace chain: 8 层 → 0（仅心跳）
- L240 死锁：每次 1-2 轮必触发 → 0
