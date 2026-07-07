# Implementation Decision Note
- issue_id: I-20260707T162123Z-A
- decision: close_issue/add_comment API 改为 platform_ids dict 参数，每个平台用自己的 ID
- why_this: GitHub 数字 ID vs Gitee 字母 ID，传同一个 ID 给所有平台不正确
- alternatives_considered: close 内部自己读 issue.md → 紧耦合；参数改为 dict → 干净
- boundary_non_goals: 不改 Handler 接口（每个 Handler 仍然接受单个 issue_id）
- residual_risk: 调用方需自己从 issue.md 读 platform_ids 传入
