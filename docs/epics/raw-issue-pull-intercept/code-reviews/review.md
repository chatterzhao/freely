# Code Review: raw-issue-pull interception guard
- issue_id: `I-20260507T143544Z-A`
## Implementation Decision Note
- decision: 在 raw-issue-pull 中添加工位/分支名校验，受保护分支直接拒绝
- why_this: 防止从 develop 等受保护分支越权拉取任意 issue
- alternatives_considered: 仅在 wt-create 内部校验（拒绝: 独立调用 raw-issue-pull 仍可绕过）
- boundary_non_goals: 不改变 platform-adapter.py 的拉取逻辑
- residual_risk: none
