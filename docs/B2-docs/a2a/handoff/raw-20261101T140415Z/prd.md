# PRD: 交接运行时 P0 修复

## 1. Goal

让 `acp_session_connect` 在**任何**新建会话路径（跨工具、resume 失败回退、无 manager 会话）都能把首条 handoff 消息送达；让 agent 存活判定不再用 `pgrep` 误杀健康会话。

成功标准：

- `_do_new` 不再有未定义名称；新会话收到 `[role:<role>]` + 原消息。
- `session/ping` 成功 → 不清绑定；明确 session 错误 → 清绑定并记 DEAD；bridge 不可达 → UNKNOWN，不清绑定。
- 既有 `test-acp-handoff.py`、`test-handoff-store.py`、`test-scan-events.py` 仍全绿。

## 2. 复现

```bash
python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py
```

修复前：`NameError: name 'message' is not defined`。
修复后：3 个用例通过。

## 3. 实现方案

### 3.1 `agent_working.py`

- 模块顶部增加 `import sys`。
- `_do_new(project, raw_key, role, agent_id, slot, base_tool, reason="", message=None)`。
- 两处调用改为传 `message=message`：
  - `acp_session_connect` 的 `resume failed` 回退；
  - `acp_session_connect` 末尾的 fallthrough。
- 行为不变：`force_new` 分支仍在 `session/new` 后立即 `_prompt_after_connect`。

### 3.2 `watchdog_sse.py`

新增：

```python
def _session_state(project, role, agent_id, session_id) -> str:
    """alive / dead / unknown via ACP session/ping."""
```

- `slot = _get_agent_slot(project, role, agent_id)`；`base_tool = slot.split("-",1)[0]`。
- `result = _acp_rpc(project, "session/ping", {"sessionId": session_id}, base_tool=base_tool)`。
- `None` → `unknown`；`result.get("error")` 且文本含 `session` → `dead`；其余 error → `unknown`；有 result → `alive`。

`_check_agent_liveness`：

- 用 `_session_state` 取代 `pgrep`。
- 仅 `dead` 时清绑定（`val=agent_id`），并记 `DEAD`；`unknown` 记 `UNKNOWN`，不动绑定。

### 3.3 测试

`docs/system/workspace/scripts/tests/test-handoff-runtime.py`：

- `test_new_session_prompts_first_message`：stub `_db_rpc`/`_acp_bridge_call`，调用 `acp_session_connect`，断言 `session/new` 后紧跟 `session/prompt`，且 prompt 含 `[role:worker]` 与原文。
- `test_session_state_alive_dead_unknown`：分别 stub `_acp_rpc` 返回 result / session error / None，断言三态。
- `test_liveness_keeps_alive_binding`：stub `_db_rpc` 返回一行带 session 的 worker，stub `_session_state=alive`，断言不产生清绑定 upsert。

## 4. 非目标

- 不做 outbox、不做信封、不改 `messages_json`。
- 不改 `worker_NN` 与 `agent-table.toml`。
- 不改 SSE 传输与重连策略。

## 5. Dev-Loop Handoff

- 改动文件：`docs/system/workspace/scripts/runtime/agent_working.py`、`docs/system/workspace/scripts/runtime/watchdog_sse.py`、`docs/system/workspace/scripts/tests/test-handoff-runtime.py`。
- 测试入口：`python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py`。
- 回归：`test-acp-handoff.py`、`test-handoff-store.py`、`test-scan-events.py`。
- 证据落点：`verification/test-evidence/`。
