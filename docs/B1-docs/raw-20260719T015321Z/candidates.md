---
candidate_id: C-20260719T015321Z-A
status: promoted
source_raw: raw-20260719T015321Z
created_at: '2026-07-19'
milestone: M-20260719T015321Z-A
---

## C-20260719T015321Z-A: 清理 lead-agent.md 悬空引用 + 修复 governance-check 落后 skill 路径

- candidate_format_version: v2
- title: 清理 lead-agent.md 全项目悬空引用 + governance-check skill 路径对齐
- status: promoted
- decision_reason: lead-agent.md 已于 2026-05-15 删除，角色职责已并入 manager-agent.md。5 处悬空引用 + governance-check 的落后 skill 路径（引用不存在的目录）阻塞所有 raw issue。必须彻底清理。
- next_action: B2 物化 I-* issue → dev（全项目引用清理 + governance-check 路径修复）→ 验证 governance-check 全绿
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - governance-check 通过（无 lead-agent.md 缺失错误，无 skill 路径不存在错误）
  - 全项目无 `lead-agent` 悬空引用（除历史文档/commit message）
  - governance-check skill 路径均指向实际存在的文件
  - 4 个治理相关测试文件的 fixture 不再创建 fake lead-agent.md
- promotion_gate: governance-check 全绿 + 全项目 grep `lead-agent` 仅命中历史引用
- open_questions: []
- acceptance_reviews:
  - reviewer: self-review（scope 明确，纯引用清理，无代码逻辑风险）
  - mode: inline
  - summary: 所有改动均为删除/替换悬空引用，不引入新功能，不修改业务逻辑。skill 路径修复是 governance-check 正确运行的前提。
  - verdict: pass
- promoted_issue_id: I-20260719T015321Z-A
- promoted_issue_path: docs/B2-docs/{epic-name}/{story-name}/raw-20260719T015321Z/issues/I-20260719T015321Z-A.md
- milestone: M-20260719T015321Z-A
- session_refs: []
