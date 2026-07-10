---
local_id: raw-20260617T090408Z08Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260617T090408Z-A
platform_ids:
  github:
    issue_id: '2906'
    url: https://github.com/chatterzhao/freely/issues/2906
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T09:04:24Z'
updated_at: '2026-06-17T15:17:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T15:17:56Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
platform_state: closed
---

## 问题

Manager 每次 delegate_workers 周期， 字段恒为 ：



故障链：
1. Manager ACP session/prompt → AI 调用 a2a-exit → 创建 A2A Task + worker prompt 文件
2. a2a-exit 没有正确填充  到 exit_contract DB
3. Freely runtime L12821  → 返回 "none"
4. L14689  检查失败
5. Worker ACP session 永不启动 → Manager 重新进入 prompt → 再次 delegate_workers → 死循环

## 根因分析

ACP 与 A2A 的桥接断裂。正确的配合模式：
- Manager ACP session/prompt → 产出 worker prompt 文件
- a2a-exit → 创建 A2A Task（submitted），写入 exit_contract（含 worker_prompts_csv）
- Freely runtime → 读 exit_contract → 启动 Worker ACP session → Worker 通过 A2A 汇报状态

当前 exit_contract 写入/读取链路中， 没有被 a2a-exit 正确填充。

## 修复方向
1. 追踪 a2a-exit → exit_contract 的写入路径
2. 确保 worker_prompts_csv 被正确序列化到 DB
3. 确保 runtime  能正确读取
4. 验证 Worker ACP session 成功启动

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
  step  -> interactive/approval mode（exit_contract 读写）
- （a2a-exit handler）
- （exit contract 写入）
