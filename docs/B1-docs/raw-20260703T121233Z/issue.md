---
local_id: raw-20260703T121233Z33Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T121233Z-A
platform_ids:
  github:
    issue_id: '3709'
    url: https://github.com/chatterzhao/freely/issues/3709
    synced_at: ''
  gitee:
    issue_id: IJYP52
    url: https://gitee.com/zhaoquan/freely/issues/IJYP52
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T12:12:55Z'
updated_at: '2026-07-03T12:12:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bugs Found

### 1. freely stop 不清理子进程
执行 freely stop 后，watchdog_sse.py、sse-watchdog.sh、a2a_server.py、freely_db_manager 等子进程未被 kill。多次启停导致进程堆积（080443Z 工位积了 7 个 watchdog_sse.py）。

### 2. sse-watchdog.sh 无限重启循环
watchdog_sse.py 退出/崩溃时 sse-watchdog.sh 立即重启，不检查已有实例。多个实例同时运行，形成 restart storm。

### 3. ACP bridge 每次 cycle 重启
bridge tool changed (opencode-apikey-ds-flash-auto → opencode) — 配置里的 slot 全名与 registry 的 binary 名不一致，每个 cycle 都检测到变化并重启 bridge。

### 4. 多个 project root 的 daemon 同时运行
同一仓库下多个 worktree 各自启动 daemon，freely stop 只停了当前 project 的，其他 worktree 的遗留进程继续运行。

## Evidence
- 080443Z: 7 watchdog_sse.py + 1 sse-watchdog.sh 遗留
- 114618Z: 2 watchdog_sse.py + 1 sse-watchdog.sh + a2a_server + freely_db_manager
- develop: 2 watchdog_sse.py + 1 sse-watchdog.sh + opencode 进程
