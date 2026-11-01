# pre-tests：讨论入口 + handoff

> B2 写入时 `red-green-status: pending`；RED 后改 `red`；GREEN 后改 `green`。

## Unit

### acceptance-CF-1：事件归一化

- requirement: issue comment / PR review / CI / chat 归一化为同一 schema，event_id 稳定
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- expected_output: `passed`，覆盖六类 source、actor、thread_key、event_id

### acceptance-CF-2：event_id 幂等

- requirement: 同一事件重复 collect 只落一行
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- expected_output: 两次 collect 后 count 不变

### acceptance-CF-3：准入

- requirement: source disabled/actor not allowed/bot/not addressed/duplicate 分别有 disposition/reason
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- expected_output: 五类拒绝原因可断言

### acceptance-CB-1：ownership 状态机

- requirement: new/active/completed/expired/cross-ticket/stop 的 owner 正确
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- expected_output: 六类场景断言通过

### acceptance-CB-2：handback 一次

- requirement: 同一 task 第二次 handback 拒绝；terminal 不复活
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- expected_output: 第二次返回 duplicate/rejected

### acceptance-CB-3：new/fork 发 message

- requirement: `acp_session_connect` 在 new/fork 后调用 prompt；message+role prompt 非空
- evidence_level: unit
- artifact_ref: `docs/system/workspace/scripts/runtime/agent_working.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-acp-handoff.py`
- expected_output: mock session/new、fork 各收到一次 prompt

### acceptance-CB-4：Reviewer 契约

- requirement: reviewer agent/watchdog/skill 三处指令一致：`a2a-exit --state completed --summary <json>`
- evidence_level: integration
- artifact_ref: `docs/system/workspace/agents/reviewer-agent.md`、`docs/system/workspace/scripts/runtime/watchdog_sse.py`、`docs/system/workspace/skills/freely-tdd-review/SKILL.md`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-reviewer-contract.py`
- expected_output: 三处文本/命令断言一致

## Integration

### acceptance-CF-4：scan 输出未读事件

- requirement: `task-lifecycle-scan.py --json` 含 `events.unread/by_source/latest`，且不影响旧字段
- evidence_level: integration
- artifact_ref: `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-scan-events.py`
- expected_output: JSON 有 events 段；无事件时为空

### acceptance-CF-5：真实 issue comment fixture

- requirement: #4070 两条真实评论归一化、去重、进 unread
- evidence_level: integration
- artifact_ref: `docs/B1-docs/raw-20261101T031502Z/research/ops/replay/intake_replay.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-scan-events.py`
- expected_output: 2 条事件、同 thread、unread=2

### acceptance-CB-5：handoff 双写/迁移

- requirement: 新表写入后旧 `a2a_tasks` 仍可查询；迁移不丢历史
- evidence_level: integration
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- expected_output: 新旧查询都能读到

## End-to-End

### acceptance-E2E-1：讨论到工单

- requirement: 真实 issue comment → events → scan → Manager prompt；不新开重复 issue
- evidence_level: e2e
- artifact_ref: `docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- expected_output: 一条事件、一个 task、owner 正确

### acceptance-E2E-2：new/fork 交接

- requirement: mock ACP new/fork 收到 task+role prompt；Reviewer verdict 可读
- evidence_level: e2e
- artifact_ref: `docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- red-green-status: red
- status: pending
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- expected_output: prompt 非空、verdict JSON 可解析

## Real-Environment

- real_environment_status: pending
- real_environment_reason: 待实现后在测试工位用真实 issue/PR 评论与 scan 验证；当前未跑。

## RED Evidence（2026-11-01）

| item | actual_RED_output | red_how |
| --- | --- | --- |
| CF-1/2/3 | `FAILED (failures=3)`；`missing module: .../discussion_events.py` | 模块未实现，归一化/幂等/准入全红 |
| CB-1/2 | `FAILED (failures=5)`；`missing module: .../handoff_store.py` | 三表/owner 未实现 |
| CF-4 | `FAILED (failures=1)`；`missing module: .../discussion_events.py` | scan summary 未实现 |
| CB-4 | `FAILED (failures=1)`；`不用 a2a_task.py / a2a-exit` 仍存在 | Reviewer 契约三处不一致 |
| CB-3 | `FAILED (errors=1)`；`missing _prompt_after_connect` | new/fork 后无 prompt helper |
| E2E-1 | `FAILED (failures=1)`；`missing module: .../discussion_events.py` | 端到端链路未实现 |

命令：逐文件 `python3 docs/system/workspace/scripts/tests/test-*.py`；全部返回非零。

## Execution Notes

- 所有测试先 RED，再实现；不得先写实现再补测试。
- 没有 worker state 的 `passed` 会被判 execution_missing；测试证据落 `verification/test-evidence/`。
