---
candidate_id: C-20260703T003829Z-A
status: promoted
source_raw: raw-20260703T003829Z
created_at: 2026-07-03
milestone: M-20260703T003829Z-A
---

## C-20260703T003829Z-A: 修复 write_workcell_state 中 unsafe source

- candidate_format_version: v2
- title: 修复 write_workcell_state 中 unsafe source 导致的命令注入
- status: promoted
- decision_reason: 用已有的 meta_env_value 安全读取，改动最小，一致性最高
- next_action: 进入 B2_IBM 设计 → dev → test → PR
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - `write_workcell_state()` 不再使用 `source` 读取 env 文件
  - daemon 启动时不会因 env 文件中的多词值而执行意外命令
  - `.freely/run/workcell-state.env` 从 git 跟踪中移除
- promotion_gate:
  - brainstorms.md 完成决策记录
  - candidates.md 完成（本文件）
  - milestones.md 已更新
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: subagent
  - summary: 审查 unsafe source 替换为 meta_env_value 的正确性，确认无其他同类问题
  - verdict: pass
- promoted_issue_id: I-20260703T003829Z-A
- promoted_issue_path: docs/epics/runtime-core/safe-state-io/raw-20260703T003829Z/issues/I-20260703T003829Z-A.md
- milestone: M-20260703T003829Z-A
- session_refs: []
