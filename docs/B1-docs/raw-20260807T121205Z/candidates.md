---
candidate_id: C-20260807T121205Z-A
status: promoted
source_raw: raw-20260807T121205Z
created_at: 2026-11-26
milestone: M-20260807T121205Z-A
---

## C-20260807T121205Z-A: a2a-exit needs-review 更新必须携带 raw_key

- candidate_format_version: v2
- title: 修复 reviewer 路由 FAIL-CLOSED：a2a-exit 更新路径补 raw_key 并 fail-closed
- status: promoted
- design_verdict: bug
- anchor_refs:
  - contracts/coordination/contract.yaml:8「sse_topics」真源
  - docs/system/workspace/scripts/runtime/watchdog_sse.py:229「FAIL-CLOSED: missing raw_key for reviewer assign」
  - docs/system/workspace/scripts/runtime/a2a_task.py:1136-1140 漏传 raw_key 的更新调用
  - docs/system/workspace/scripts/tests/test-a2a-task-cli-loadable.py:63-64 AT 接线先例
- decision_reason: 根因是 a2a-exit 更新分支漏传 raw_key；最小修复在生产端，保留 watchdog 的 FAIL-CLOSED 不降级
- next_action: 进入 B2 物化 I-20260807T121205Z-A，写 pre-tests 并跑 RED
- revisit_trigger: 若 AT 在 develop 基线意外 PASS（说明 bug 已不复现），回 B2 重设测试设计
- acceptance_criteria:
  - 合法场景：任务记录含 raw_key 且 a2a-exit 更新为 input-required/needs-review:* 时，PATCH 字段含该 raw_key（SSE 事件携带）
  - fail-closed 场景：参数与任务记录均无 raw_key 时，a2a-exit 返回 ok:false 且不发出更新
  - 非 review 状态转换行为不变
  - AT 注册进 bin/test-all 的 CORE 与 CI_CORE
- promotion_gate: B0 判定为 bug；根因定位到 a2a_task.py 更新分支；AT 可独立验证 RED→GREEN
- open_questions: []
- acceptance_reviews:
  - reviewer: cli
  - mode: self-audit
  - summary: B0 锚点逐一核对，判定 bug 与 Option A 边界一致
  - verdict: pass
- promoted_issue_id: I-20260807T121205Z-A
- promoted_issue_path: docs/B2-docs/a2a/reviewer-agent/raw-20260807T121205Z/issues/I-20260807T121205Z-A.md
- milestone: M-20260807T121205Z-A
- session_refs: []
