# Tasks: 消除启动锁 TOCTOU 与 DB daemon 双实例
- issue_id: I-20261103T132622Z-A
- pre_tests_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261103T132622Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复核 9 个证据点，确认 4 个在 develop 仍成立；实测 macOS 无 `flock` 命令、项目既有 `fcntl.flock` 范式（`freely:1621-1650`）。
- [x] T2: 写 AT-001（5 静态 + 4 启动锁 + 4 DB 并发），基线快照确认 RED `5 ok / 8 failed`。
- [x] T3: 新增 `project_start_lock_dir_age_secs_for_runtime` 与 `project_start_lock_pid_belongs_to_project_for_runtime`。
- [x] T4: `state_file_missing` 回收加 age 门槛；`active` 判定加 cmdline 校验（PID 复用）。
- [x] T5: DB daemon 在 fork 前 flock 抢 pid 文件、`bind` 前探测存活 daemon、`_cleanup` 校验 owner。
- [x] T6: GREEN `13 ok / 0 failed`；拆出 #4239（派发/SSE/pkill）并排进 goal。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6 | AT-001（Real-Environment） |
