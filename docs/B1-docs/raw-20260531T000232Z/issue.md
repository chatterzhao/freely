---
local_id: raw-20260531T000232Z32Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2346'
    url: https://github.com/chatterzhao/freely/issues/2346
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-31T00:02:46Z'
updated_at: '2026-06-17T00:24:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

1. dead tool 机制从未工作——db manager 进程自 May 26-27 运行，May 28 的 tool_failure_log 表和处理函数未生效
2. cooldown 在长 AI cycle 中过期导致 fallback index 重置，永远切不到后面的工具
3. opencode 收到 429 后内部重试不返回错误，900s idle timeout 期间 stall watchdog 要求 bridge 已死才触发——bridge 活着但 AI 完全不产出

## 修复

1. cooldown 取消 index-reset：始终单调前进，dead 机制单独防 ping-pong
2. _tool_test_resurrect: perl alarm 30s 强制结束，say hi 测试，不管什么原因失败都不滑出
3. stall watchdog: 去掉 bridge-dead 前提——debug log 120s 无变化就 kill child
