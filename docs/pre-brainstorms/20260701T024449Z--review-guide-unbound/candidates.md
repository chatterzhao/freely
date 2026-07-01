---
candidate_id: C-20260701T024449Z-A
status: promoted
source_raw: raw-20260701T024449Z
created_at: 2026-07-01
milestone: M-20260701T024449Z-A
---

## C-20260701T024449Z-A: 修复 _review_guide 未定义变量

- candidate_format_version: v2
- title: 将 `$_review_guide` 替换为字符串字面量
- status: promoted
- decision_reason: 最简修复，一行改动，零维护负担
- next_action: B2 设计 → dev 应用修复 → test 验证
- revisit_trigger: N/A
- acceptance_criteria:
  - ACP 不可用时 pr-review-guarded 正常走完 manual_required 路径
  - 不再出现 `_review_guide: unbound variable` 错误
  - `set -euo pipefail` 下脚本正常退出
- promotion_gate: bash -n 语法检查通过，manual_required 路径不 crash
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-code
  - mode: subagent
  - summary: 确认 _review_guide 无其他引用，修复方案正确
  - verdict: pass
- promoted_issue_id: I-20260701T024449Z-A
- promoted_issue_path: docs/epics/pr-review-guarded/review-guide-unbound/raw-20260701T024449Z/issues/I-20260701T024449Z-A.md
- milestone: M-20260701T024449Z-A
- session_refs: []
