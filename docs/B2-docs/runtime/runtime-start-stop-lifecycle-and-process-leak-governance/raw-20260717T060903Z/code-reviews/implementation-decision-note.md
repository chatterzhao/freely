---
issue_id: I-20260717T060903Z-A
issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/issues/I-20260717T060903Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T060903Z-A
- issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/issues/I-20260717T060903Z-A.md

## Implementation Decision Note

- decision: self-heal acp_bridge 逐文件枚举（新 _clear_stale_acp_bridge_pid_file_if_invalid）+ 清理 per-tool 定向；runtime_pid_file_for_role 分支消 glob
- why_this: 失效点与误伤点都在 self-heal 层，单层收敛；ensure 层（已修 lane）不动
- alternatives_considered: 返回首个匹配（漏检其余，否）；pid 族入 SQLite（另案）
- boundary_non_goals: 不动 ensure/bridge 本体/monitor
- residual_risk: 文件名 tool 后缀解析依赖命名约定 <hash>-<tool>.pid——该约定由 acp-bridge.py _pid_file 单点生成，漂移风险低
