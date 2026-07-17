---
local_id: raw-20260717T004721Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T004721Z-A
platform_ids:
  github:
    issue_id: '3949'
    url: https://github.com/chatterzhao/freely/issues/3949
    synced_at: ''
  gitee:
    issue_id: IK1L7Y
    url: https://gitee.com/zhaoquan/freely/issues/IK1L7Y
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T00:47:44Z'
updated_at: '2026-07-17T00:47:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 现象
每次 status / self-heal / reconcile 都对活着的 sse-watchdog 触发 startup_self_heal_stale_pid_cleared（误清 pid 文件）与 runtime-source reconcile 误杀。2026-07-16/17 事件日志中每个 supervisor 启动周期均出现。

## 根因
runtime/freely ~L3570：
  valid_sse_watchdog_pid_for_project() { local pid="$1" project="$2" ... }
所有调用方（runtime_pid_valid_for_role、reconcile_control_plane_processes_for_active_runtime、sse_watchdog_pid_for_project 等）都传 (project, pid)。参数反转后 pid_matches_project 拿项目路径当 pid 做 kill -0，恒失败 → 活进程永判 invalid。fe8df8be9（2026-06-23）引入。

## 修复
参数顺序对齐调用方约定（改函数签名为 project、pid），并补一条回归测试：对刚启动的 sse-watchdog，valid 判定必须为真。

## 影响
sse-watchdog 控制面真源持续被误清；fleet/live-status 无法看到 sse 状态；reconcile 每轮误杀活进程。
