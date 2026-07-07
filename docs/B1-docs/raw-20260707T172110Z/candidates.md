---
candidate_id: C-20260707T172110Z-A
status: promoted
source_raw: raw-20260707T172110Z
milestone: M-20260707T172110Z-A
---
## C-20260707T172110Z-A: scan 修复
- status: promoted
- decision_reason: 修复 7 个缺陷，恢复 scan 检测能力
- promoted_issue_id: I-20260707T172110Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T172110Z/issues/I-20260707T172110Z-A.md
- acceptance_criteria:
  - scan --project 参数正确解析
  - 平台检测复用 platform-adapter
  - 平台查询复用 platform-adapter list_open_issues()
  - 1b_reopen 逻辑可达
  - extract_id 支持所有平台
  - 无 raw-{key} 平台 issue 被报告
  - agent_working import 正确
