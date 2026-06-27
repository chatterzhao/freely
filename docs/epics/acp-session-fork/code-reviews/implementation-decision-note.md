---
issue_id: I-20260627T084551Z-A
issue_path: docs/issues/I-20260627T084551Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260627T084551Z-A
- decision: fork 路径 try session/fork，运行时检测能力，不支持降级 session/new
- why_this: ACP 官方规范，Claude+OpenCode 已支持，无需 registry 字段
- alternatives_considered: 按工具分 registry 字段（冗余，运行时可检测）
- boundary_non_goals: 不修改工具注册表
- residual_risk: session/fork 在 unstable flag 下，未来 ACP 协议可能有变化
