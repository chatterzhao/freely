---
candidate_id: C-20261116T050414Z-A
status: promoted
source_raw: raw-20261116T050414Z
created_at: 2026-11-16
milestone: M-20261116T050414Z-A
---

# Candidates

## C-20261116T050414Z-A: 标题规范化前移到 scan 漏斗

- candidate_format_version: v2
- title: scan 入口自动规范化平台 raw 标题 + pr-create 兜底 + 门禁可操作诊断
- status: promoted
- design_verdict: 实现未完成（能力已存在但未接到唯一漏斗；CLOSED/absorbed 入口不可达）
- anchor_refs:
  - brainstorms.md §0「Read-only lifecycle gate for a configured raw replica set.」
  - brainstorms.md §0「scan preparation must not ... platform side effects」
  - brainstorms.md §0「不改平台读取通道、不改 scan 状态机」
  - brainstorms.md §0「[title] {plat}: normalized to {canonical}」
- decision_reason: 用户明确 scan 是所有平台 raw 进入本地任务的漏斗；历史实现只在物化路径触发，导致不达标标题到 PR 才暴露且报错无指引。Option C 把同一契约接到正确时机，同时保持 gate 与 scan 分析器只读。
- next_action: B2 物化 I-* issue 与 pre-tests → RED → dev 实现 → GREEN → PR 收口
- revisit_trigger: 若 scan 不再作为平台 raw 的唯一入口，或 raw_title_contract 迁移到新真源，重新评估落点
- acceptance_criteria:
  - `freely task-source-scan` 在建索引前规范化 OPEN raw 标题，stdout 含 from→to
  - 规范化只改标题、走 adapter 唯一通道、幂等、支持 dry-run
  - `pre-scan-fix.sh` 与 `task-lifecycle-scan.py` 分析器零平台写
  - `pr-create-guarded` 对 absorbed/CLOSED raw 的 preflight 仍生效
  - gate 报 `non_canonical_title` 且含 observed/expected/suggested_command，输出精简
  - develop 基线 RED、修复后 GREEN，AT 进 CORE/CI_CORE
- promotion_gate: B0 判定为「实现未完成」且有 4 条原文锚点；Option C 与用户方案修订一致；边界不违反只读契约
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: plan-subagent
  - summary: 对照用户方案修订评论与历史 c0b1af50b 决策，确认「scan 主入口 + pr-create 兜底」兼容只读契约，且以 title+body 取 key 可避免 created_at 猜 key
  - verdict: pass
- promoted_issue_id: I-20261116T050414Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/issues/I-20261116T050414Z-A.md
- milestone: M-20261116T050414Z-A
- session_refs:
  - tool/session_id/unavailable://current-session/role/owner
