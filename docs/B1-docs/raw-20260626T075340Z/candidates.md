---
candidate_id: C-20260626T075340Z-A
status: promoted
source_raw: raw-20260626T075340Z
milestone: M-20260626T075340Z-A
---

## C-20260626T075340Z-A: legacy issue

- candidate_format_version: v2
- title: cline tool-registry.toml slot/session fix + bridge_config_env CLI flag mode
- status: absorbed
- decision_reason: cline slot config 与实际行为不符，env var 测试证实 cline 不读任何环境变量
- next_action: 实现并合并
- revisit_trigger: N/A
- acceptance_criteria:
  - cline.slot 全部字段修正
  - bridge_config_env 支持 --* CLI flag 模式
  - 已有工具行为不变
- promotion_gate: 代码实现 + 评审通过
- open_questions: []
- promoted_issue_path: docs/issues/I-20260626T075340Z-A/issue.md
- milestone: M-20260626T075340Z-A
- absorbed_into: I-20260626T075340Z-A
