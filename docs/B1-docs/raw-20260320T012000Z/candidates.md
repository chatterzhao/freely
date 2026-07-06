# Candidates - 20260320-0120--interruption-manager-agent-triage

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260320T012000Z-A: legacy issue
- title: Interruption manager agent decides direct answer vs delegation
- problem: 当前 direct-answer dispatcher 已能快速处理少数控制查询，但仍偏规则机，不能代表“主管基于职责自主判断是否自己回答”。
- why_now: human interruption 的核心体验不是收件箱，而是第一跳判断质量；必须把这一步从硬编码提升为主管型 AI 决策。
- acceptance_hint:
  - dispatcher 只负责 watch / invoke / writeback
  - handler 负责判断 `manager_answer_*` 或 `delegate_general`
  - 决策依据是职责边界，不是话术穷举
  - “看看后台 AI 进程都在做什么”应被快速直答
  - 非直答问题至少要被及时 claim 并留待后续委派
- priority: P0
- status: absorbed
- adoption_type: supporting_evidence
- decision_reason: manager answer-vs-delegation triage 已进入 interruption handler、manager route 与 `I-20260321T192500Z` 的 canonical owner surface，不再单开平行 issue。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260320T012000Z-A/issue.md
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
