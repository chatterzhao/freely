---
candidate_id: C-20260707T162123Z-A
status: promoted
source_raw: raw-20260707T162123Z
milestone: M-20260707T162123Z-A
---
## C-20260707T162123Z-A: per-platform ID close
- status: promoted
- decision_reason: close_issue/add_comment API 改为 platform_ids dict——每个平台用自己的 ID
- promoted_issue_id: I-20260707T162123Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T162123Z/issues/I-20260707T162123Z-A.md
- acceptance_criteria:
  - close_issue/add_comment 接受 platform_ids dict 而非单个 ID
  - wt-close 双平台 close（遍历 platform_ids）
  - scan Gitee 检测正常工作
  - 新平台只需在 issue.md 有 platform_ids 条目
