# pre-tests：讨论入口 + handoff

> B2 写入时 `red-green-status: pending`；RED 后改 `red`；GREEN 后改 `green`。

## Unit
- acceptance_target: 事件归一化/准入/handoff 单元行为
- testing_layer: unit
- target_environment: feature-local worktree
- required_evidence: unittest OK + test-evidence/*.log
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-discussion-events.py，覆盖 CF-1/2/3。
2. 运行 test-handoff-store.py，覆盖 CB-1/2/5。
3. 运行 test-acp-handoff.py，覆盖 CB-3。
4. 运行 test-reviewer-contract.py，覆盖 CB-4。

### acceptance-CF-1：事件归一化

- requirement: issue comment / PR review / CI / chat 归一化为同一 schema，event_id 稳定
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- expected_output: `passed`，覆盖六类 source、actor、thread_key、event_id

### acceptance-CF-2：event_id 幂等

- requirement: 同一事件重复 collect 只落一行
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- expected_output: 两次 collect 后 count 不变

### acceptance-CF-3：准入

- requirement: source disabled/actor not allowed/bot/not addressed/duplicate 分别有 disposition/reason
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/discussion_events.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-discussion-events.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- expected_output: 五类拒绝原因可断言

### acceptance-CB-1：ownership 状态机

- requirement: new/active/completed/expired/cross-ticket/stop 的 owner 正确
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- expected_output: 六类场景断言通过

### acceptance-CB-2：handback 一次

- requirement: 同一 task 第二次 handback 拒绝；terminal 不复活
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- expected_output: 第二次返回 duplicate/rejected

### acceptance-CB-3：new/fork 发 message

- requirement: `acp_session_connect` 在 new/fork 后调用 prompt；message+role prompt 非空
- evidence_level: mock
- artifact_ref: `docs/system/workspace/scripts/runtime/agent_working.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-acp-handoff.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-acp-handoff.log
- expected_output: mock session/new、fork 各收到一次 prompt

### acceptance-CB-4：Reviewer 契约

- requirement: reviewer agent/watchdog/skill 三处指令一致：`a2a-exit --state completed --summary <json>`
- evidence_level: integration
- artifact_ref: `docs/system/workspace/agents/reviewer-agent.md`、`docs/system/workspace/scripts/runtime/watchdog_sse.py`、`docs/system/workspace/skills/freely-tdd-review/SKILL.md`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-reviewer-contract.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-reviewer-contract.log
- expected_output: 三处文本/命令断言一致

## Integration
- acceptance_target: scan events summary、真实 fixture、additive 迁移
- testing_layer: integration
- target_environment: feature-local / temp project
- required_evidence: integration unittest OK + evidence log
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-scan-events.py，覆盖 collect/summary。
2. 运行 test-handoff-e2e.py，覆盖真实 #4070 fixture。
3. 运行 test-handoff-store.py，覆盖 additive 迁移。

### acceptance-CF-4：scan 输出未读事件

- requirement: `task-lifecycle-scan.py --json` 含 `events.unread/by_source/latest`，且不影响旧字段
- evidence_level: integration
- artifact_ref: `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-scan-events.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-scan-events.log
- expected_output: JSON 有 events 段；无事件时为空

### acceptance-CF-5：真实 issue comment fixture

- requirement: #4070 两条真实评论归一化、去重、进 unread
- evidence_level: integration
- artifact_ref: `docs/B1-docs/raw-20261101T031502Z/research/ops/replay/intake_replay.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-scan-events.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-scan-events.log
- expected_output: 2 条事件、同 thread、unread=2

### acceptance-CB-5：handoff 双写/迁移

- requirement: 新表写入后旧 `a2a_tasks` 仍可查询；迁移不丢历史
- evidence_level: integration
- artifact_ref: `docs/system/workspace/scripts/runtime/handoff_store.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-store.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- expected_output: 新旧查询都能读到

## End-to-End
- acceptance_target: issue comment → events → task owner；new/fork → prompt
- testing_layer: end_to_end
- target_environment: temp project + mock ACP
- required_evidence: e2e unittest OK + evidence log
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-handoff-e2e.py，覆盖 comment→event→task owner。
2. 运行 test-acp-handoff.py，覆盖 new/fork prompt。

### acceptance-E2E-1：讨论到工单

- requirement: 真实 issue comment → events → scan → Manager prompt；不新开重复 issue
- evidence_level: e2e
- artifact_ref: `docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-e2e.py.log
- expected_output: 一条事件、一个 task、owner 正确

### acceptance-E2E-2：new/fork 交接

- requirement: mock ACP new/fork 收到 task+role prompt；Reviewer verdict 可读
- evidence_level: e2e
- artifact_ref: `docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- red-green-status: green
- status: passed
- test_command: `python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py`
- actual_output: OK (unittest)
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-e2e.py.log
- expected_output: prompt 非空、verdict JSON 可解析

## Acceptance Items

### acceptance-1
- id: CF-1
- requirement: 事件归一化覆盖六类 source
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- test_command: python3 docs/system/workspace/scripts/tests/test-discussion-events.py
- expected_output: OK
- actual_output: OK

### acceptance-2
- id: CF-2
- requirement: event_id 幂等
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- test_command: python3 docs/system/workspace/scripts/tests/test-discussion-events.py
- expected_output: OK
- actual_output: OK

### acceptance-3
- id: CF-3
- requirement: 准入 disposition/reason
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-discussion-events.log
- test_command: python3 docs/system/workspace/scripts/tests/test-discussion-events.py
- expected_output: OK
- actual_output: OK

### acceptance-4
- id: CF-4
- requirement: scan 输出未读事件 summary
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-scan-events.log
- test_command: python3 docs/system/workspace/scripts/tests/test-scan-events.py
- expected_output: OK
- actual_output: OK

### acceptance-5
- id: CF-5
- requirement: 真实 issue comment fixture 进 events
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-e2e.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py
- expected_output: OK
- actual_output: OK

### acceptance-6
- id: CB-1
- requirement: ownership 六类状态
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-store.py
- expected_output: OK
- actual_output: OK

### acceptance-7
- id: CB-2
- requirement: handback 一次/terminal 不复活
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-store.py
- expected_output: OK
- actual_output: OK

### acceptance-8
- id: CB-3
- requirement: new/fork 发 task+role prompt
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: mock
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-acp-handoff.log
- test_command: python3 docs/system/workspace/scripts/tests/test-acp-handoff.py
- expected_output: OK
- actual_output: OK

### acceptance-9
- id: CB-4
- requirement: Reviewer verdict 三处一致
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-reviewer-contract.log
- test_command: python3 docs/system/workspace/scripts/tests/test-reviewer-contract.py
- expected_output: OK
- actual_output: OK

### acceptance-10
- id: CB-5
- requirement: additive 迁移保留旧 a2a_tasks
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-store.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-store.py
- expected_output: OK
- actual_output: OK

### acceptance-11
- id: E2E-1
- requirement: 真实 issue comment 到 task owner
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-e2e.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py
- expected_output: OK
- actual_output: OK

### acceptance-12
- id: E2E-2
- requirement: new/fork+Reviewer verdict 可读
- surface_kind: e2e
- target_lane: premerge-integration
- promotion_gate: develop_merge
- evidence_level: integration
- status: passed
- red-green-status: green
- artifact_ref: docs/B2-docs/a2a/handoff/raw-20261101T031502Z/verification/test-evidence/test-handoff-e2e.log
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-e2e.py
- expected_output: OK
- actual_output: OK
## Real-Environment

- real_environment_status: pass
- real_environment_reason: temp project 写 discussion-events.json 和 freely.db，真实文件系统/SQLite 跑 collect 去重；见 test-evidence/real-environment.log。完整 scan 在 test-premerge 复验。

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
