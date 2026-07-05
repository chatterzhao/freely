# Candidates

## C-20260509T090210Z-A: legacy issue

- candidate_format_version: v2
- title: 主管-worker 交接从文件重构为 SQLite handoffs 表
- status: promoted
- decision_reason: 当前文件管道脆弱（awk regex 解析 markdown），表管理更可靠、可查询、可校验
- promoted_issue_path: docs/issues/I-20260509T090210Z-A/issue.md
- milestone: M-20260509T090210Z-A
- next_action: B2_IBM → dev-loop → merge
- acceptance_criteria:
  - handoffs 表替代 exit-contract.env + worker-prompts/*.txt 作为 launch 数据源
  - 主管和 worker 交接记录在同一表，role 字段区分
  - 工位路径存绝对路径
  - 写时校验 + 读时兜底
- open_questions:
  - 旧 continuity.md 是否需要改为从表查询？
