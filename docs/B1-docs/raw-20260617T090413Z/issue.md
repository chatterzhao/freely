---
local_id: raw-20260617T090408Z13Z
kind: raw
phase_state: dropped
platform_state: closed
completed_at: '2026-08-07T06:00:00Z'
closeout_note: legacy raw closeout (platform closed)
platform_ids:
  github:
    issue_id: '2907'
    url: https://github.com/chatterzhao/freely/issues/2907
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T09:04:29Z'
updated_at: '2026-06-17T15:18:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T15:18:07Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 问题

A2A Server 已启用 SSE（， endpoint），但 freely runtime 的 Manager 仍然通过轮询  获取 Worker 状态变更。

## 正确设计

A2A 协议规范的 SSE 模式：
1. Worker 状态变更 → A2A Server →  SSE 推送
2. Manager 通过  订阅 Worker task
3. Manager 收到  事件 → 触发下一步决策

当前 Freely 的实现：
- Manager 等待 Worker 完成：轮询 
- 无 SSE 订阅 → 延迟高、资源浪费

## 修复
1. freely runtime 的 Worker 等待逻辑：从轮询改为 SSE 订阅
2. Manager prompt 中增加"通过 A2A SSE 监控 Worker 状态"的指令
3. A2A Server SSE 断连重试（）

## 影响文件
- Usage:
  freely init [--project <abs_path>] --intent <abs_file> --constitution <abs_file> [--ai <tool[:model][:mode]>] [--tool-adapter <adapter>] [--tool-adapter-policy <policy>] [--reasoning-effort <effort>] [--accept-default-autonomy] [--force]
  freely set-tool [--project <abs_path>] --tool <name> [--tool-adapter <adapter>] [--tool-adapter-policy <policy>]
  freely sync-tooling [--project <abs_path>] --source-project <abs_path>
  freely doctor [--project <abs_path>]
  freely security-review-brief [--project <abs_path>]
  freely chat [--project <abs_path>] (--issue <id> | --new-issue) [--urgent] <message>
  freely tui [--project <abs_path>] [--once]
  freely intake chat [--project <abs_path>] (--issue <id> | --new-issue) [--urgent] (--message <text> | --message-file <abs_file>) [--author <name>] [--channel <name>]
  freely intake claim [--project <abs_path>] --intake-id <id> --claimed-by <name> --reaction <steer|followup|collect|interrupt|noise> [--classification <discovery|continuation|control|noise>] [--delegated-worktree <abs_path>] [--linked-artifact <path>]
  freely intake resolve [--project <abs_path>] --intake-id <id> --resolved-by <name> --reaction <steer|followup|collect|interrupt|noise> --resolution-file <abs_file> --absorption-target <target> [--status <delegated|absorbed|dropped>] [--classification <discovery|continuation|control|noise>] [--linked-artifact <path>] [--delegated-worktree <abs_path>]
  freely intake status [--project <abs_path>]
  freely ensure-manager [--project <abs_path>] [--watch] [--interval <seconds>]
  freely ensure-interruption-dispatch [--project <abs_path>] [--watch] [--interval <seconds>]
  freely auth-change-wake [--tool <name>] [--slot <slot>] [--reason <reason>]
  freely start [--project <abs_path>] [--task-mode auto|wait|listen|id:<scan-id>] [--force]
  freely daemon start [--project <abs_path>] [--task-mode auto|wait|listen|id:<scan-id>] [--force]
  freely task-mode set --project <abs_path> --task-mode auto|wait|listen|id:<scan-id> [--force]
  freely task-mode get --project <abs_path>
  freely daemon stop [--project <abs_path>]
  freely daemon status [--project <abs_path>]
  freely daemon logs [--project <abs_path>] [--follow] [--file runtime-events|lifecycle-trace|loop]
  freely restart [--project <abs_path>] [--all-projects]
  freely restore-work [--project <abs_path>]
  freely baseline-status [--project <abs_path>]
  freely security-review-brief [--project <abs_path>]
  freely task-source-scan [--project <abs_path>] [--json]
  freely task-scan [--project <abs_path>] [--json]
  freely raw-issue-pull --raw-key <key> [--project <abs_path>] [--target <dir>]
  freely feedback --repo <user/repo|url> --title <text> --body <text> [--severity P0|P1|P2]   (create raw issue on GitHub)
  freely issue-sync <args>...                   (delegate to bin/issue-sync)
  freely status [--project <abs_path>] [--view baseline|live|fleet|all]
  freely live-status [--project <abs_path>]
  freely fleet-status [--project <abs_path>]
  freely develop-push status [--project <abs_path>]
  freely develop-push attempt [--project <abs_path>]
  freely develop-push defer [--project <abs_path>] --reason <post_merge_acceptance|cleanup_followthrough|remote_delivery_hold> [--note <text>]
  freely develop-push clear [--project <abs_path>]
  freely wt-create [--raw-key <key>] [--source <platform|chat-inbox>] [--skill <skill>] [--slug <slug>] [--base <branch>]
  freely pr-create-guarded [--title <title>] [--body <body>] [--base <branch>]
  freely pr-merge-guarded <target-branch> <source-branch> [--dry-run]
  freely pr-merge-guarded complete <target-branch> <source-branch>
  freely wt-close <branch> [--force] [--skip-platform] [--dry-run]
  freely stop [--project <abs_path>]

AI mode:
  auto  -> non-interactive, auto-approve (where supported)
  step  -> interactive/approval mode
- 
