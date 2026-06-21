---
local_id: raw-20260521T132714Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2061'
    url: https://github.com/chatterzhao/freely/issues/2061
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T13:27:26Z'
updated_at: '2026-06-21T18:26:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-05-21T15:27:10Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
platform_state: closed
---

## 问题
daemon stop 只杀 AI pid、manager watchdog、interruption dispatcher，不杀 acp-bridge.py。
旧 bridge 变孤儿残留，新 daemon 无法正常重启。

## 根因
stop_project_runtime 没有记录/清理 ACP bridge 的 pid。

## 修复
1. 启动时把 bridge pid 写入 .freely/run/acp-bridge.pid
2. stop_project_runtime 读取并 terminate 该 pid
3. 参考 Zed AcpConnection 的 spawn → monitor → shutdown 模式
