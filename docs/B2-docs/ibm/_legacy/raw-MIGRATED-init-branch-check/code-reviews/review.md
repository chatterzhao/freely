# Code Review: init branch check
- issue_id: I-20260510T1326Z-A
## Implementation Decision Note
- decision: validate_project_branch_names 在 init 时扫描全部分支，不合规直接 exit 1
- why_this: 提前拦截比运行时发现更可靠，避免 AI 陷入无法修复的循环
