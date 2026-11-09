---
candidate_id: C-20261103T132622Z-A
status: promoted
source_raw: raw-20261103T132622Z
created_at: 2026-11-09
milestone: M-20261103T132622Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261103T132622Z-A: 消除启动锁 TOCTOU 与 DB daemon 双实例

- candidate_format_version: v2
- title: 启动锁的 `state_file_missing` 回收必须先过 age 校验（堵 TOCTOU 窗口）、stale 回收前校验 cmdline（防 PID 复用）；DB daemon 用 `fcntl.flock` 抢 pid 文件、bind 前先 `connect()` 探测、`_cleanup` 校验 owner
- status: promoted
- decision_reason: 启动锁的毫秒级窗口会让两个 supervisor 都过门禁（状态文件互相覆盖、stop 只能杀一个）；DB daemon 无单实例会导致**全项目 DB 不可用**并自激（5s 重试再起一个）。两者后果是「AI 行为怪异」而非崩溃，现场无法定位，且 R20 #4163 以本条为前置。
- next_action: 建 AT-001（并发背靠背启动 + 并发 ensure_db 两组隔离夹具）→ 实现限制在 `acquire_project_start_lock_or_wait` 的回收判定 + `freez_db_manager` 的抢锁/探测/清理 → 并发实测 → PR。
- revisit_trigger: 若引入跨机器调度或共享存储（NFS）使 `fcntl.flock` 语义不可靠，需改为 lease/CAS 服务。
- acceptance_criteria:
  - RED：隔离临时项目背靠背启动两次 `freely start` → 当前可观测到第二个进程在第一个写 `state.env` 之前把它判成 `state_file_missing` 并 `rm -rf` 锁目录（AT 用可控窗口稳定复现）；修复后第二个必须等待或明确拒绝。
  - RED：并发两次 `ensure_freely_db`（隔离 HOME）→ 当前可产生两个 daemon / 第二个把第一个的 socket `unlink` 掉；修复后只有一个 daemon、一个 socket inode。
  - GREEN：`state_file_missing` 分支必须 `age >= stale_secs` 且无活跃进程才回收（`grep` 断言 + 行为断言双覆盖）。
  - GREEN：stale 回收前校验 `owner_pid` 的 cmdline，PID 复用不会被当成 active 无限等待。
  - GREEN：DB daemon 抢 `flock` 成功才 `bind`；`bind` 前 `connect()` 探测到存活 daemon 即退出；`_cleanup` 删除文件前比对 pid 文件内容 == 自己。
  - 不覆盖（拆独立 issue）：派发 CAS、SSE 单链路/死代码、`pkill -f` 转义。
- promotion_gate: AT-001 RED → GREEN + 并发实测 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复核 9 个证据点中 4 个在 develop 仍成立（`state_file_missing` 设置/消费点、5 处 `rm -rf "$lock_dir"`、db_manager 零 flock、`_generate_chat_id` 单写者注释）；实测 macOS 无 `flock` 命令、项目既有 `fcntl.flock` 范式在 `freely:1621-1650`；据此把 issue 的「flock fd 继承」改为「回收判定进 flock 临界区 + age/cmdline 校验」，并把 3 个正交面拆出。
  - verdict: pass
- promoted_issue_id: I-20261103T132622Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261103T132622Z/issues/I-20261103T132622Z-A.md
- milestone: M-20261103T132622Z-A
- session_refs: []
