# B1 Candidates — raw-20261113T113100Z

## C-20261113T113100Z-A：评审 skill 新增 L0 项目意图一致性锚点

- status: promoted
- promoted_issue_id: I-20261113T113100Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T113100Z/issues/I-20261113T113100Z-A.md
- milestone: M-20261113T113100Z-A
- kind: feature
- decision: 只改评审权威指南 `freely-tdd-review/SKILL.md`（新增 L0 层 + 输出格式 + 真实案例）并加 AT；不改 verdict 契约、不改 `pr-review-guarded` 的判定逻辑、不改任何门禁。
- 依据：brainstorms §1（四层只审 fidelity 的结构性盲区）、§2（L0 定义）、§3（真实案例）、§4（方案 A）。
- 范围：
  1. `docs/system/workspace/skills/freely-tdd-review/SKILL.md`：
     - 核心方法之前新增 **L0：项目意图一致性 / 设计漂移检测**；
     - 外部锚点清单（设计文档 / 既有验收测试 / 门禁源码注释 / 既有同类实现 / 配置约束）；
     - 五个必答问题 Q1–Q5（冲突、门禁强度、能力降级、第二套语义、设计漂移）；
     - 门禁改动四段举证责任；
     - 失败判据（任一命中即 fail）；
     - 输出格式新增 `## L0：项目意图一致性` 段；
     - 真实案例：R33.8 / R33.9 / R33.10。
  2. 新增 AT `docs/system/workspace/scripts/tests/test-review-intent-anchor.py`，接入 CORE/CI_CORE。
- 验收：
  - skill 含 L0 标题、五项必答、外部锚点、四段举证、失败判据、输出段、三个真实案例；
  - L0 位于四层之前（顺序断言）；
  - 负向控制：develop 基线 skill 不含 L0，AT 必须判红；
  - `bin/test-all --ci` 全绿；不动 `pr-review-guarded` / `review_verdict` / 任何门禁。
- 不退化边界：
  - 四层审查内容不改；`pr-review-guarded` 与 `review-verdict` 契约不改；
  - 不新增 lint 强制字段，避免「补字段就过」；
  - 不把 skill 变更伪装成 doc-only（配置明确不允许）。
