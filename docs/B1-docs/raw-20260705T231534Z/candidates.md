---
candidate_id: C-20260705T231534Z-A
status: promoted
source_raw: raw-20260705T231534Z
created_at: 2026-07-06
milestone: M-20260705T231534Z-A
---

## C-20260705T231534Z-A: ./bin/xxx → freely xxx 统一引用

- candidate_format_version: v2
- title: ./bin/xxx → freely xxx 统一引用
- status: promoted
- decision_reason: ~230 处 ./bin/ 引用，按"用户可见→freely xxx，source/chmod/-x检查→保留"规则分类替换
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - 所有用户可见文本（echo/cat/help/usage/错误提示）中 ./bin/xxx → freely xxx
  - source ./bin/ 保留（需要文件路径）
  - chmod +x ./bin/ 保留（安装指令）
  - -x "./bin/xxx" 保留（文件存在性检查）
  - hook 脚本中 gate 调用改为 freely xxx
- promotion_gate: grep 验证无遗漏的用户可见 ./bin/ 引用
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: ~230 处分类替换，规则清晰，逐文件执行
  - verdict: pass
- promoted_issue_id: I-20260705T231534Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260705T231534Z/issues/I-20260705T231534Z-A.md
- milestone: M-20260705T231534Z-A
- session_refs: []
