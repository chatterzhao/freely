---
candidate_id: C-20261125T100958Z-A
status: promoted
source_raw: raw-20261125T100958Z
created_at: 2026-11-25
milestone: M-20261125T100958Z-A
---

## C-20261125T100958Z-A: feedback edit 平台发现 ids
- candidate_format_version: v2
- title: feedback edit 缺本地文档时按 raw key 从平台发现 ids
- status: promoted
- promoted_issue_path: docs/B2-docs/human/feedback/raw-20261125T100958Z/issues/I-20261125T100958Z-A.md
- milestone: M-20261125T100958Z-A
- decision_reason: 修改 raw issue 不等于实现它；edit 应与 wt-create 解耦，与 comment 一样是纯平台命令
- acceptance_criteria: 无本地文档时 edit --raw-key 可改平台单；不创建本地文件；空字段不覆盖；fail-closed
- promotion_gate: B0 判定为实现偏差
