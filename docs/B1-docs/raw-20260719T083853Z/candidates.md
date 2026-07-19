---
candidate_id: C-20260719T083853Z-A
status: promoted
source_raw: raw-20260719T083853Z
created_at: '2026-07-19'
milestone: M-20260719T083853Z-A
---
## C-20260719T083853Z-A: 三层防线校验 a2a task + agent_working 写入

- candidate_format_version: v2
- title: L1 argparse handler + L2 DB insert + L3 agent_assign 三层校验 worker task 必填字段
- status: promoted
- decision_reason: 当前写入链三层全通零拦截，worktree/branch/raw-key 空值静默写入。需三层校验 + 精确错误消息。
- next_action: B2 → dev（a2a_task.py L1 + freely_db_manager.py L2 + agent_working.py L3 + freely prompt模板）→ test → PR
- acceptance_criteria:
  - L1: role=worker 时 worktree/branch/raw_key 非空 → 空则报错含字段名
  - L1: 新 task state 必须 submitted → 否则报错
  - L2: DB insert 前再次检查 worker task 必填字段
  - L3: agent_assign worker role 时 agent_id 格式校验
  - prompt 模板含 --worktree --branch --raw-key
- promotion_gate: 三层校验代码存在，prompt 模板补全
- open_questions: []
- acceptance_reviews: [ reviewer: self-review, mode: inline, verdict: pass ]
- promoted_issue_id: I-20260719T083853Z-A
- promoted_issue_path: docs/B2-docs/{epic-name}/{story-name}/raw-20260719T083853Z/issues/I-20260719T083853Z-A.md
- milestone: M-20260719T083853Z-A
- session_refs: []
