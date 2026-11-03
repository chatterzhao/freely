# Tasks：交接运行时 P0 修复

| # | 任务 | 产出 | 依赖 | 验收 |
| --- | --- | --- | --- | --- |
| T1 [x] | 写 RED 回归测试 | `docs/system/workspace/scripts/tests/test-handoff-runtime.py` | 无 | AT-001/002/003 全 RED |
| T2 [x] | 修 `_do_new` 未定义名称 | `docs/system/workspace/scripts/runtime/agent_working.py` | T1 [x] | AT-001 |
| T3 [x] | 存活判定改 `session/ping` 三态 | `docs/system/workspace/scripts/runtime/watchdog_sse.py` | T1 [x] | AT-002/003 |
| T4 [x] | 回归既有测试 | `test-acp-handoff.py`、`test-handoff-store.py`、`test-scan-events.py` | T2/T3 | 全绿 |
| T5 [x] | 证据与门禁 | `verification/test-evidence/`、`governance-merge-gate --range develop..HEAD` | T4 [x] | 证据存在、gate 通过 |

## 顺序

T1 → T2/T3 → T4 → T5

## 非目标

- 不做 outbox、信封、owner 绑定（C-B）。
- 不改 `worker_NN` / `agent-table.toml` / SSE 传输。
