---
schema_version: '1'
local_id: raw-20261103T132622Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4155'
    url: https://github.com/chatterzhao/freely/issues/4155
    synced_at: ''
  gitee:
    issue_id: IKSPQC
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQC
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-03T13:26:22Z'
updated_at: '2026-11-04T07:44:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
---

# fix: 用 flock 替换启动锁与 DB 单实例约定

workflow_kind: fix

## 根因
并发安全靠 pid 文件 + 时间戳 + 「先检查后动作」，没有 flock / CAS / 租约；同一队列还存在两个派发器，DB daemon 也没有单实例约束。

## 证据
- 启动锁 TOCTOU：`freely:631-632` `mkdir` 成功后下一行才写 `state.env`；等待方在 `:538-541` 快照到 `state_file_missing` → `:711-722` 直接 `rm -rf "$lock_dir"`（无 age 校验、无 owner 校验）→ 两个 supervisor 都能过 `ensure_no_active_supervisor_conflict:22630`；锁在 `:22792` 就释放，而 pid 文件 `:22776` 之后、`launch_manager_watchdog:22830` 仍是**无锁区间**。
- DB daemon 无单实例：`freely_db_manager.py:1682-1690`（check-then-act，无 flock / O_EXCL）、`:370-376` 启动即 `unlink` 别人的 socket、`:1710-1718` `_cleanup` 删 pid/socket 不校验 owner → 孤儿 daemon 退出时删掉健康 daemon 的 socket，全项目 DB 不可用；`_generate_chat_id:358-368` 注释明确假设「单写者」。
- 派发非幂等：`freely:13509` 取 `submitted` → `:13530` 先启动 worker → `:13532` 再 `update --state working ... || true`（无事务、无租约、失败被吞）→ 崩溃后下一轮重复拉起第二个 worker。同队列还有第二个派发器（`:13920-13955` TSV 通道，带 `worktree_has_active_worker` 闸，`:13508-13548` 那条没有）。
- SSE 三重实例 + watch-in-watch：`launch_sse_watchdog:18732-18739` + `_start_watchdog_sse_py:20580` + `:20619-20626` 外层 `while true` 包内层 `while true`（`:20624,20626` 为死代码）；两个消费者同时向 manager 注入同一条 `state_update`（`sse-watchdog.sh:167`），`sse-watchdog.sh:40` 写 pid 无互斥。
- PID 复用：`freely:575-586` `kill -0` 成功即判 `active`，`:655` 只有 `age >= stale_secs` 才回收，无 cmdline / 启动时间校验 → 无关进程复用 pid 后 `freely start` 等 30s 后 `exit 1`，表现为「启动无原因失败」。

## 影响
单项目双控制面（状态文件互相覆盖、stop 只能杀一个、孤儿 supervisor）；DB 全停 30s → 5s 重试 → 再起第二个 daemon（自激）；worker 重复拉起。后果表现为「AI 行为怪异」而不是程序崩溃，现场很难定位。均为代码路径证实，未并发实测（报告 U1 / U2）。

## 修复方案
1. 启动锁改 `flock` 持有 fd 并继承给 supervisor 子进程；`state_file_missing` 分支要求 `age >= stale_secs` 才回收，回收前校验 owner_pid 与 cmdline。
2. DB daemon 用 `flock` 抢 pid_file；`_cleanup` 删文件前校验 pid 文件内容 == 自己；`_run_socket_server` 在 `bind` 之前先 `connect()` 探测存活 daemon，探测通则退出。
3. 派发改为 `update --state launching --claimed-by <pid>` 做 CAS，失败即跳过；删掉两条派发器中较弱的一条（`freely:13508-13548` 或 `:13920-13955` 二选一）。
4. SSE 只保留一条链路（删死代码 `:20624,20626` 或删外层循环），pid 写入加 flock。
5. `freely:8800` 的 `pkill -f` 前对 `$project` 做正则转义（与 #4156 同族）。

## 验收标准
- RED：背靠背启动两次 `freely start`（隔离临时项目），断言只有一个 supervisor 且第二个明确拒绝；当前可能两个都过（U1 窗口需实测）。
- RED：并发两次 `ensure_freely_db`（隔离环境），断言只产生一个 daemon 且只有一个 socket inode；当前可能双 daemon（U2）。
- GREEN：锁文件由 flock fd 持有；`grep -n 'rm -rf "$lock_dir"' freely` 的清理路径带 age + owner 校验。
- GREEN：`freely:13530` 「先启动 worker 后写状态」的顺序被 CAS 取代（启动前已完成状态抢占）。
- GREEN：同一队列只剩一个派发器调用点；`:20624/20626` 死代码已删。
