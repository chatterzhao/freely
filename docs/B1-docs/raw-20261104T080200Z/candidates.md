---
candidate_id: C-20261104T080200Z-A
status: promoted
source_raw: raw-20261104T080200Z
created_at: 2026-11-11
milestone: M-20261104T080200Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T080200Z-A: pr-review-guarded 迁回 scripts/ + 投影注册表与门禁

- candidate_format_version: v2
- title: 806 行实现移到 `scripts/worktree/pr-review-guarded` + `bin/` 4 行投影 + `bin-projections.yaml` + `bin/check-bin-projection` + 入口清单
- status: promoted
- decision_reason: 真源边界已失效但「超阈值就迁」是错的判据（多数是自包含工具）；用「登记 + 过期即失败」的注册表既能覆盖全部 99 个入口，又能避免为了指标造影子实现。
- next_action: AT-001（12 静态 + 4 行为）→ develop `cad8b5875` 基线 RED → 实现 → GREEN → PR。
- revisit_trigger: 注册表里 `implementation-in-bin` 清零或改标时，必须同步删条目；门禁会用「已降到阈值内即失败」逼你删。
- acceptance_criteria:
  - RED：`bin/pr-review-guarded` 806 行无 scripts 真源、无注册表、无门禁、无清单、AT 未接线、epics 无 story。
  - GREEN：`bin/pr-review-guarded` ≤8 行且 `exec` 指向 `scripts/worktree/pr-review-guarded`；迁移后的实现仍含 MAX_ROUNDS/REVIEWER_SKILL/verdict 解析。
  - GREEN：注册表覆盖全部超阈值入口；无过期条目；无仍登记但已降到阈值内的条目。
  - GREEN：`bin/check-bin-projection` 0/1/2 三态，未登记与过期豁免均被拒。
  - GREEN：清单列出 ≥30 条并引用后续 raw；AT 进 CORE/CI_CORE；epics 注册 story。
  - 不退化：`bin/freely pr-review-guarded` 分派不变；其余 98 个入口行为不变。
- promotion_gate: AT-001 RED → GREEN + `test-all --ci` + epics 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 用 `wc -l` 盘点 99 个入口并按内容分类；用 `git archive develop` 快照复现 RED；用临时 fixture 项目验证门禁的三条拒绝路径。
  - verdict: pass
- promoted_issue_id: I-20261104T080200Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261104T080200Z/issues/I-20261104T080200Z-A.md
- milestone: M-20261104T080200Z-A
- session_refs: []
