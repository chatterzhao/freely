# Code Review: skill ref cleanup
- issue_id: I-20260508T004541Z-A
## Implementation Decision Note
- decision: lead-agent.md 改为 dual-mode；runtime 脚本保持路径
- why_this: runtime prompt 需兼容 Codex（无 skill 部署）
- alternatives_considered: 全部改 skill 名（拒绝：破坏 runtime）
- boundary_non_goals: 不改 start-lead-agent.sh 等 runtime 脚本
- residual_risk: none
