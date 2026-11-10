---
candidate_id: C-20261110T064015Z-A
status: promoted
source_raw: raw-20261110T064015Z
created_at: 2026-11-10
milestone: M-20261110T064015Z-A
---

# Candidates

被否决方案见 brainstorms.md（面 1 的根因更正、面 2 的假设否掉、方向 B/C/D/E）。

## C-20261110T064015Z-A: 派发状态抢占 CAS + SSE watchdog 单实例所有权

- candidate_format_version: v2
- title: 四层贯通 `--expected-state` CAS（CLI → A2A server → DB daemon）并在启动 worker 前抢占；SSE 监督者不消费、消费者用 flock 原子认领 pid
- status: promoted
- decision_reason: `a2a_task.py` 用 `parse_known_args()` 静默吞掉未登记的 `--expected-status`，而 server/DB 两层都没有条件更新，派发循环又在 worker 启动之后才写状态 → 同一 `submitted` 任务可被并发重复派发。SSE 侧三条启动路径 + watch-in-watch 死代码 + 三处裸 pid 写让并发实例互相覆盖。两者都是静默正确性缺陷。
- next_action: 建 AT-001（11 静态 + 4 DB 行为 + 3 CLI 行为 + 2 并发 pid）→ 基线 RED → 实现四层 CAS 与单实例所有权 → GREEN → 回归 → 门禁 PR。
- revisit_trigger: 若派发器改为多进程共享非 SQLite 存储，或 A2A 状态机新增中间态（如 `launching`），需重述 CAS 的期望态词表与 409 语义。
- acceptance_criteria:
  - RED：develop `6715a67a2` 基线 + 最终版 AT-001 → `2 ok / 18 failed`，两项 PASS 仅为守卫。
  - GREEN：AT-001 `20 ok / 0 failed`；真实 DB handler 第二次 CAS `affected=0`；真实 CLI 对 409 非零退出；两个并发 pid claim 只有一个成功。
  - GREEN：不改 R23.5 的 JSON Lines / NUL 流派发契约、不改 R19 的启动锁与 DB 单实例、不改 `|| true` 的其它容错语义、不删 `watchdog_sse.py` 的既有事件语义。
  - GREEN：10 个相关回归 + `test-materialize-h1` 全绿；`bin/test-all --ci` 实际执行新 AT。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 在目标文件（而非全仓 grep）逐层核对 `runtime/freely:14162-14300`、`a2a_task.py:730/847/902`、`a2a_server.py:757`、`freely_db_manager.py:1149`、`watchdog_sse.py:164-182`、`sse-watchdog.sh:40/166`、`freely:18983/20832/20853/24789`；确认 `parse_known_args()` 吞参数而非报错；确认 python watchdog 只处理 input-required，不能删；用 `git archive develop` 隔离基线跑最终版 AT 得到真实 RED；在文件副本上预演四层改动后才落盘。
  - verdict: pass
- promoted_issue_id: I-20261110T064015Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T064015Z/issues/I-20261110T064015Z-A.md
- milestone: M-20261110T064015Z-A
- session_refs: []
