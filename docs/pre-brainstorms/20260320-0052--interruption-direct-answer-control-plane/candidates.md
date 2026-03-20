# Candidates - 20260320-0052--interruption-direct-answer-control-plane

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260320-0052-A
- title: Runtime interruption dispatcher for direct-answer control queries
- problem: 高注意力的询问型插话会 durable 落盘，但主主管长循环不一定及时 claim，导致“看看后台 AI 进程在做什么”这类问题得不到即时响应。
- why_now: 这类询问正是人类插话体验的最敏感场景；若连这里都不能及时响应，human interruption 能力就还不算可用。
- acceptance_hint:
  - 主管仍然只有一个，不能演化成多主管
  - 新增独立 interruption dispatcher，只处理窄范围 answer-only control query
  - 这类插话不进入 pre-brainstorm / issue / worker delegation
  - 形成 resolution artifact，并把 intake 回写为 absorbed
  - 第一版至少支持“后台 AI 进程在做什么”这类查询
- priority: P0
- status: needs_research
- decision_reason: 范围已收紧到 runtime direct answer，可直接实现最小链路并用真实插话验证。
- promoted_issue_path: pending://issue-materialization
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
