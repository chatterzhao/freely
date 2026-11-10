---
raw_id: raw-20261110T064015Z
status: brainstormed
created_at: 2026-11-10
---

# Brainstorms

## 前置评审：重做真源普查（issue 正文明确要求）

工位基于 `ab86c1b16`，已 merge develop `6715a67a2`（含 P0 #4272 的
`from __future__ import annotations`，本条的前置阻塞已解除）。在**目标文件上直接
grep 并交叉验证调用方**后，两面结论如下（两处立项假设被证伪/更正）。

### 面 1：派发非幂等 —— 成立，但根因与恢复点记载不同

真源链路（develop `6715a67a2`）：

```
runtime/freely:14162  a2a_task.py list --role worker --status submitted
                        | consume_worker_tasks.py | decode_worker_tasks.py   # R23.5 JSON Lines / NUL
runtime/freely:14234  a2a_task.py insert            # 建 pending handoff record
runtime/freely:14277  launch_worker_from_manager_prompt_if_needed(...)
runtime/freely:14282  a2a_task.py update --status launched --expected-status pending || true
runtime/freely:14286  a2a_task.py update --status working || true          # A2A task 侧无 CAS
```

- **更正一次普查结论**：`a2a_task.py:847` 用的是 `parser.parse_known_args()`，不是
  `parse_args()`。因此 `--expected-status` **不会让命令被拒**，而是被静默丢弃；
  `p_update` 参数表（`:730-739`）确实没有登记它。命令照常执行、状态照常改写，
  但 CAS 从未生效 —— 这比「命令被拒」更隐蔽，因为运维看到的是「更新成功」。
- `a2a_server.py:757` 的 PATCH 端点直接 `update_fields(task_id, **fields)`，没有
  `expected_state` 概念；`freely_db_manager.py:1149` 的 `a2a_task.update` 是无条件
  `UPDATE a2a_tasks SET ... WHERE task_id = ?`。**四层里没有任何一层有 CAS**。
- A2A task 侧的 `--status working` 在 worker 启动**之后**才写，且 `|| true` 吞掉
  失败。崩溃/并发时第二个派发器仍能从 `submitted` 列表里取到同一任务并再拉一个 worker。
- `handoff_store.assign` 只有测试调用方，不是派发真源（历史误判，本次再次确认）。

### 面 2：SSE 三重实例 —— 部分成立，一处关键假设被否掉

- **否掉「两个消费者同时注入同一条 `state_update`」**：`runtime/watchdog_sse.py:164-182`
  的 `_handle_sse_event` 第一行就是 `if state != "input-required": return`，它是
  **input-required 路由 + liveness/staleness 看护**，职责与 `sse-watchdog.sh`
  （`state_update` 写 JSONL 队列 + 注入 manager session）互补，不是重复消费者。
  **不能按 issue 正文的建议删掉「较弱的那个消费者」**，否则将丢失 input-required 路由。
- 真正仍然成立的是**启动路径与 pid 所有权**：
  - `freely:18983 launch_sse_watchdog` 同时 nohup 起 `sse-watchdog.sh --watch` 并调用
    `_start_watchdog_sse_py`（`:20832`）；
  - `freely:20853 cmd_ensure_sse_watchdog_watch` 外层 `while true` 里又
    `bash "$_sse_watchdog_sh" --project ... --watch --interval 10`，而 shell watchdog
    自身 `sse-watchdog.sh:166` 就是 `while true` —— **外层 sleep/重试是死代码**；
    它还把自身 `$$` 写进 `sse-watchdog.pid`，让 `valid_sse_watchdog_pid_for_project`
    永远看到「健康」，真正的 consumer 死了也不会被重启；
  - `freely:24789`（`ensure-sse-watchdog` 非 watch 模式）是第三条启动路径；
  - 三处 pid 写入都是裸 `echo ... > pid`（`sse-watchdog.sh:40`、`_start_watchdog_sse_py`
    的 `echo $! > pid`、`cmd_ensure_sse_watchdog_watch` 的 `echo "$$" > pid`），
    检查-写入无互斥，并发启动可互相覆盖。

