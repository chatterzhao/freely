# Candidates

## C-20260506T1400Z-A: merge-guarded fix/* whitelist

- candidate_format_version: v2
- title: merge-guarded fix/* whitelist
- status: needs_research
- decision_reason: fix-execution skill 产出 fix/* 分支需要合法 merge 路径进入 test-pre-merge-*；merge-guarded 当前只允许 feature/* 和 hotfix/*，fix/* 被阻断
- next_action: 已 materialize 为 I-20260506T1400Z-A，进入 dev-loop 实现
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - validate_merge_direction 增加 fix/* case pattern
  - help text 增加 fix/* 到 allowed directions
  - pre-flight gate 增加 fix/* 支持
- promotion_gate: 三处修改完成且 pre-tests 全部 pass
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-sonnet-4.7
  - mode: inline
  - summary: 问题边界清晰，影响范围可控（仅三处 one-line change），不涉及合并纪律或 protected-branch 策略修改；pre-tests.md 已定义三层验收，直接 promote
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260506T1400Z-A/issue.md
- milestone: M-20260506T1400Z-A
- session_refs:
  - tool: claude-code
  - session_id: unavailable://wt-create
  - jsonl_path: unavailable://wt-create
  - role: worker
