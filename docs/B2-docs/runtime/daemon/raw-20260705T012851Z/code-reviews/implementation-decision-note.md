---
issue_id: I-20260705T012851Z-A
issue_path: docs/B2-docs/runtime/daemon/raw-20260705T012851Z51Z/issues/I-20260705T012851Z-A.md
phase_state: completed
---
- issue_id: I-20260705T012851Z-A
## Implementation Decision Note
- decision: _unique_tools[*] → [*]:- 防崩 + 空数组根因诊断 + dirty 提示指向工作流
- why_this: bash 3.2 set -u 下空数组崩溃；dirty 提示缺 workflow 引导
- alternatives_considered: 仅加 :- 兜底 → 掩盖根因；预填 AGENT_AI_TOOL → 复杂且不必要
- boundary_non_goals: 不修改 bridge 启动逻辑本身
- residual_risk: 无
