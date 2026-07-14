---
local_id: raw-20260714T021808Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260714T021808Z-A
platform_ids:
  github:
    issue_id: '3900'
    url: https://github.com/chatterzhao/freely/issues/3900
    synced_at: ''
  gitee:
    issue_id: IK0UDN
    url: https://gitee.com/zhaoquan/freely/issues/IK0UDN
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-14T02:18:30Z'
updated_at: '2026-07-14T02:18:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

### 问题 1: daemon start --task-mode 不生效
用户传 --task-mode auto，cmd_daemon_start 正确写 DB，但 daemon-run 永远以 wait 启动。三处断裂：launch_project_runtime_daemon_or_fail 不接受 task_mode、daemon-run spawn 不传 --task-mode、start_project_runtime hardcode wait。

### 问题 2: watchdog 重启 listen 被误判为 auto
launch_manager_supervisor 只允许 auto|wait|id:*，listen 落入 fallback 改为 auto。

### 问题 3: watchdog 重启 fallback 应为 wait
line 18254 fallback 为 auto，应与 read_task_mode DB 查询失败返回值(wait)一致。

### 问题 4: AI_MODE 裸引用 crash
3 处 $AI_MODE 无守卫 (lines 22697/22719/24994)，set -u 下 crash 导致 AI 无法启动，表现为无限重启循环。

## 修复方案
1. 打通 task_mode 传递链：cmd_daemon_start → launch_... → daemon-run → start_project_runtime
2. launch_manager_supervisor 加 listen，fallback 改 wait
3. $AI_MODE → ${AI_MODE:-none}
