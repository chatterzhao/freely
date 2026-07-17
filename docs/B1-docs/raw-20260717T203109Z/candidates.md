---
candidate_id: C-20260717T203109Z-A
status: promoted
source_raw: raw-20260717T203109Z
created_at: 2026-07-17
milestone: M-20260717T203109Z-A
---

# Candidates

## C-20260717T203109Z-A: wt-close autonomous gate 收尾 — 静默退出/merge 竞态/RPC 数字键根修

- candidate_format_version: v2
- title: wt-close autonomous gate 收尾 — gate 静默退出、_has_merge 竞态、agent_working RPC 数字键序列化根修
- status: promoted
- decision_reason: PR #3980 的 gate 核心判定在位但三条判定输入全部失效（agent_working 恒空且致命、_has_merge 恒 false、a2a/B1 查询指错根）。实测根因与 raw 表面描述不同（详见 brainstorms P1-P4），需按根因修：handler 列名 d[0]→d[1] + gate 韧性四件套（try/except 降级、_main_root 解析、rev-list 免管道、|| true 双保险）
- next_action: N/A（已 promote）
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - db daemon 不在时 gate 不再静默杀死 wt-close：三态矩阵（foreign+merged→allow sweep / self+unfinished 无活动→allow / foreign+unfinished→DENY）均有可见 stderr 输出
  - _has_merge 对已合并 raw key（如 raw-20260717T004620Z）稳定判 true，无 SIGPIPE 竞态
  - agent_working.get / get_all RPC 返回命名键（worker_id 等），活跃 worker 行存在时 gate 判 DENY
  - gate 的 agent_working/a2a/B1 查询均指向主仓根（git-common-dir 解析），工位内执行行为一致
  - usage() --force 描述与 autonomous gate 语义同步
- promotion_gate: 全部 acceptance 有 RED（HEAD 版本复现）→ GREEN（修复后）证据；db_manager 修复不破坏既有 a2a handler 行为
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - summary: bash -x 追踪 + python 直跑逐项定位根因，P4 为新发现的共享 handler 缺陷（波及 SSE 复用路径），修复面收敛于 wt-close gate + db_manager 两行
  - verdict: pass
- promoted_issue_id: I-20260717T203109Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T203109Z/issues/I-20260717T203109Z-A.md
- milestone: M-20260717T203109Z-A
- session_refs: []
