---
b1_id: B1-20260720T111149Z
phase_state: completed
source_raw: raw-20260720T111149Z
source_url: https://gitee.com/zhaoquan/freely/issues/IK2DZE
produced_candidate: C-20260720T111149Z-A
created_at: 2026-07-20
---

# B1_IBM: DB daemon silent exit degrades task mode

## Input
- **来源**: Gitee IK2DZE / GitHub #4062，daemon start --task-mode auto 后 10-15s DB daemon 无声消失
- **证据**: db-daemon.log（无 crash trace）、daemon-launch.log、lifecycle-trace.log、workcell-state.env
- **涉及文件**: `docs/system/workspace/scripts/runtime/freely` (L8633-8665 ensure_freely_db, L8785-8803 read_task_mode, L22868+ supervisor loop), `docs/system/workspace/scripts/runtime/freely_db_manager.py` (L365-378 socket server loop, L426-440 lifecycle)

## Problem

### 问题域
freely-db daemon 在启动后 10-15 秒内**无声退出**（PID 消失、socket 无监听者、db-daemon.log 无 crash trace），导致：
1. task-mode get 查询失败后返回 `wait`（退出码 0），伪装成数据库权威值
2. Supervisor 对 DB 控制面失效完全无感知，继续保持 running/starting 状态驱动 AI

### 根因拆解

#### R1: read_task_mode 查询失败仍返回成功退出码
`read_task_mode()` (L8785-8803) 在 3 次重试全部失败后，输出 `wait` 并 `return 0`。调用方无法区分"DB 挂了降级为 wait"和"合法 wait 模式"。task-mode get CLI 命令调用此函数，得到 wait + 退出码 0 → 误以为这是权威数据库值。

#### R2: DB daemon 无声退出的三种可能路径
- **路径 A (最可能)**: Python 进程收到 SIGKILL（OOM killer / 系统资源压力），无信号处理器可用
- **路径 B**: `_run_socket_server` 的 `try/finally` (L365/375) 内部发生未捕获异常（如 `_handle_client` 中 `json.loads` 抛出的非 Exception 子类，或某个 C 扩展崩溃）
- **路径 C**: sqlite3 WAL 文件损坏导致 `sqlite3.connect()` 内部 abort

三种路径都不会经过 `SIGTERM`/`SIGINT` handler (L1628-1629) 的 `_cleanup()` → 不会写 "daemon stopped" 日志 → db-daemon.log 看不到退出痕迹。

#### R3: Supervisor 不监控 DB daemon 存活
- `ensure_freely_db()` (L8633-8665) 只在启动时检查一次，之后不再验证
- 主循环 (L22868+) 无 DB health check — 与 ACP bridge 不同（每轮 `_ensure_acp_bridge_running`）
- 心跳子进程 (L22681-22691) 只做日志轮转，不做 DB ping
- 当 DB daemon 挂掉后，唯一能发现问题的是 `read_task_mode`（它仍然返回 wait + 退出码 0 → 被静默吞噬）

#### R4: workcell-state 反映不实
DB 已死、Supervisor 在 wait 空转，但 workcell-state.env 仍报告 `supervisor=up, reason=starting`。没有 `db_unhealthy` 或 `control_plane_degraded` 状态。

## Brainstorm

### Option A: 查询层加固 + Supervisor 健康检查回路 (推荐)

**改动点**:
1. `read_task_mode` 查询失败时返回特殊错误 token（如 `error:db_unavailable`）或非零退出码；task-mode get CLI 透传错误
2. Supervisor 主循环中，在 `read_task_mode` 前加入 `ensure_freely_db` 调用（复用现有 db.ping 逻辑）
3. `ensure_freely_db` 改为可重入：如果 DB 活着直接 return 0；如果死掉尝试重启 daemon
4. DB daemon 不可恢复时，Supervisor 写入 workcell-state `control_plane_degraded` 并退出（不继续空转）
5. DB daemon 加入 catch-all 异常日志（在 `start()` 外层包 try/except，崩溃前至少留一行 traceback）

**优点**: 改动最小、复用现有 `ensure_freely_db`、不引入新组件
**缺点**: 重启 daemon 会丢失内存状态（当前无关键内存状态，可接受）
**风险**: 如果 DB daemon 反复崩溃→重启→崩溃，需要熔断

### Option B: 独立 DB watchdog 子进程

**改动点**:
1. 独立后台进程（类似 heartbeat subprocess），每秒 ping DB
2. DB 连续 N 次不响应 → 写 workcell-state `db_dead` → Supervisor 检测后退出
3. DB daemon 重启逻辑放在 watchdog 中

**优点**: 关注点分离、检测延迟更低
**缺点**: 多一个常驻进程、增加系统复杂度、与现有 heartbeat/logrotate 子进程功能重叠
**评估**: 过度设计——现有 heartbeat 子进程只需加一行 db.ping，无需独立 watchdog

### Option C: 仅加固 DB daemon 进程、不改变 Supervisor

**改动点**:
1. DB daemon 加 signal handler (SIGUSR1 等)、atexit 日志、catch-all 异常
2. 依赖日志事后排查，运行时行为不变

**优点**: 改动最小
**缺点**: 不解决根因——即使 daemon 写了 crash 日志，Supervisor 仍然盲飞。issue 的"查询失败仍返回成功"和"Supervisor 盲区"两个问题一个都没修
**评估**: 不可接受——只修症状不修根因

## Decision: Option A

**理由**:
- `read_task_mode` 返回成功但数据错误 → 这是数据完整性问题，必须修正
- Supervisor 感知 DB 存活是控制面基本要求 → 用现有 `ensure_freely_db` 机制，最小改动
- DB daemon 崩溃日志加固是防御层，不是修复层
- Option B 过度设计，Option C 不修根因

**具体实现**:

### 修复 1: read_task_mode 故障语义修正 (freely L8785-8803)
```bash
read_task_mode() {
  # ... retry loop ...
  if [[ -z "$result" ]]; then
    log_error "task_mode degraded to WAIT: DB query failed..."
    echo 'error:db_unavailable'; return 1  # ← 关键: 非零退出码 + 错误 token
  fi
  # ...
}
```
所有调用方 (`task-mode get` CLI、`_manager_auto_consume_workers`、`_pre_tm` gate check) 检查返回值或退出码。

### 修复 2: Supervisor 主循环加 DB health gate (freely L22959 前)
```bash
# Before task-mode gate, ensure DB is alive
if ! ensure_freely_db "$PROJECT_ROOT"; then
  log_error "freely-db daemon unreachable and cannot be restarted; control plane degraded"
  write_workcell_state "$PROJECT_ROOT" "error" "up" "down" "db_unavailable"
  sleep 5
  continue  # 让 operator 有机会介入，或 DB 自行恢复
fi
```

### 修复 3: ensure_freely_db 改为可重入 (freely L8633-8665)
当前逻辑已支持：先 db.ping → 失败则重启 daemon → 等待就绪。不需大改，只需确认在 daemon 已在运行但无响应时能正确处理（先尝试 SIGTERM 旧 PID → 重启）。

### 修复 4: DB daemon 崩溃日志防御 (freely_db_manager.py L426-431)
```python
def start(self) -> None:
    try:
        self._open_db()
        self._ensure_tables()
        self.running = True
        self.uptime = time.time()
        self._run_socket_server()
    except Exception as e:
        self.log(f"FATAL: daemon crashed: {e}")
        import traceback
        self.log(traceback.format_exc())
        raise
```

## Candidate
- candidate_id: C-20260720T111149Z-A
- status: promoted
- milestone: M-20260720T111149Z-A
