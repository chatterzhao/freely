# Candidates - 20260308-0145--state-sync-and-session-evidence-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Candidates

### C-20260308T014500Z-A: legacy issue
- title: 状态联动、流程标识词典与 session evidence 传播治理
- problem: Freely 当前缺少统一的流程标识语义和状态联动矩阵，导致 milestone / issue / progress / recovery 容易不同步；同时 `session_refs` 没有从 pre-brainstorm 持续传播到 IBM 与 dev-loop。
- why_now: 这已经直接影响 Freely 吃自己的狗粮能力；如果 AI 不知道这些自定义流程标识的统一含义，它就只能凭猜测做状态更新。
- acceptance_hint: 1) `LAWS` 成为流程标识的唯一事实源；2) `milestones.md` 区分 IBM 与 dev-loop 的 `loop_stage`；3) candidate->issue->progress/recovery 的联动更新被写成硬规则；4) `session_refs` 统一要求 `tool/session_id/jsonl_path/role`；5) skills 统一引用该词典。
- priority: P0
- status: promoted
- decision_reason: 这是当前治理可信度和可恢复性的结构性缺口；不先补齐，Freely 继续自举只会积累更多“工作做了但状态没同步”的债。
- promoted_issue_path: `docs/B2-docs/ibm/state-sync-and-session-evidence-governance/issues/state-sync-and-session-evidence-governance.md`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- session_refs: [{tool: codex, session_id: "019ccaa2-2f48-7782-a713-7d6d6d325030", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
