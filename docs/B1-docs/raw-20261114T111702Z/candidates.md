---
candidate_id: C-20261114T111702Z-A
status: promoted
source_raw: raw-20261114T111702Z
created_at: 2026-11-24
milestone: M-20261114T111702Z-A
---

## C-20261114T111702Z-A: cmd_comment 复用 SELF_ROOT 修复 ACP 通知未定义变量

- candidate_format_version: v2
- title: cmd_comment 复用 SELF_ROOT 修复 ACP 通知未定义变量
- status: promoted
- design_verdict: bug
- anchor_refs:
  - brainstorms.md §0「docs/system/workspace/scripts/runtime/freely:32 `SELF_ROOT="$(cd ... && pwd -P)"`」
  - brainstorms.md §0「docs/system/workspace/scripts/runtime/freely:3707 `PROJECT_ROOT="$project"` 位于 heredoc 内；:3687 显式 unset PROJECT_ROOT」
  - brainstorms.md §0「docs/system/workspace/scripts/runtime/split-plan.md:97 `bin/check-runtime-size` 读 `runtime/.size-budget`，超过即 fail-closed；只许下调，不许上调。」
- decision_reason: 根因是 `cmd_comment()` 在 `set -u` 下引用了未定义且非全局的 `PROJECT_ROOT`；`SELF_ROOT` 已定义为单一根路径真源。等长（同行）替换两处引用即可恢复 ACP worker 通知，不新增行、不放宽门禁。
- next_action: 进入 B2_IBM 物化 I-20261114T111702Z-A，设计 AT 覆盖 rc=0 / 无 unbound variable / 平台评论成功 / ACP stub 被调用 / 行数门禁绿 / 基线红。
- revisit_trigger: 若 `SELF_ROOT` 与项目根路径不等价，或等长替换导致 check-runtime-size 失败，回到 B1 重判。
- acceptance_criteria:
  - brainstorms.md 含 discovery/research/decision 与 B0 广搜、二元决策
  - candidate 有 design_verdict 与 ≥2 条 anchor_refs
  - milestones.md candidate_issues 已同步 M-20261114T111702Z-A
  - 方案不新增行、不引入第二套根路径变量
- promotion_gate: B1 边界稳定，acceptance review verdict=pass，milestone 绑定完成
- open_questions: []
- acceptance_reviews:
  - reviewer: independent-plan-review
  - mode: plan-subagent
  - summary: 核对 B0 锚点逐字命中、三类分层与矛盾清单、Q1-Q4 判定；确认 bug 判定与等长替换方案一致，未新增行、未改门禁。
  - verdict: pass
- promoted_issue_id: I-20261114T111702Z-A
- promoted_issue_path: docs/B2-docs/acp/cross-tool-session/raw-20261114T111702Z/issues/I-20261114T111702Z-A.md
- milestone: M-20261114T111702Z-A
- session_refs: []
