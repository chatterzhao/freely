---
candidate_id: C-20261105T062506Z-A
status: promoted
source_raw: raw-20261105T062506Z
created_at: 2026-11-05
milestone: M-20261105T062506Z-A
---

# Candidates

被否决的替代方案（把 bootstrap 改成 tracked 文件、把一致性检查做成打包后校验、批量改写历史工位、把 seed 条目设为 required=true）属于退化或越界，记录见 brainstorms.md，不作为 candidate 立项。

## C-20261105T062506Z-A: 补齐 seed 声明并建立 allowlist/seed 一致性检查

- candidate_format_version: v2
- title: seed manifest 声明 bootstrap，打包前置检查保证 gitignored 白名单条目都有 seed 声明
- status: promoted
- decision_reason: 根因是两份清单各自维护且无一致性约束。只补一条声明能修当下，但不能防止以后再漏；因此需要只读一致性检查作为打包前置。required=false 避免干净 clone 上新增硬失败。
- next_action: 写 AT-001 RED（真实工位打包缺文件），加 seed 声明 + checker + 打包前置调用，跑 GREEN 与 7 个回归基线对比。
- revisit_trigger: 若未来把 `.freely/` 中更多文件加入 allowlist，checker 会自动要求同步 seed；若改为 tracked，则另开 issue 调整检查语义。
- acceptance_criteria:
  - 由 seeder 创建的新工位无需人工复制即可跑通真实打包。
  - 新增未 seed 的 gitignored allowlist 条目被一致性检查拦下并点名路径。
  - 输出路径守卫及其顺序、allowlist 复制循环行为不变。
  - 7 个相关回归零新增失败。
  - 新 seed 条目 required=false（不新增硬失败点；不改变既有的 agent-table required=true 行为）。
- promotion_gate: AT-001 RED → GREEN + 7 个回归基线对比 + governance gate
- open_questions: []
- acceptance_reviews:
  - reviewer: session-self
  - mode: desk-research + executable-reproduction
  - summary: 逐行核对 allowlist 与 .gitignore，确认仅 1 条 gitignored 条目；核查 seeder apply 的 required 语义与路径守卫；确认 R2 物化 H1 在本轮自举生效；确认 #4201/#4151 已覆盖相邻现象。
  - verdict: pass
- promoted_issue_id: I-20261105T062506Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261105T062506Z/issues/I-20261105T062506Z-A.md
- milestone: M-20261105T062506Z-A
- session_refs: []
