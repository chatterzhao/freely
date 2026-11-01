# Tasks：讨论入口 + handoff

| # | 任务 | 产出 | 依赖 | 验收 |
| --- | --- | --- | --- | --- |
| T1 | 事件模块与 schema | `docs/system/workspace/scripts/runtime/discussion_events.py` | 无 | CF-1/2/3 |
| T2 | GitHub adapter comment/review/CI | `docs/system/workspace/scripts/sync/platform-adapter.py` | T1 | CF-5 |
| T3 | scan 接线 | `task-lifecycle-scan.py` 的 events 段 | T1/T2 | CF-4 |
| T4 | handoff 三表与所有权 | `docs/system/workspace/scripts/runtime/handoff_store.py` | T1 | CB-1/2/5 |
| T5 | new/fork 发 message | `agent_working.py` | T4 | CB-3 |
| T6 | Reviewer 契约统一 | `reviewer-agent.md`、`watchdog_sse.py`、`freely-tdd-review/SKILL.md` | T4 | CB-4 |
| T7 | E2E/证据 | `tests/test-handoff-e2e.py`、`verification/test-evidence/` | T1-T6 | E2E-1/2、Real-Environment |

## 顺序

T1 → T2 → T3（C-F 可先独立 GREEN）
T1 → T4 → T5/T6 → T7（C-B）

## 非目标

- 不做 webhook、完整 A2A RPC、UI。
- 不改 `freely` 20K 行单体；只加模块 + 最小接线。
