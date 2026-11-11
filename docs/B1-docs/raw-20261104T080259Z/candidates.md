---
candidate_id: C-20261104T080259Z-A
status: promoted
source_raw: raw-20261104T080259Z
created_at: 2026-11-11
milestone: M-20261104T080259Z-A
---

# Candidates

被否决方案见 brainstorms.md。

## C-20261104T080259Z-A: 投影一致性契约（copy/delegate 双语义 + 四类投影 + CI）

- candidate_format_version: v2
- title: 清 `.githooks/` 死副本 + `post-checkout` 迁真源 + `projection.lock` + `freely projections verify` + deploy-skills 写回 hash + AGENTS skill 名修正
- status: promoted
- decision_reason: 投影分 copy 与 delegate 两种，按字节 hash 一律比对会把 61/62 条误判为漂移；用 mode 字段区分后，既能证明部署副本一致，也能证明 wrapper 仍指向真源。skills 目标在 $HOME，必须留在 machine-local lock，否则仓库 lock 不可移植。
- next_action: AT-001（16 静态 + 4 行为）→ develop `27e91e50c` 基线 RED `1 ok / 19 failed` → 实现 → GREEN `20 ok / 0 failed` → unit 17 文件 111 断言 + CI 21/0 → PR。
- revisit_trigger: 新增 wrapper 或新增 `bin/` 投影后必须重跑 `freely projections record`；改真源而不 record 会被 verify 判红（这是设计意图）。
- acceptance_criteria:
  - RED：6 个非 wrapper 文件仍在、`post-checkout` 不是委托形态、无 lock、无 verifier、runtime 无 `projections`、生成器/模板含 3 个幽灵 skill 名、AT 未接线、epics 无 story。
  - GREEN：`.githooks/` 只有 8 个 wrapper + `.gitignore` + `bin/`；8 个 wrapper 全部 `exec` 真源。
  - GREEN：lock 声明四类 kind，仓库内含 hooks/bin/agents 三类；每条含 kind/source/target/sha256/mode；所有路径存在、所有 hash 与真源一致。
  - GREEN：`freely projections verify` 一致时 0；篡改真源或切断 wrapper 委托时非 0；lock 缺失时 2。
  - GREEN：生成器与模板零幽灵 skill 名，模板引用的名字全部真实存在。
  - GREEN：AT 进 `CORE`/`CI_CORE`；epics 注册 story；`bin/deploy-skills` 部署后写回 hash。
  - 不退化：`bin/check-runtime-size` 仍 ok（**预算不上调**）；`bin/check-bin-projection` 仍 ok；7 个既有 AT 全绿；post-checkout 行为不变。
- promotion_gate: AT-001 RED → GREEN + unit 111 断言 + `test-all --ci` 21/0 + 三个门禁全过
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 全仓扫描确认 6 个待删文件无引用；用 `git archive develop` 快照复现 RED；真机冒烟 post-checkout 三种入参；用沙箱树验证真源篡改与委托切断都被拒。
  - verdict: pass
- promoted_issue_id: I-20261104T080259Z-A
- promoted_issue_path: docs/B2-docs/gate/projection-consistency/raw-20261104T080259Z/issues/I-20261104T080259Z-A.md
- milestone: M-20261104T080259Z-A
- session_refs: []
