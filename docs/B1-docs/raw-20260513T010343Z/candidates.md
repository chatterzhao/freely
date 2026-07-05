# Candidates

## C-20260513T010343Z-A: legacy issue

- candidate_format_version: v2
- title: 秒级 raw key 格式清理——4 处 regex 遗漏 + 10+ 处文档更新
- status: promoted
- decision_reason: #326 确认 + I-20260507T143545Z-A 验证时遗漏的 14 处，改动已在 feature 工位实现
- next_action: B2_IBM materialize → merge
- acceptance_criteria:
  - freely 脚本 4 处 regex 已改为 `[0-9]{4,6}`
  - wt-create 帮助/错误消息 + legacy regex 已更新
  - governance-merge-gate、ibm-framework.md、CONSTITUTION.md 格式文字已更新
  - 3 个 skill 文件 + pre-push.sh 格式文字已更新
  - grep -rn THHMMZ（不含 [SS]/SS）在 docs/system/ 中仅剩 2 处 task-lifecycle-scan.py 注释（文档性，非格式规范）
- promoted_issue_path: docs/issues/I-20260513T010343Z-A/issue.md
- milestone: M-20260513T010343Z-A
