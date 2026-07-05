# Code Review: skill ref cleanup
- issue_id: I-20260508T004541Z-A
## Implementation Decision Note
- decision: 全部路径引用改为 skill:name；deploy-skills 支持 --tools 逗号分隔多工具
- why_this: skills 已通过 deploy-skills 部署到 ~/.claude/skills/ 和 ~/.codex/skills/，所有工具可用 skill:name
- alternatives_considered: 保留路径引用（拒绝：deploy 后路径失效）；只改部分文件（拒绝：不彻底）
- boundary_non_goals: 历史文档（epics/brainstorms）不改，保持冻结记录
- residual_risk: Codex 的 skill:name 需验证（已部署到 ~/.codex/skills/）
