---
candidate_id: C-20261104T074512Z-A
status: promoted
source_raw: raw-20261104T074512Z
created_at: 2026-11-04
milestone: M-20261104T074512Z-A
---

# Candidates

## C-20261104T074512Z-A: freely-package 输出路径安全守卫

- candidate_format_version: v2
- status: promoted
- decision_reason: 删除动作发生在任何校验之前，且目标可由调用方任意指定；最小修复是在 rm 之前拒绝危险目标并限制默认输出根。
- next_action: 先写守卫测试（RED），再实现 refuse_dangerous_output，GREEN 后走 test-pre-merge。
- revisit_trigger: 若未来确实需要向仓库外目录打包，必须通过显式参数并提供 dry-run，而不是放开默认行为。
- acceptance_criteria:
  - `--output /`、`--output ~`、`--output ..` 在 rm 之前被拒绝，退出非零。
  - 输出不在 `$HOME/.freely/versions/` 下时默认拒绝，`FREELY_PACKAGE_ALLOW_OUTSIDE=1` 可放行。
  - 安全目标仍正常打包。
- promotion_gate: 单测 GREEN + test-pre-merge + governance gate
- open_questions: 是否增加 `--dry-run`（本 PR 不实现，留作后续）。
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research
  - summary: 逐行确认 rm 位于所有校验之前；空值已有兜底，故只处理 /、$HOME、.. 与白名单外路径
  - verdict: pass
- promoted_issue_id: I-20261104T074512Z-A
- promoted_issue_path: docs/B2-docs/runtime/package-output-guard/raw-20261104T074512Z/issues/I-20261104T074512Z-A.md
- milestone: M-20261104T074512Z-A
- session_refs: []
