---
candidate_id: C-20260707T043833Z-A
status: absorbed
source_raw: raw-20260707T043833Z
milestone: M-20260707T043833Z-A
---
## C-20260707T043833Z-A: 彻底移除本地 raw issue 创建路径
- status: absorbed
- decision_reason: 不留 fallback——7 个文件全部清理，只允许 platform 模式
- promoted_issue_id: I-20260707T043833Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T043833Z/issues/I-20260707T043833Z-A.md
- acceptance_criteria:
  - chat-inbox.py 文件删除
  - freely_db_manager.py new-issue 创建逻辑移除
  - governance-merge-gate chat-inbox catch-all 移除
  - freely-db-cli --type new-issue 默认值移除
  - freely chat --new-issue 重定向到 freely feedback
  - task-lifecycle-scan.py chat-inbox 扫描移除
- promotion_gate: 6 个文件修改完成，无本地 raw issue 创建路径残留
