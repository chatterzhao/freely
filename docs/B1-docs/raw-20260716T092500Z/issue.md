---
local_id: raw-20260716T092500Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3938'
    url: https://github.com/chatterzhao/freely/issues/3938
    synced_at: ''
  gitee:
    issue_id: IK1IV6
    url: https://gitee.com/zhaoquan/freely/issues/IK1IV6
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T09:25:23Z'
updated_at: '2026-07-16T09:25:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

agent_working 当前只记录 anchor UUID (本地追踪 ID)，不是 Claude/OpenCode 真实的 session ID。
真 session ID 在 AI cycle 完成后可从 cycle log 提取，但未写回 agent_working。
session-store writeback 使用 || true 静默吞错，导致 session-store 永远不更新。
daemon 下次重启时读不到有效 session ID → 被迫 fresh → 缓存命中率 0%。

## 修复

1. monitor-ai-acp.sh: AI cycle 完成后，将真实 session ID 写入 agent_working
2. 移除 || true 静默吞错
3. 支持多种 session ID 格式 (UUID v4, ses_xxx 等)
4. select_launch_kind 优先从 agent_working 读取 resume target
