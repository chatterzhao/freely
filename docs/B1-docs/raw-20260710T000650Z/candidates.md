---
candidate_id: C-20260710T000650Z-A
status: absorbed
source_raw: raw-20260710T000650Z
absorbed_into: I-20260710T000650Z-A
milestone: M-20260710T000650Z-A
---

## C-20260710T000650Z-A: pre-scan-fix + scan raw_key fallback

- candidate_format_version: v2
- title: pre-scan-fix + scan raw_key fallback
- status: absorbed
- decision_reason: 636 个 items 是纯本地文档，应脚本批处理不进入 scan；platform_ids 缺失时用 raw_key 回退匹配
- acceptance_criteria:
  - pre-scan-fix.sh 自动处理 terminal phase 本地文档
  - scan raw_key fallback 正确匹配平台 issue
  - scan items 从 685 降到 ~50
- promoted_issue_id: I-20260710T000650Z-A
- promoted_issue_path: docs/B2-docs/runtime/scan/raw-20260710T000650Z/issues/I-20260710T000650Z-A.md
- milestone: M-20260710T000650Z-A
