# Candidates

## C-20260623T162226Z-A: L0-L3 兜底死循环检测
- candidate_format_version: v2
- title: L0-L3 四层递进兜底死循环检测
- status: promoted
- decision_reason: SSE 和状态管理已修复主因，但缺安全网。#3381 设计中充分讨论，现在 SSE 实现后条件更精准。
- next_action: B2_IBM → dev-loop 实现
- revisit_trigger: N/A
- acceptance_criteria:
  - L0: 独立 TSV 窗口，300s 内 fresh>3 + worker_launched=0 → wait
  - L1: (exit_kind, worker_launched) 3轮相同+0 → 递进 hint→指令→listen
  - L2: 10min >20K tokens + 0 worker → listen（prompt_bytes 降级）
  - L3: 总 token >500K → wait + stop marker
  - 每层触发写 runtime event 含证据
- promotion_gate: brainstorms 完成 + acceptance review pass
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.8 / mode: subagent / verdict: pass
- promoted_issue_path: docs/issues/I-20260623T162226Z-A/issue.md
- milestone: M-20260623T162226Z-A
- session_refs: []
