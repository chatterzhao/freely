# Candidates
## C-20260511T001900Z-A: legacy issue
- title: 消掉 latest-manager 管道脆弱性
- status: promoted
- decision_reason: 管道串两个 python3 2>/dev/null 吞错误导致 false positive，需改为直接 SQLite 查询
- promoted_issue_path: docs/issues/I-20260511T001900Z-A/issue.md
- milestone: M-20260511T001900Z-A
- completion_note: I-20260511T001900Z-A 已完成 closeout，sync 管道修复已吸收到 develop
