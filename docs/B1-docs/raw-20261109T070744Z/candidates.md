---
candidate_id: C-20261109T070744Z-A
status: promoted
source_raw: raw-20261109T070744Z
created_at: 2026-11-09
milestone: M-20261109T070744Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261109T070744Z-A: 门禁把「修复既有损坏」与「多 issue 混入」区分开

- candidate_format_version: v2
- title: `governance-merge-gate` 对基线副本不可解析的 issue 文档做结构修复豁免（staged 与 range 双路径）；基线可解析的跨 key 文档仍拦截
- status: promoted
- decision_reason: GATE 1 与后续 owner 校验让 23 份历史坏文档在门禁下永远无法被修复——修它的分支必然被判「一工位多 issue」。这是死锁，阻塞 #4148 的存量修复面。
- next_action: 建 AT-001（6 夹具 + 6 仓库/选择 + 1 反向守护），改 `governance-merge-gate` 的 `baseline_text` / `legacy_frontmatter_damaged` / `select_repair_only_paths` 并接入 GATE 1 前的 owner 剔除。
- revisit_trigger: 若引入远端 runner 或门禁改为读 PR diff（而非 staged/range），需重新确认 baseline 解析路径。
- acceptance_criteria:
  - RED：develop 基线无该能力 → AT-001 `5 ok / 8 failed`。
  - RED：staged 模式必须生效（`pr-merge-guarded` 走的就是它）。
  - GREEN：AT-001 `13 ok / 0 failed`。
  - GREEN：基线可解析、key 不匹配的文档仍被拦截（反向守护）。
  - GREEN：legacy bullet-only 文档不被判损坏。
  - GREEN：`raw-20261103T132517Z` 的 PR 在 develop 侧通过合并门禁。
- promotion_gate: AT-001 RED → GREEN + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 复现 28 条错误；核对 `--staged` 与 `--range` 两条执行路径；验证安装态不参与（hook 取 `git rev-parse --show-toplevel`）；证伪「按 diff 内容判断」「路径白名单」两条替代方案。
  - verdict: pass
- promoted_issue_id: I-20261109T070744Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261109T070744Z/issues/I-20261109T070744Z-A.md
- milestone: M-20261109T070744Z-A
- session_refs: []
