---
candidate_id: C-20261124T072402Z-A
status: promoted
source_raw: raw-20261124T072402Z
created_at: 2026-11-24
milestone: M-20261124T072402Z-A
---

## C-20261124T072402Z-A: 更正 governance check 文档断言

- candidate_format_version: v2
- title: workflow 注释与实现对齐——check 恒 in_progress 是网页拦截设计态
- status: promoted
- design_verdict: 设计正确、实现正确、文档断言错误
- anchor_refs:
  - `.github/workflows/pr-merge-guard.yml:3`「Only pr-merge-guarded sets it to "success" via GitHub API」
  - 同文件 `:4`「Result: GitHub UI merge button is greyed out」+ `:33-35`「NEVER the GitHub Merge button」
  - `pr-merge-guarded:749`「gh pr merge does NOT work. Use local merge」+ `git push develop`
  - CI run 45346477702 check 实测 in_progress + 分支保护实测 protected=true
- decision_reason: Option B。原 P0 功能断言已被证伪；保留文档修正子问题可防止同类误判重复。
- next_action: B2 物化 I-*；更正 workflow 注释第 3 条，补静态 AT 锁定「注释不声称置 success」与「无自签调用」。
- revisit_trigger: 若未来设计改为由 CI/App 在验证通过后置 success（并保留网页拦截），重新评估本 candidate。
- acceptance_criteria:
  - workflow 注释不再声称 pr-merge-guarded 会置 check success
  - 注释明确 check 恒 in_progress 是拦截网页合并的设计态，合并走本地 pr-merge-guarded
  - 静态 AT 覆盖注释与实现一致性
  - 分支保护处于启用态且 pr-merge-guarded 本地链路不受影响（有证据）
- promotion_gate: B0 判定与 brainstorms §0 一致；无门禁绕过。
- open_questions: []
- acceptance_reviews:
  - reviewer: self-b1-audit
  - mode: structured-check
  - summary: 原断言经实测证伪；三方案对比后选文档修正；锚点引用原文，判定与 decision 一致。
  - verdict: pass
- promoted_issue_id: I-20261124T072402Z-A
- promoted_issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/issues/I-20261124T072402Z-A.md
- milestone: M-20261124T072402Z-A
- session_refs:
  - tool: codebuddy-agent
  - session_id: unavailable://current-session
  - jsonl_path: unavailable://current-session
  - role: worker
