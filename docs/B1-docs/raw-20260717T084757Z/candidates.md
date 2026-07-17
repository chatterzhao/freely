---
candidate_id: C-20260717T084757Z-A
status: promoted
source_raw: raw-20260717T084757Z
created_at: 2026-07-17
milestone: M-20260717T084757Z-A
---

# Candidates

## C-20260717T084757Z-A: 路由死定义搬移 + 静态断言

- candidate_format_version: v2
- title: _get_agent_slot 移至 main 前 + 日志时间戳
- status: promoted
- decision_reason: 位置性缺陷搬移即愈；AST 断言防复发。见 brainstorms Option A
- next_action: B2 → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - AC1: AST——main 块后无被引用 def；日志带时间戳
  - AC2: __main__ 语义沙箱——阻塞点前 _get_agent_slot 已定义
  - AC3: E2E——真实 daemon + chat 触发路由,无 NameError 且路由完成
- promotion_gate: 缺陷 file:line 坐实 + 生产日志实抓
- open_questions: []
- acceptance_reviews:
  - reviewer: inline-code-verification
  - mode: inline
  - summary: main 块位置/三调用点/07-04 引入考证
  - verdict: pass
- promoted_issue_id: I-20260717T084757Z-A
- promoted_issue_path: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/issues/I-20260717T084757Z-A.md
- milestone: M-20260717T084757Z-A
- session_refs: []
