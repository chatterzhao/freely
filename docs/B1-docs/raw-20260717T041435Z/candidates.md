---
candidate_id: C-20260717T041435Z-A
status: promoted
source_raw: raw-20260717T041435Z
created_at: 2026-07-17
milestone: M-20260717T041435Z-A
---

# Candidates

## C-20260717T041435Z-A: 门禁字段解析引号可选化

- candidate_format_version: v2
- title: pretests-gate 与 pr-review-guarded 解析统一（引号可选）
- status: promoted
- decision_reason: 两门禁互斥格式使任何单一写法必被其一拦截；引号可选化向后兼容全部存量（含双行 workaround）。见 brainstorms Option B
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: runtime_pid_file_for_role acp_bridge glob 多文件展开问题需另行 B1（raw 附带段已记录）
- acceptance_criteria:
  - AC1: pretests-gate extract 对 裸值/'单引号'/"双引号"/`反引号` 四种输入均解析出纯路径（python 行为测试）
  - AC2: pr-review-guarded 取值逻辑对同四种输入均得纯路径（bash 行为测试）
  - AC3: 回归——已合并 lane 的引号版 I-*（raw-20260717T004620Z）与双行版 I-*（raw-20260717T004721Z）均通过两门禁的路径格式校验
- promotion_gate: 两解析点 file:line 坐实；今日双向拦截各有一次实证
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: 双向拦截实证（lane A 无引号被 review 拦、lane C 引号被 gate 拦）+ 源码逐行核实
  - verdict: pass
- promoted_issue_id: I-20260717T041435Z-A
- promoted_issue_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20260717T041435Z/issues/I-20260717T041435Z-A.md
- milestone: M-20260717T041435Z-A
- session_refs: []
