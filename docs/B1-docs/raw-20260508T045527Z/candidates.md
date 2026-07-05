# Candidates
## C-20260508T045527Z-A: legacy issue
- candidate_format_version: v2
- title: 删除废弃扫描脚本
- status: promoted
- decision_reason: 废弃的 task-source-scan.py 需要清理，统一使用 task-lifecycle-scan.py，单一切口风险低
- promoted_issue_path: docs/issues/I-20260508T045527Z-A/issue.md
- milestone: M-20260508T045527Z-A
- completion_note: I-20260508T045527Z-A 已完成 closeout，task-source-scan.py 已删除并吸收到 develop
- acceptance_criteria:
  - task-source-scan.py 已删除
