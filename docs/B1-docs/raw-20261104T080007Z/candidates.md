---
candidate_id: C-20261104T080007Z-A
status: promoted
source_raw: raw-20261104T080007Z
created_at: 2026-11-10
milestone: M-20261104T080007Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T080007Z-A: 核心 runtime 建立函数级 RED→GREEN 证据链

- candidate_format_version: v2
- title: `tests/unit/` 函数级语料 + PR body 强制 `## RED 证据` + review 侧 runtime RED gate + 3 个历史修复补录
- status: promoted
- decision_reason: 27,272 行运行时只有端到端测试，「先红后绿」无法证明；PR body 默认 `See commits for details.`，review 侧没有任何 TDD 检查，宪法 §16 的自举不自我豁免在核心 runtime 上失效。
- next_action: AT-001（6 静态 + 4 行为组）→ develop 基线 RED `2 ok / 19 failed` → 实现 → 工位 GREEN `21 ok / 0 failed` → 回归 + CI → PR。
- revisit_trigger: 若运行时被拆分（#4160）或 review 改成必须调用 ACP，RED gate 的 diff 判定与证据来源要重新对齐。
- acceptance_criteria:
  - RED：无 `tests/unit/`；无 `pr_body.py` / `runtime_red_gate.py`；`pr-create-guarded` body 为裸文案；`pr-review-guarded` 无 RED 检查。
  - GREEN：≥10 个函数级测试（实测 14 文件 / 68 断言）覆盖状态机、锁、退出码，且 runner 自身能失败（故意失败的 probe 必须让 runner 非零退出）。
  - GREEN：非 runtime diff → `## RED 证据` 标注「不适用」；runtime diff 无证据 → 组 body exit 3 拒绝建 PR；有证据 → 引用命令/RED/GREEN/证据路径。
  - GREEN：review gate 非 runtime → exit 2 skip；runtime 无单测/无证据 → exit 1 refuse；齐全 → exit 0 pass。
  - GREEN：3 个已合并修复在各自修复前基线上复现 RED（A `6715a67a2`、B/C `83ba84a74`）。
  - 不退化：不改 `runtime/freely` 任何一行、不改 `issue-write-one`/0-3-1 退出码、不改 promote/close 语义。
- promotion_gate: AT-001 RED → GREEN + 回归 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 核实运行时是 sourceable 库（#4153）而非必须重构；核实仓库无 PR 模板且 `gh pr create --body` 会覆盖模板，因此改走 body 组合；用 `git archive` 取三个历史修复前快照，把 `tests/unit` 注入后逐个复现 RED。
  - verdict: pass
- promoted_issue_id: I-20261104T080007Z-A
- promoted_issue_path: docs/B2-docs/runtime/tdd-evidence/raw-20261104T080007Z/issues/I-20261104T080007Z-A.md
- milestone: M-20261104T080007Z-A
- session_refs: []
