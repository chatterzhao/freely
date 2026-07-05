---
local_id: raw-20260517T023647Z
kind: raw
phase_state: completed
platform_ids:
  github:
    issue_id: '384'
    url: https://github.com/chatterzhao/freely/issues/384
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-17T02:37:04Z'
updated_at: '2026-05-17T02:40:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-17T02:40:22Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260517T023647Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260517T023647Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-17T02:36:47Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260517T023647Z`。实现前请用 `wt-create --raw-key 20260517T023647Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-17T02:36:47Z"
title: "supervisor 静默崩溃：set -e 导致 loop 中未保护命令失败时退出且原因丢失"

## 根因分析

supervisor loop（`while true; do ... done`）在 `set -e` 下运行。循环中有数百条命令，部分未用 `|| true` 保护。任一条返回非零 → bash 立即退出循环 → 用默认值 `LAST_WORKCELL_EXIT_REASON="supervisor_exit"` 执行清理。

证据：
- `supervisor_cleanup` 的 `exit_reason=supervisor_exit`（默认值，未被任何已知退出路径设置）
- `stop_requested=0`（不是外部 stop 信号）
- `desired_state=running`（supervisor 认为自己应该继续跑）
- 循环中 `write_workcell_state "running" "up" "down"` 后 supervisor 消失（在进入下一轮 AI launch 前崩溃）
- `loop.log` 中的 `Terminated: 15` 是父进程退出时子进程被系统带走

## 修复方案

在 supervisor loop 入口加 ERR trap：在任何命令因 `set -e` 失败时，捕获失败命令、行号、返回值，写入 `LAST_WORKCELL_EXIT_REASON`，然后安全退出。

```bash
trap 'LAST_WORKCELL_EXIT_REASON="set_e_exit_line_${LINENO}_rc_$?"' ERR
```

这样所有未来的静默崩溃都会被精确定位，且原因可追溯。

## 范围

`docs/system/workspace/scripts/runtime/freely`：`daemon_run` supervisor loop 入口处加 ERR trap。
