# B1 Candidates — raw-20261114T031605Z

## C-20261114T031605Z-A：B1 增设计意图审计层

- status: promoted
- promoted_issue_id: I-20261114T031605Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261114T031605Z/issues/I-20261114T031605Z-A.md
- milestone: M-20261114T031605Z-A
- kind: feature
- decision: 方案 A——`freely-doc-B1_IBM-execution/SKILL.md` 新增 B0（外部锚点原文 + 五分类判定 + 冲突 + 影响面 + 全局适配四问），brainstorms 模板加 §0，candidates 模板加 `design_verdict`/`anchor_refs`，完成自检加两项；新增 AT 防回退；**不新增硬门禁**。
- design_verdict: 设计不完整 + 实现未完成
- anchor_refs: `freely-doc-B1_IBM-execution/SKILL.md:45-51`（B 阶段原文）；`freely-tdd-review/SKILL.md` L0 段（「四层自洽不能替代项目一致」）；`governance-merge-gate:1500`（只校验 B1 产物存在）
- 范围:
  1. `docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md`：B 阶段新增 B0（位于价值审视之后、发散之前）；brainstorms/candidates 两个模板同步；完成自检加两项；新增「与 review L0 分工」说明。
  2. 新增 AT `test-b1-design-intent-audit.py`，CORE/CI_CORE 各 +1。
  3. `projection.lock` 重录（若 skill 变更影响 delegate 投影校验）。
- 验收:
  - skill 含 B0 段、五分类、四类锚点、全局适配四问、§0 模板；
  - B0 在「发散/Brainstorm」之前；
  - candidates 模板含 `design_verdict` / `anchor_refs`，完成自检含对应两项；
  - 自举：本轮 brainstorms.md 含 §0 与四问、candidates.md 含两个字段；
  - 不新增 `pr-create-guarded` 硬门禁（静态断言 skill 未声明硬门禁、gate 代码零改动）；
  - 基线（develop）各条红。
- 不退化边界:
  - 不改 `freely-tdd-review` L0 五问与失败判据；不改 verdict 契约；
  - 不新增硬门禁、不新增跳过通道；
  - 不追溯校验历史 raw 文档。
