---
candidate_id: C-20260706T232728Z-A
status: promoted
source_raw: raw-20260706T232728Z
created_at: 2026-07-06
milestone: M-20260706T232728Z-A
---

## C-20260706T232728Z-A: 封装命令文档系统化

- candidate_format_version: v2
- title: 封装命令文档系统化 — 意图→命令映射 + 为什么用封装
- status: absorbed
- decision_reason: Option B — 集中 commands.md 作为权威参考 + 各触点嵌入场景化引导，覆盖所有用户触点
- next_action: B2_IBM 物化 I-* issue + prd/pre-tests/tasks/code-reviews →
  实现 6 个文件的文档修改
- revisit_trigger: 新封装命令被添加时需要更新 commands.md
- acceptance_criteria:
  - AGENTS.md 速查表增加"意图"列和"封装了什么"列
  - freely-workflow-guarded-execution SKILL.md 铁律区域前增加"意图→命令速查"章节
  - .githooks/bin/gh wrapper 每个拦截消息增加"为什么"解释
  - .githooks/pre-commit.sh 拦截末尾增加流程提示
  - .githooks/pre-push.sh 拦截末尾增加流程提示
  - 新建 docs/system/workspace/commands.md 封装命令权威参考
  - 所有位置的表述与 commands.md 一致
- promotion_gate: 6 个文件修改完成，语法检查通过，commands.md 覆盖全部 7 个封装命令
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260706T232728Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260706T232728Z/issues/I-20260706T232728Z-A.md
- milestone: M-20260706T232728Z-A
- session_refs: []
