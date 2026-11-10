---
candidate_id: C-20261110T093145Z-A
status: promoted
source_raw: raw-20261110T093145Z
created_at: 2026-11-10
milestone: M-20261110T093145Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261110T093145Z-A: raw H1 判定改为代码块感知，三处复用单一契约

- candidate_format_version: v2
- title: `raw_title_contract.find_local_heading` 新增；物化 / 副本 gate / H1 backfill 三处复用；gate 新增 `missing_local_title` 显式诊断
- status: promoted
- decision_reason: 三处裸 `^#\s+` 正则把 fenced code block 里的 python 注释误当 H1 —— 物化跳过注入、gate 借注释当 LOCAL title 并丢弃正文、backfill 跳过修复，导致健康 raw 的首个 PR 被 `content_diverged` 误挡。R23.13 已实际踩到并靠人工补 H1 绕过。
- next_action: 建 AT-001（6 静态 + 4 单元 + 4 行为）→ 扩展 `raw_title_contract` → 三处复用 → gate 加诊断 → 回归。
- revisit_trigger: 若 Markdown 出现新的围栏语法（缩进 >3 空格的围栏、HTML 注释包裹），需扩充 finder 并加夹具。
- acceptance_criteria:
  - RED：基线 `_local_record` 把代码注释当 title、物化不注入真实 H1、backfill 跳过修复；现有 H1 套件仍 PASS（守卫）。
  - GREEN：AT-001 `14 ok / 0 failed`；helper 对 ````` / `~~~` 围栏均正确；真实物化与真实 gate 行为正确。
  - GREEN：gate 无真实 H1 时给 `missing_local_title` 而非误导性 `content_diverged`。
  - GREEN：`tests/test-materialize-h1` 18 项 + 8 个相关测试 + `test-all --ci` 全绿。
  - GREEN：不改 `canonical_raw_title` / `local_heading_title` / `platform_title` 等既有契约函数语义。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 用 `git log -L` 否掉立项假设并找到既有 H1 注入逻辑；比对 #4264/#4269 两份物化文档定位代码块注释差异；逐处核对三处裸正则；实测 gate 借注释当 title 与物化跳过注入；确认既有契约与回归套件位置。
  - verdict: pass
- promoted_issue_id: I-20261110T093145Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261110T093145Z/issues/I-20261110T093145Z-A.md
- milestone: M-20261110T093145Z-A
- session_refs: []