## 方案方向

### 方向 A：四层贯通 CAS + 启动前抢占（选中）
1. `a2a_task.py` 登记 `--expected-state` / `--expected-status`（legacy 词表映射），
   update 分支透传并在 `state_conflict` 时 `sys.exit(3)`；
2. `a2a_server.py` PATCH 识别 `expected_state` / `expected_status`，`affected == 0`
   返回 409 `state_conflict`；
3. `freely_db_manager.py` 的 `a2a_task.update` 用单条
   `UPDATE ... WHERE task_id = ? AND state = ?` 完成原子 CAS（DB daemon 是单写者，
   无需额外事务协议 —— 沿用 R20 #4163 的边界）；
4. `runtime/freely` 在 `launch_worker_from_manager_prompt_if_needed` **之前**抢占
   `submitted → working`，抢占失败即 `continue`；删掉启动后的 A2A 状态写。
   三处既有 `--expected-status pending` 调用因此第一次真正生效。

选它的理由：只加「可选前置条件」，不改派发数据契约（R23.5 的 JSON Lines / NUL 流）、
不改 A2A 状态机词表、不改 `|| true` 的其它容错语义（那是 #4157/R25）。

### 方向 B：只在 shell 里用 `mkdir` 做任务锁（否决）
跨进程可行，但会引入与 DB 状态机不一致的第二套所有权，崩溃后需要额外回收逻辑；
且问题本就出在「状态更新没有条件」，B 只治标。

### 方向 C：把 python watchdog 删掉，只留一条链路（否决）
按前置评审，两者职责互补。删掉会让 input-required 路由与 session staleness 看护消失。
本轮改为「**监督者不消费、消费者只有一个**」：`cmd_ensure_sse_watchdog_watch`
只检查 pid 存活并调用唯一的启动入口 `launch_sse_watchdog`，不再嵌套启动 consumer。

### 方向 D：只在 pid 文件上加 `flock`，不动 watch-in-watch（否决）
互斥能挡住并发写，但挡不住「外层 while 永不可达」和「ensure 自己冒充 consumer pid」
这两个结构性缺陷。

### 方向 E：把 SSE 面拆成下一条 raw（否决）
与 R22/R23.5 的「4 面做 2 面」不同，本条两面同属「并发所有权」且共享同一套 AT 夹具；
再拆会把同一份真源普查与回归做两遍，也会留下一个「已关闭但两面只做一面」的半成品。
用户已明确不要无限拆 issue。

## 被否决
放宽 `test-all`、改 `|| true` 语义（#4157）、重写派发管线（R23.5 契约）、改
`SSEPool`（#4272）、动启动锁/DB 单实例（#4155）、删 `watchdog_sse.py`、拆新 raw。

## fidelity 基线

- RED 必须证明：CLI 未登记参数（PATCH body 无 `expected_state`）、409 冲突不 fail-closed、
  DB handler 第二次同样的 CAS 仍能改状态、派发 CAS 不在 launch 之前、
  watch-in-watch 与裸 pid 写仍在、并发 pid 认领没有独占所有者
  （基线连 claim helper 都不存在，两个进程都以 command-not-found 告终）。
- GREEN 必须证明：11 项静态接线 + 4 项隔离 SQLite 真实 handler + 3 项真实 CLI/stub
  REST + 2 项并发 pid claim 全绿；既有 10 个回归 + `test-materialize-h1` 全绿；
  `bin/test-all --ci` 实际执行新 AT。
- 2 项 RED PASS 必须是守卫（普通 update 仍工作、legacy `--status launched` 仍映射 working），
  不是新功能。

## 价值判定

- 不过时：develop 与安装态真源逐行核对，四面缺陷均在。
- 不重叠：#4155（启动锁/DB 单实例）、#4239（pkill 转义）、#4246（输入边界）、
  #4272（CLI 可加载）、#4157（可观测性）均不覆盖「状态条件更新 + watchdog 所有权」。
- 高价值（P1）：并发派发会重复拉起 worker 并重复改文件；SSE 重复消费者会重复注入
  manager prompt，均属静默正确性缺陷。
