---
candidate_id: C-20261104T075849Z-A
status: promoted
source_raw: raw-20261104T075849Z
created_at: 2026-11-11
milestone: M-20261104T075849Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T075849Z-A: runtime 拆分第一阶段（helper 单源 + 3 子命令外移 + 行数守卫）

- candidate_format_version: v2
- title: `runtime/lib/common.sh` 单源 + `bin/test-gate` / `bin/evidence` 外移 + `bin/check-runtime-size` + 依赖矩阵 + Rust PoC
- status: promoted
- decision_reason: 单体已从 26,823 涨到 27,272 且 `check-file-size` 对它完全跳过，所以「拆分」的第一步必须是**建立可机检的行数承诺**；同时外移的真实阻塞是 helper 内联，先把 helper 变成单源，后续每个 phase 1/2 外移都只需 `exec` 一行。
- next_action: AT-001（12 静态 + 4 行为）→ develop `d33855eb0` 基线 RED `0 ok / 16 failed` → 实现 → GREEN `16 ok / 0 failed` → 单测 16 文件 98 断言 + CI 19/0 → PR。
- revisit_trigger: 每完成一批 phase 1/2 外移，必须同步下调 `runtime/.size-budget`；若某个外移导致 `bin/freely` 的 source 身份失效（4 个脚本 source 单体），说明边界选错，回退该命令。
- acceptance_criteria:
  - RED：无 `bin/test-gate`、无 `bin/evidence`、无 `lib/common.sh`、单体仍内联 9 个 helper、3 个 cmd 未投影、无行数守卫、无矩阵、无 Rust PoC、AT 未接线、epics 无 story。
  - GREEN：单体不再定义 `_log_ts`/`log_*`/`current_timestamp_utc_for_machine`/`state_dir`/`run_dir_for_project`/`_test_gate_file`/`_test_gate_write`，且 source `lib/common.sh`。
  - GREEN：3 个 `cmd_*` 只剩 `exec bash "$SELF_ROOT/bin/..."` 投影。
  - GREEN：`bin/test-gate` 拒绝非 test-pre-merge 工位（rc 2）并接受 test-pre-merge（写 gate env）；`bin/evidence add` 拒绝不存在的文件（rc 2）。
  - GREEN：`bin/check-runtime-size` 读 `runtime/.size-budget`，超预算 fail-closed；预算 < 27,272 且 ≥ 实际行数。
  - GREEN：`split-plan.md` 覆盖全部 56 个 `cmd_*`（矩阵 ≥50 行）；`rust-migration-poc.md` 有边界/成本/回滚且声明未迁移。
  - 不退化：`bin/freely` 的 source 身份不变、4 个 source 单体脚本仍可用、既有 AT 全绿（R27 21、R28 21、R28.5 18、R29 16、R30 17）。
- promotion_gate: AT-001 RED → GREEN + unit 98 断言 + `test-all --ci` 19/0 + epics 对齐
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 用脚本解析 944 个顶层函数生成依赖矩阵（非手写）；用 `git archive develop` 快照复现 RED；外移后用真机冒烟（refuse 非 test 工位 / accept test 工位 / 写 gate env / 未知子命令 exit 1）证明行为不变。
  - verdict: pass
- promoted_issue_id: I-20261104T075849Z-A
- promoted_issue_path: docs/B2-docs/runtime/runtime-split/raw-20261104T075849Z/issues/I-20261104T075849Z-A.md
- milestone: M-20261104T075849Z-A
- session_refs: []
