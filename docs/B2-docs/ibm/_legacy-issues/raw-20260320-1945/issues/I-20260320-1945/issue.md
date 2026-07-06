---
local_id: I-20260320-1945
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260320-1945/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '29'
    url: https://github.com/chatterzhao/freely/issues/29
    synced_at: '2026-04-27T11:14:37Z'
  gitee:
    issue_id: IJFO5P
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5P
    synced_at: '2026-04-27T13:14:21Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md
last_synced_comment_at:
  github: '2026-04-27T11:14:37Z'
hash: ''
created_at: '2026-04-27T11:14:37Z'
updated_at: '2026-04-27T11:14:37Z'
platform_state: closed
---

Freely 已经有 runtime watchdog、manager continuity、interruption intake 和 fleet supervision，但还没有一个统一的“当前态控制面”。

结果是：

- 进程活着但是否在推进不清楚
- 主管监督缺少 canonical current-state 入口
- 用户需要手工拼 `baseline-status + prompt + continuity + ps + jsonl`

canonical: docs/B2-docs/runtime/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md
