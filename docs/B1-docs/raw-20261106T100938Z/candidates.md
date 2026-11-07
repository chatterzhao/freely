---
candidate_id: C-20261106T100938Z-A
status: promoted
source_raw: raw-20261106T100938Z
created_at: 2026-11-06
milestone: M-20261106T100938Z-A
---

# Candidates

被否决的替代方案（把 allowlist 改成自动包含整个目录、把 3 个纯文档一并打包、把防复发检查合并进 R5 的 seed parity、批量改写历史安装版本）属退化或越界，完整记录见 brainstorms.md，不作为 candidate 立项。

## C-20261106T100938Z-A: 补齐运行时必需的 allowlist 条目并建立防复发检查

- candidate_format_version: v2
- title: 显式补齐 5 个运行时必需 workspace 顶层文件；新增只读 checker 保证「运行时引用的 tracked 顶层文件」不会漏出 allowlist
- status: promoted
- decision_reason: 根因是两份事实（运行时引用 vs 打包声明）各自维护且无机器约束。只补 5 行能修当下，但以后再新增运行时文件仍会静默漏配；因此需要只读一致性检查作为打包前置。保留显式白名单机制是 #4157 的既有收敛成果，不得破坏。
- next_action: 写 AT-001 RED（真实安装态自举打包失败 / seeder 回退 builtin），补 allowlist 5 行、新增 checker、接入 freely-package 前置、跑 GREEN 与 9 个回归基线对比。
- revisit_trigger: 若未来把运行时必需文件迁出 `docs/system/workspace/` 顶层，或改用 manifest 驱动打包，另开 issue 调整 checker 的扫描范围；本 PR 以 `git ls-files` + 运行时字面引用为事实来源。
- acceptance_criteria:
  - 新打出的安装态含 5 个运行时文件，sha256 与真源一致。
  - 安装态执行 `freely-package` 自举打包成功且 `integrity: verified`。
  - 安装态 `worktree_seed.load()` 返回 `source=manifest`，条目数与真源一致（含 R5 的 3 条声明）。
  - 安装态 R5 seed parity checker 通过（`undeclared=[]`）。
  - 一致性检查能拦下「新增被运行时引用的 tracked 顶层文件但未加入 allowlist」，并点名路径。
  - 3 个纯文档/测试资料明确不随包；显式白名单机制保留；输出守卫与 R5 hook 顺序不变。
  - 9 个相关回归以未修改 develop HEAD 做基线对比，零新增失败。
- promotion_gate: AT-001 RED → GREEN + 9 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐条核对 17 个顶层 tracked 文件的运行时引用点，实证区分 SELF_ROOT 真源与 repo-scoped 清单（诚实修正 issue 正文）；核查 R5 checker 职责边界、输出守卫顺序、#4157 收敛意图；隔离 git 项目验证防复发拦截；真实安装态自举打包验证。
  - verdict: pass
- promoted_issue_id: I-20261106T100938Z-A
- promoted_issue_path: docs/B2-docs/gate/governance/raw-20261106T100938Z/issues/I-20261106T100938Z-A.md
- milestone: M-20261106T100938Z-A
- session_refs: []
