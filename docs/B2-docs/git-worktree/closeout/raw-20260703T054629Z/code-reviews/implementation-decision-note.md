- issue_id: I-20260703T054629Z-A
## Implementation Decision Note
- decision: wt-close 查找 test-pre-merge 工位路径传入 pretests-retirement-gate
- why_this: 与 pr-create-guarded 一致，test-gate.env 仅在 test 工位存在
- alternatives_considered: 无
- boundary_non_goals: 不修改 pretests-retirement-gate 本身
- residual_risk: 若 raw key 提取失败则回退到原行为
