# PRD: B1 增设计意图审计层

- issue_id: I-20261114T031605Z-A
- source_raw: raw-20261114T031605Z
- workflow_kind: feature
- milestone: M-20261114T031605Z-A
- story: command-wrapper/pr-review-projection（复用既有 story）

## 目标

把「拿到 raw 先判断设计/实现/缺陷属于哪一类」前移到 B1 立项阶段，避免动手后才在 review L0 发现方向错、返工成本已付。

## 唯一改动范围

- `docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md`：
  - B 阶段新增 **B0：设计意图审计**（位于价值审视之后、发散之前）：外部锚点原文（五类）、五分类判定、冲突、影响面、全局适配四问、与 review L0 分工、不做硬门禁的声明；
  - `brainstorms.md` 模板加 `## 0. 设计意图审计` 与 `## 0.1 全局适配反思`；
  - `candidates.md` 模板加 `design_verdict` / `anchor_refs`；
  - 「完成自检」加两项（§0 与锚点 ≥2、candidate 两字段且与 §0 一致）。
- 新增 AT `test-b1-design-intent-audit.py`，CORE/CI_CORE 各 +1；`projection.lock` 重录。

## 不退化边界

- 不改 `freely-tdd-review` L0 五问与失败判据；不改 verdict 契约；
- **不新增硬门禁**、不新增跳过通道、不修改 `governance-merge-gate`（AT S15 断言）；
- 不追溯校验历史 raw 文档；
- 若未来升级为门禁，必须校验锚点逐字命中原文，不得只查字段存在。

## 功能需求

- FR-1：B0 存在且位于发散之前。
- FR-2：四类外部锚点 + 五分类判定 + 冲突 + 影响面，且要求引用原文。
- FR-3：全局适配四问（类别 / 职责边界 / 结构性冲突 / 门禁失配）。
- FR-4：brainstorms 模板含 §0 / §0.1；candidates 模板含 `design_verdict` / `anchor_refs`。
- FR-5：完成自检加两项并校验 design_verdict 与 §0 一致。
- FR-6：明确「不做硬门禁」及其理由；L0 分工说明。
- FR-7：**自举**——本轮自己的 brainstorms/candidates 必须遵循 B0（AT S17–S20）。
- FR-8：基线（develop）在 FR-1..FR-7 上必须红。

## 验收

AT-001 GREEN `31 ok / 0 failed`；基线 `3 ok / 28 failed`；`bin/test-all --ci` 全绿；`check-skill-frontmatter` 仍绿。
