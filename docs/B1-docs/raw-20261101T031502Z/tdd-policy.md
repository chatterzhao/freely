---
analysis_id: TDD-20261101T231000Z
phase_state: in_progress
topic: Freely TDD 的强制边界
created_at: 2026-11-01
---

# TDD 政策：哪些必须真跑，哪些可以 not_applicable

## 0. 现状

- `pretests-gate` 在完成/PR 前要求每个 Acceptance Item 的 `red-green-status` 为 `green` 或合法 `not_applicable`。
- 它检查 `not_applicable_reason/explanation/replacement_evidence`，但不检查“至少一个真实 test_command/pass”，也不检查 `actual_RED_output` 是否真实。
- “全部 not_applicable 是糊弄”只写在 `freely-test-execution` skill，不是代码门禁。
- 历史资产：431 份 pre-tests，327 份出现 not_applicable，247 份无 test_command（含旧 schema/纯文档）。

结论：**TDD 目前是“终态证据门禁 + 流程约束”，不是“每个改动都硬 TDD”。** 这既不是完全失效，也不是完全硬保证。

## 1. 问题不是“要不要 TDD”，而是“按改动面分级”

如果把所有改动都要求可执行测试，docs-only/配置/元数据会被迫造假测试；如果允许随便 not_applicable，TDD 就退化成填表。

需要的是**改动面声明 + 分级验收**：

| 改动面 | 示例 | 最低验收 |
| --- | --- | --- |
| docs/spec | README、B1/B2、PRD | 链接/结构/引用校验；可 not_applicable 可执行测试 |
| config/metadata | config.toml、milestone、phase | 解析/一致性校验；不是“无测试” |
| script/runtime | bin、runtime、adapter | 至少一个可执行测试；优先端到端 |
| agent/skill/prompt | skill、agent 定义、prompt | 行为回放/结构校验；不能只靠“读起来对” |
| UI/GUI | 前端、Tauri | 交互验证/截图/端到端；不能只靠单测 |

## 2. 三种可选策略

### Option A：硬门禁“至少一个真实 test_command”

- 所有 issue 至少一个 acceptance item 有可执行 test_command + passed。
- 优点：简单、可验证。
- 缺点：docs-only 会被迫写假测试；不适用于纯文档。

### Option B：改动面声明 + 分级（推荐方向）

- B2 在 PRD/pre-tests 声明 `change_surface`（docs/config/script/runtime/agent/ui）。
- 不同 surface 有不同最低验收；docs-only 允许全 not_applicable，但必须有结构/链接/引用校验证据。
- 代码类 surface 至少一个可执行测试；agent/skill 类至少一个行为回放或结构校验。
- 优点：不逼造假，也不给代码类放水。
- 缺点：需要 schema、skill 与 gate 同步；surface 声明可能被误用。

### Option C：只靠 Reviewer 判断

- gate 只查格式，Reviewer 判断测试是否足够。
- 优点：灵活。
- 缺点：Reviewer 负担大、不可复现；容易变成“看心情”。

## 3. 推荐：Option B + 两个硬约束

1. **代码类 surface 至少一个可执行 test_command + passed**；`not_applicable` 不能覆盖整个代码类 issue。
2. **docs/config 类允许全 not_applicable，但必须有可执行的替代校验**（链接检查、解析、schema 校验），不能只写“不适用”。

另外两条“软约束”交给 Reviewer：

- `actual_RED_output` 是否真实（现在 gate 不查）。
- 测试是否只覆盖 happy path（需要 reviewer 看断言）。

## 4. 与 Super-agent 的对比

- Super-agent 没有 TDD 门禁；Worker 自己决定测试，CI 是外部。它更快，但无法防止“AI 自证”。
- Freely 的 GREEN 门禁是真实优势；但“全 not_applicable 只由 skill 约束”是可见的绕过面。
- 结论：**Freely 应保留 TDD，但改成按改动面分级；不要用“全部 not_applicable”作为默认逃生门。**

## 5. 度量

- 每个 issue 的 `surface` 与 `not_applicable` 比例。
- 代码类 issue 中“至少一个可执行测试”的比例。
- `actual_RED_output` 为占位符的比例。
- Reviewer 打回“测试不足”的比例。
- 这些指标应先采样，再决定是否加硬门禁。

## 6. 未解

- `change_surface` 由谁声明、谁校验？B2 还是 runtime？
- docs-only 的“替代校验”是否足够（链接/结构）？
- 是否要检查提交顺序（先 RED 后实现）？成本高、且可被 rebase 打乱。
- 是否要求测试失败过一次（negative control）？对 AI 生成的测试尤其重要，但实现复杂。
