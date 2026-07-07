---
candidate_id: C-20260707T172110Z-A
status: absorbed
source_raw: raw-20260707T172110Z
milestone: M-20260707T172110Z-A
---
## C-20260707T172110Z-A: scan 修复
- status: absorbed
- decision_reason: argparse + 复用 platform-adapter + 修复 7 缺陷
- promoted_issue_id: I-20260707T172110Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T172110Z/issues/I-20260707T172110Z-A.md
- promotion_gate: scan --project 正确返回 items + 平台检测走 adapter + 全部 7 缺陷修复
- acceptance_criteria:
  - A: scan --project 参数正确解析
  - B: 文件扫描不依赖 head_changed（始终扫）
  - C: 1b_reopen 集成到 Category 2
  - D: 无 raw-{key} 平台 issue 被报告
  - E: 平台检测/查询复用 platform-adapter
  - F: agent_working import 正确
  - G: extract_id 支持所有平台
