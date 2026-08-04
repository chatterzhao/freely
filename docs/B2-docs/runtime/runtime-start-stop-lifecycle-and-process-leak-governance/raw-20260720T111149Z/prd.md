# PRD: DB daemon 存活监控与 task-mode 查询降级修正

## Goal

修复 freely-db daemon 无声退出后，task-mode 查询降级为 `wait` + 退出码 0 的缺陷，并让 Supervisor 感知 DB 控制面失效。

### 问题现状
1. DB daemon 无声退出（OOM/crash/WAL 损坏）→ db-daemon.log 无任何 trace
2. read_task_mode 三重重试全部失败 → 返回 `wait` + 退出码 0 → Supervisor 以为是权威数据库值
3. Supervisor 主循环无 DB health check → DB 死后继续以 running 状态空转
4. workcell-state 反映不实：DB 已死，报告 supervisor=up, reason=starting

### 目标状态
1. DB daemon 崩溃时 db-daemon.log 至少有 FATAL traceback
2. read_task_mode 查询失败返回错误 token + 非零退出码
3. Supervisor 每轮检查 DB 存活，不可用时尝试重启或写 `db_unavailable` 状态
4. ensure_freely_db 处理 stale PID 场景

## Solution

### 修改文件

#### 1. `docs/system/workspace/scripts/runtime/freely`

**改动 A: read_task_mode 故障语义修正 (L8793-8794)**

```bash
read_task_mode() {
  local project="$1"
  local cli="$SELF_ROOT/docs/system/workspace/scripts/runtime/freely-db-cli"
  local result _retry
  for _retry in 1 2 3; do
    result=$(python3 "$cli" --project "$project" task-mode.read-with-scan 2>/dev/null) && break
  done
  if [[ -z "$result" ]]; then
    log_error "task_mode DB query failed after 3 retries (freely-db daemon not ready or crashed)"
    echo 'error:db_unavailable'; return 1
  fi
  # ... rest unchanged ...
}
```

两处变更：退出码 `return 0` → `return 1`；输出 `echo 'wait'` → `echo 'error:db_unavailable'`。

**改动 B: Supervisor 主循环 DB health gate (L22958 前)**

```bash
# DB health gate: ensure freely-db is alive before reading task mode
if ! ensure_freely_db "$PROJECT_ROOT"; then
  log_error "freely-db daemon unreachable and restart failed; control plane degraded"
  write_workcell_state "$PROJECT_ROOT" "error" "up" "down" "db_unavailable"
  sleep 5
  continue
fi
```

插入在 `_pre_tm="$(read_task_mode "$PROJECT_ROOT")"` 之前。此 gate 也保护了所有后续 `read_task_mode` 调用。

**改动 C: ensure_freely_db stale PID 清理 (L8639 后)**

```bash
ensure_freely_db() {
  local project="$1"
  # ... existing vars ...

  # Quick health check
  if python3 "$cli" --project "$project" db.ping >/dev/null 2>&1; then
    return 0
  fi

  # Stale PID cleanup
  local pid_file; pid_file="/tmp/freely-db-$(python3 -c "
import hashlib,os
h=hashlib.sha256(os.path.abspath('$project').encode()).hexdigest()[:16]
print(h)" 2>/dev/null || true).pid"
  local socket_path; socket_path="/tmp/freely-db-$(python3 -c "
import hashlib,os
h=hashlib.sha256(os.path.abspath('$project').encode()).hexdigest()[:16]
print(h)" 2>/dev/null || true).sock"
  if [[ -f "$pid_file" ]]; then
    local old_pid; old_pid=$(cat "$pid_file" 2>/dev/null || true)
    if [[ -n "$old_pid" ]] && ! kill -0 "$old_pid" 2>/dev/null; then
      log_warn "stale freely-db PID $old_pid (process gone), cleaning up"
      rm -f "$pid_file" "$socket_path"
    fi
  fi

  # ... rest of start logic unchanged ...
}
```

#### 2. `docs/system/workspace/scripts/runtime/freely_db_manager.py`

**改动 D: start() 崩溃日志 (L426-431)**

```python
def start(self) -> None:
    try:
        self._open_db()
        self._ensure_tables()
        self.running = True
        self.uptime = time.time()
        self._run_socket_server()
    except Exception as e:
        import traceback
        self.log(f"FATAL: daemon crashed with {type(e).__name__}: {e}")
        self.log(traceback.format_exc())
        raise
```

**改动 E: _cleanup 信号日志 (L1620-1626)**

```python
def _cleanup(signum=None, frame=None):
    sig_name = signal.Signals(signum).name if signum else "EXIT"
    daemon.log(f"daemon received signal {sig_name}, stopping")
    daemon.stop()
    # ... rest unchanged ...
```

### 改动范围总结

| 文件 | 函数/位置 | 新增行 | 修改行 | 说明 |
|------|----------|--------|--------|------|
| freely | read_task_mode | 1 | 2 | echo wait→error:db_unavailable, return 0→1 |
| freely | supervisor loop | 6 | 0 | DB health gate |
| freely | ensure_freely_db | 15 | 0 | stale PID cleanup |
| freely_db_manager.py | start() | 4 | 0 | try/except + FATAL log |
| freely_db_manager.py | _cleanup | 2 | 0 | signal log |

总计 ~28 行新增，2 行修改。零依赖引入。

## Dev-Loop Handoff

1. 修改 `freely`：改动 A (L8793-8794)，改动 B (L22958 前插入)，改动 C (L8639 后插入)
2. 修改 `freely_db_manager.py`：改动 D (L426-431)，改动 E (L1620-1626)
3. 验证：pre-tests.md 4 个 acceptance items (AT-001～AT-004)
4. 无新增依赖、无配置变更
