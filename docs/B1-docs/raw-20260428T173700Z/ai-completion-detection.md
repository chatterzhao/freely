# AI 完成检测统一抽象

## 现状：两种模式检测方式不同

| 检测点 | direct 模式 | ACP 模式（当前） | ACP 模式（未来持久） |
|--------|-----------|----------------|-------------------|
| AI 进程 | `claude -p` → 退出 | `run-acp-prompt.py` → 退出 | `claude-agent-acp` → 常驻 |
| 完成信号 | 进程退出 + rc | 进程退出 + rc | ACP `session/prompt` 响应 |
| 存活检测 | `kill -0 $pid` | `kill -0 $pid`（同 direct） | 协议心跳 |
| Stall 检测 | debug log mtime + process state | 同 direct | 协议超时 |

**关键发现**：当前 ACP 实现中，`run-acp-prompt.py` 是每次新建 session → 发 prompt → 等响应 → 退出。所以客户端进程仍然退出，PID 监控仍然有效。server 进程（`claude-agent-acp`）常驻但不由 monitor 管理。

## 统一抽象

```bash
# _ai_is_running: 统一的 AI 存活检查
_ai_is_running() {
  local ai_pid="$1"
  if [[ "${AI_TOOL_ADAPTER:-direct}" == "acp" ]]; then
    # ACP: client process (run-acp-prompt.py) exits when done
    # Future: check ACP session state instead of PID
    kill -0 "$ai_pid" 2>/dev/null
  else
    # direct: check claude process
    kill -0 "$ai_pid" 2>/dev/null
  fi
}

# _ai_shows_liveness: 统一的 AI 活性检测（防 stall）
_ai_shows_liveness() {
  local project="$1" ai_pid="$2" cycle_log="$3" threshold_secs="${4:-90}"
  if [[ "${AI_TOOL_ADAPTER:-direct}" == "acp" ]]; then
    # ACP: check client process + debug log (same as direct for now)
    # Future: check ACP session heartbeat
    _ai_shows_liveness_direct "$project" "$ai_pid" "$cycle_log" "$threshold_secs"
  else
    _ai_shows_liveness_direct "$project" "$ai_pid" "$cycle_log" "$threshold_secs"
  fi
}
```

## 适配模式判断点

所有需要区分 direct/acp 的地方都通过 `AI_TOOL_ADAPTER` 判断：

```bash
case "${AI_TOOL_ADAPTER:-direct}" in
  acp)  _ai_completion_acp "$@" ;;
  *)    _ai_completion_direct "$@" ;;
esac
```

## 影响面

| 文件 | 函数 | 改动 |
|------|------|------|
| monitor-ai-cli.sh | while kill -0 $child_pid | 无改动（ACP client 也退出） |
| monitor-ai-cli.sh | exit $child_rc | 无改动 |
| freely | _ai_shows_liveness | 封装适配判断 |
| freely | manager_ai_stalled_with_pending_intake | 同上 |
| freely | select_launch_kind | ACP 模式不支持 resume（每次新 session） |
| freely | tool_launch_args | 已通过 adapter 区分 |
