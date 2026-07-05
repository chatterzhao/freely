---
candidate_id: C-20260705T231131Z-A
status: promoted
source_raw: raw-20260705T231131Z
milestone: M-20260705T231131Z-A
---

## C-20260705T231131Z-A: 全项目旧路径引用清理

- candidate_format_version: v2
- title: 19个执行脚本 docs/issues→docs/B1-docs + docs/epics→docs/B2-docs
- status: promoted
- decision_reason: |
    上一个 PR docs-structure-refactor 遗漏了 bin/ + scripts/ 执行层。
    B1-docs: raw-{key}/issue.md (目录+文件)
    B2-docs: I-{key}.md (扁平 .md 文件，通过 raw_key 反向查找)
- next_action: B2 设计 → 实现（代码已在工作区）→ 测试
- revisit_trigger: 新 issue 写入旧路径
- acceptance_criteria:
  - 19 个核心脚本 `grep 'docs/issues\|docs/epics'` 归零
  - governance-closeout-gate 正确处理 raw-* 和 I-* 双路径
  - wt-create 能正常从 platform pull raw issue
  - 所有脚本 `bash -n` 通过
- promotion_gate: B1 brainstorms 完成 + candidate promoted + 实现完成
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260705T231131Z-A
- promoted_issue_path: pending://B2-materialization
- milestone: M-20260705T231131Z-A
- session_refs: []
