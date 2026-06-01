---
local_id: raw-20260429-1745
kind: raw
phase_state: absorbed
absorbed_into: I-20260429-1745-A
platform_ids:
  github:
    issue_id: '215'
    url: https://github.com/chatterzhao/freely/issues/215
    synced_at: '2026-05-05T14:19:41Z'
  gitee: {}
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-04-29T17:45:00Z'
updated_at: '2026-06-01T11:48:16Z'
intake_id: 20260429-1745-bash32-daemon-compat-fix
author: human
channel: chat
session_refs: []
platform_state: closed
---

macOS bash 3.2 兼容性修复：daemon 自检测自杀 + select_launch_kind pipefail 崩溃。

通过 chat 插话发现：`./bin/freely daemon start` 在 macOS 上无法正常启动。经 `bash -x` trace 定位到两个 bash 3.2 兼容性 bug：
1. `resolve_active_supervisor_pid_for_start` 中 daemon 进程自检测后自杀
2. `select_launch_kind` 中 `ls` 空 glob + `pipefail` 导致 shell 崩溃

## Comments
