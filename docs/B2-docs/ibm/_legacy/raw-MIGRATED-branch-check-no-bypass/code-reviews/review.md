# Code Review: no bypass branch check
- issue_id: I-20260510T1840Z-A
## Implementation Decision Note
- decision: 移除 --skip-branch-check，daemon start 也加检查
- why_this: 宁可 init 失败，不让后续无限循环
