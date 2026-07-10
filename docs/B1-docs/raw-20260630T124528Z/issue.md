---
local_id: raw-20260630T124528Z28Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T124528Z-A
platform_ids:
  github:
    issue_id: '3657'
    url: https://github.com/chatterzhao/freely/issues/3657
    synced_at: ''
  gitee:
    issue_id: IJXXDP
    url: https://gitee.com/zhaoquan/freely/issues/IJXXDP
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T12:45:49Z'
updated_at: '2026-06-30T12:45:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 背景

当前 Usage:
  freely init [--project <abs_path>] --intent <abs_file> --constitution <abs_file> [--ai <tool[:model][:mode]>] [--tool-adapter <adapter>] [--tool-adapter-policy <policy>] [--reasoning-effort <effort>] [--accept-default-autonomy] [--force] [--reason <text>]
  freely set-tool [--project <abs_path>] --tool <name> [--tool-adapter <adapter>] [--tool-adapter-policy <policy>]
  freely sync-tooling [--project <abs_path>] --source-project <abs_path>
  freely doctor [--project <abs_path>]
  freely security-review-brief [--project <abs_path>]
  freely chat [--project <abs_path>] (--issue <id> | --new-issue) [--urgent] <message>
  freely comment --issue raw-{key} <message>          (write comment to all platforms via adapter)
  freely comment --issue raw-{key} --file <path>      (write comment from file)
  freely tui [--project <abs_path>] [--once]
  freely intake chat [--project <abs_path>] (--issue <id> | --new-issue) [--urgent] (--message <text> | --message-file <abs_file>) [--author <name>] [--channel <name>]
  freely intake claim [--project <abs_path>] --intake-id <id> --claimed-by <name> --reaction <steer|followup|collect|interrupt|noise> [--classification <discovery|continuation|control|noise>] [--delegated-worktree <abs_path>] [--linked-artifact <path>]
  freely intake resolve [--project <abs_path>] --intake-id <id> --resolved-by <name> --reaction <steer|followup|collect|interrupt|noise> --resolution-file <abs_file> --absorption-target <target> [--status <delegated|absorbed|dropped>] [--classification <discovery|continuation|control|noise>] [--linked-artifact <path>] [--delegated-worktree <abs_path>]
  freely intake status [--project <abs_path>]
  freely ensure-manager [--project <abs_path>] [--watch] [--interval <seconds>]
  freely ensure-interruption-dispatch [--project <abs_path>] [--watch] [--interval <seconds>]
  freely ensure-sse-watchdog [--project <abs_path>] [--watch] [--interval <seconds>]
  freely auth-change-wake [--tool <name>] [--slot <slot>] [--reason <reason>]
  freely start [--project <abs_path>] [--task-mode auto|wait|listen|id:<scan-id>] [--force] [--reason <text>]
  freely daemon start [--project <abs_path>] [--task-mode auto|wait|listen|id:<scan-id>] [--force] [--reason <text>]
  freely task-mode set --project <abs_path> --task-mode auto|wait|listen|id:<scan-id> [--force] [--reason <text>]
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
  freely feedback --title <text> --body <text> [--severity P0|P1|P2]   (create raw issue on all configured repo platforms)
  freely issue-sync <args>...                   (delegate to bin/issue-sync)
  freely status [--project <abs_path>] [--view baseline|live|fleet|all]
  freely live-status [--project <abs_path>]
  freely fleet-status [--project <abs_path>]
  freely develop-push status [--project <abs_path>]
  freely develop-push attempt [--project <abs_path>]
  freely develop-push defer [--project <abs_path>] --reason <post_merge_acceptance|cleanup_followthrough|remote_delivery_hold> [--note <text>]
  freely develop-push clear [--project <abs_path>]
  freely wt-create [--raw-key <key>] [--source platform] [--skill <skill>] [--slug <slug>] [--base <branch>]
  freely pr-create-guarded [--title <title>] [--body <body>] [--base <branch>]
  freely pr-merge-guarded <target-branch> <source-branch> [--dry-run]
  freely pr-merge-guarded complete <target-branch> <source-branch>
  freely wt-close <branch> [--force] [--skip-platform] [--discard-unmerged] [--reason <text>] [--dry-run]
  freely stop [--project <abs_path>]

AI mode:
  auto  -> non-interactive, auto-approve (where supported)
  step  -> interactive/approval mode

Bypass gates (--force / --skip-platform / --discard-unmerged) require --reason:
  这些命令的 bypass 标志（--force、--skip-platform、--discard-unmerged）必须配合 --reason 使用。
  --reason 格式必须匹配正则: --reason "违规绕过门禁中，理由充分，是：<业务理由>"
  业务理由必须是真正的业务原因，不能是技术症状（如 phase_state 未 completed、连接超时等）。

  有效业务理由示例:
    ✅ "该功能确定放弃，不再继续实现此 raw issue"
    ✅ "该方案已被否决，未合并提交确认丢弃"
    ✅ "配置文件损坏无法修复，需重建初始化"
    ✅ "守护进程状态损坏导致无法正常调度，需强制重建运行时"
    ✅ "当前 AI 进程陷入死循环无法响应，需强制终止后切换模式"
    ✅ "IBM Completeness 维度不适用于本次纯文档修改"

  无效理由（技术症状，会被拒绝）:
    ❌ "phase_state 未 completed"
    ❌ "连接超时"
    ❌ "编译失败" 的 ACP 预检（line 20073-20132）只做存在性检查，不做下载。工具处理硬编码  vs ，opencode/cline 完全未处理。registry 里只有 codex 有下载配置，其他三种工具缺失。

## 要做什么

### tool-registry.toml
- 每个  新增  字段（唯一合法下载源）
- 每个  新增  字段（npm / github_release / cargo 等）
- claude: 
- codex: （保留现有字段，统一格式）
- opencode: （或 cargo/github）
- cline: 

### freely init
- 新增 ACP 工具准备步骤，循环 tool-registry 的每个 [tool] section
- 先搜系统已有安装（PATH、npm list、~/.cache）
- 未找到 → 提示用户确认下载（所有工具都需确认）
- 从 registry 的 download_url 下载，不硬编码任何工具名
- 下载完成后写入 config.toml 记录路径
- 后续 runtime 从 config.toml 读路径

### ensure-codex-acp
- 改为通用 ，接受 tool 参数
- 或废弃，逻辑直接集成到 freely init
