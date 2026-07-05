# Candidates
## C-20260623T075200Z-A: ACP usage workaround
- candidate_format_version: v2
- title: ACP usage workaround — prompt_bytes estimation + cache_metrics token fields
- status: promoted
- decision_reason: ACP 外部依赖短期修不了，Freely 侧 workaround 提供估算数据。~10 行改动。
- next_action: B2_IBM → dev-loop → pr-create
- revisit_trigger: ACP 修复后升级为真实 usage 数据
- acceptance_criteria:
  - run-acp-prompt.py: usage 为空时 prompt_bytes/4 估算 input_tokens
  - freely: cache_metrics 加 estimated_input_tokens
  - [CACHE] 行不再全零（至少有 prompt_bytes 估算）
- promotion_gate: 语法验证通过
- open_questions: []
- acceptance_reviews: [reviewer: claude-opus-4.8 / mode: subagent / verdict: pass]
- promoted_issue_path: docs/issues/I-20260623T075200Z-A/issue.md
- milestone: M-20260623T075200Z-A
