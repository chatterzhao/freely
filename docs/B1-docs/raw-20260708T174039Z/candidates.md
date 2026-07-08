---
candidate_id: C-20260708T174039Z-A
status: absorbed
source_raw: raw-20260708T174039Z
milestone: M-20260708T174039Z-A
---
## C-20260708T174039Z-A: tool-launchers socket path fix

- candidate_format_version: v2
- title: tool-launchers.sh socket path 加入 base_tool 后缀
- status: absorbed
- milestone: `M-20260708T174039Z-A`
- decision_reason: 一行修复——_bridge_socket 调用传入已解析的 tool 名作为 base_tool
- next_action: 修改 tool-launchers.sh 第 823 行
- revisit_trigger: N/A
- acceptance_criteria:
  - tool_run_acp_from_prompt_file 中 _bridge_socket 调用传入 $tool
  - daemon 启动后 cycle log 不再为 0 字节
- promotion_gate: 修改一行，验证 socket 路径正确
- open_questions: []
- promoted_issue_id: I-20260708T174039Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T174039Z/issues/I-20260708T174039Z-A.md
absorbed_into: I-20260708T174039Z-A
