---
candidate_id: C-20261126T130151Z-A
status: promoted
source_raw: raw-20261126T130151Z
created_at: 2026-11-26
milestone: M-20261126T130151Z-A
---

# Candidates

## C-20261126T130151Z-A: pr-merge 自动沿袭测试证据

- candidate_format_version: v2
- title: issue-sync commit 同步 test 工位后自动 attest-meta
- status: promoted
- design_verdict: 实现未完成
- anchor_refs:
  - `test-evidence.py:174`「Carry test evidence forward across metadata-equivalent commits」
  - `pr-merge-guarded:653-655`「git -C "$_test_wt" merge "$_src_branch"」
- decision_reason: 两轮实测 wt-close 因 chain 断裂判 stale，封装链缺一步；不改门禁判据。
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: 若 test-evidence 提供 lane 声明真源，改为读取声明而非默认值
- acceptance_criteria:
  - test 工位 merge 成功后调用 attest-meta，打印 from→to 回执
  - 敏感路径变化 / 无 gate 文件时不沿袭，打印明确重跑指引
  - 不吞错、不改 validate 判据、不放宽 wt-close
- promotion_gate: B1 §0 判定实现未完成，锚点 ≥2
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus
  - mode: main-agent
  - summary: 封装链缺一步，复用 #4703 既有 CLI，不引入第二判据。
  - verdict: pass
- promoted_issue_id: I-20261126T130151Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/issues/I-20261126T130151Z-A.md
- milestone: M-20261126T130151Z-A
- session_refs: []
