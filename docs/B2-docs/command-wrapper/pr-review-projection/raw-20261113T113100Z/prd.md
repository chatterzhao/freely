# PRD: 评审 skill 新增 L0 项目意图一致性锚点

- issue_id: I-20261113T113100Z-A
- source_raw: raw-20261113T113100Z
- workflow_kind: feature
- milestone: M-20261113T113100Z-A
- story: command-wrapper/pr-review-projection（复用既有 story）

## 目标

给 `freely-tdd-review` 补上「以项目既有资产为锚」的 L0 审查层，使
「四层全绿但整体漂移」的实现无法再通过评审。只改评审权威指南 + 加 AT，
不改 verdict 契约、不改 `pr-review-guarded` 判定逻辑、不改任何门禁。

## 唯一改动范围

- `docs/system/workspace/skills/freely-tdd-review/SKILL.md`：新增 L0（锚点清单 / Q1–Q5 / 四段举证 / 失败判据 / 三个真实案例）、输出格式加 L0 段、门禁分工表加两行。
- 新增 AT `docs/system/workspace/scripts/tests/test-review-intent-anchor.py`，`bin/test-all` 双数组各 +1。

## 不退化边界

- 四层审查内容不变；`pr-review-guarded` 与 `review_verdict` 契约不变；
- 不新增强制 lint 字段（避免「补字段就过」）；不放宽任何门禁；
- 不把 skill 变更伪装成 doc-only（`.freely/config.toml [skip_ibm_gate].allowed_paths` 不含 skills/）。

## 功能需求

- FR-1：L0 位于四层之前，明确「四层自洽不能替代项目一致」。
- FR-2：外部锚点清单包含设计文档 / 既有验收测试 / 门禁源码注释 / 既有同类实现 / 配置约束。
- FR-3：Q1–Q5 五个必答问题，任一不通过即整体 fail。
- FR-4：门禁改动四段举证（当初为什么 / 现在为什么 / 判定 / 强度不降）。
- FR-5：失败判据含「用补数据/补字段让门禁通过」。
- FR-6：真实案例 R33.8 / R33.9 / R33.10 回填，不虚构。
- FR-7：输出格式含 `## L0：项目意图一致性` 段。

## 验收

AT-001 RED `1 ok / 19 failed`（develop `52b095892` 快照）→ GREEN `20 ok / 0 failed`；
`bin/test-all --ci` 全绿；四层与 verdict 契约零改动。
