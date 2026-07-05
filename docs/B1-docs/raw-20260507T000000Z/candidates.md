# Candidates

## C-20260507-A: legacy issue

- candidate_format_version: v2
- title: 统一的仓库平台层用于 issue-sync，提供 create/update/close/comment/pull 操作
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T070000Z-A/issue.md
- decision_reason: 当前平台交互散落在 5+ 个文件中，功能重叠但不统一；统一平台层是后续自动化流程的基础，能降低维护成本和引入新平台的门槛
- milestone: M-20260507-A
- acceptance_criteria:
  - 统一平台层提供 create/update/close/comment/pull 标准操作
  - 所有 CLI/脚本统一调用平台层，消除重复实现
  - 支持 GitHub 和 Gitee 双平台
  - chat-inbox → raw issue 物化后自动调用 platform.create
  - merge 后自动调用 platform.update/close 同步所有平台
