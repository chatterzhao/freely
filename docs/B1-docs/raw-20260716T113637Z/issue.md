---
local_id: raw-20260716T113637Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T040152Z-A
platform_ids:
  github:
    issue_id: '3942'
    url: https://github.com/chatterzhao/freely/issues/3942
    synced_at: ''
  gitee:
    issue_id: IK1K1I
    url: https://gitee.com/zhaoquan/freely/issues/IK1K1I
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T11:37:00Z'
updated_at: '2026-07-16T11:37:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

manager_ai_stalled_without_runtime_progress() 只检查主 cycle log 的 mtime。
AI 执行 tool call 时输出全在 debug log (.debug.log)，主 log 不更新。
90 秒后被误判 stalled → recovery kill bridge/supervisor → writeback 永远没机会跑 → session-store 永远不更新 → 下次只能 fresh → 缓存命中率 0%。

## 修复

在 stall detection 中增加 debug log mtime 检查。
如果 debug log 在 threshold 内被更新过，说明 AI 正在活跃执行 tool call，不应判定为 stalled。## 修复

在 stall detection 中增加 debug log mtime 检查。
