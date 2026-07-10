---
candidate_id: C-20260710T043521Z-A
status: promoted
source_raw: raw-20260710T043521Z
created_at: 2026-07-10
milestone: M-20260710T043521Z-A
---
## C-20260710T043521Z-A: scan skip closed items
- candidate_format_version: v2
- title: scan skip closed items
- status: promoted
- decision_reason: platform_state=closed + 无 platform_ids 的 items 已本地解决，不应进入 Manager AI cycle
- next_action: B2 实现
- acceptance_criteria:
  - scan items 从 ~690 降到 ~50
  - 11 corrupt 文件修正
- promoted_issue_id: I-20260710T043521Z-A
- promoted_issue_path: docs/B2-docs/runtime/scan/raw-20260710T043521Z/issues/I-20260710T043521Z-A.md
- milestone: M-20260710T043521Z-A
