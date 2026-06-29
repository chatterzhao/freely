# Candidates

## C-20260629T025659Z-A: 统一 fix skill 治理顺序为 B1→B2→dev→test

- candidate_format_version: v2
- title: 统一 fix skill 与 feature skill 的 IBM 治理顺序
- status: promoted
- decision_reason: fix 的"治理后置"导致 pre-tests 形同虚设、TDD 无法落地、brainstorm 走过场。统一流程让文档治理在开发之前，真正保证质量
- next_action: 修改 6 个文件 → B2_IBM → dev → test → pr → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - fix skill 流程顺序改为 B1 → B2 → dev → test
  - 去掉 test-pre-merge cherry-pick 机制
  - fix 的 B1 保留根因分析要求
  - fix 的 B2 必须有 pre-tests
  - three-loop 真源文档同步更新
  - AGENTS.md 同步更新
- promotion_gate: 6 个文件修改完成，流程描述一致，门禁通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 fix 和 feature skill 的两个流程版本，确认统一方案正确
  - verdict: pass
- promoted_issue_path: docs/epics/fix-flow-unify/skill-refactor/raw-20260629T025659Z/issues/I-20260629T025659Z-A.md
- milestone: M-20260629T025659Z-A
- session_refs: []
