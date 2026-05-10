# Code Review: raw issue governance reminder injection
- issue_id: I-20260510T0112Z-A
## Implementation Decision Note
- decision: 在 issue-sync _issue_body 中对 kind=raw 注入治理提醒行
- why_this: 最小侵入，只在同步到平台时附加，不影响本地 issue.md
- alternatives_considered: (1) raw-issue-pull 注入到本地文件 — 会在下次同步时被覆盖 (2) GitHub Actions 注入 — 复杂
- boundary_non_goals: 不改变其他 kind 的 issue 正文，不改变 raw-issue-pull 行为
