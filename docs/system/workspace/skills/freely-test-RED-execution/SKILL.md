---
name: freely-test-RED-execution
description: TDD RED 阶段——B2 之后、dev 之前。执行 pre-tests.md 中全部测试，确认全部 RED（失败），证明 bug 可复现（fix）或功能未实现（feature）。不通过 RED 绝不允许写一行实现代码。
---

# skill:freely-test-RED-execution

> 全链路: B2(写pre-tests) → RED(确认全红) → dev(实现) → GREEN(全绿) → test-pre-merge → pr
>                      [本 skill 自此开始 — 执行 RED，确认全部测试真的会失败]

## 定位

**RED skill 是 TDD 的第一道闸门。** B2 写好了 pre-tests.md，但这只是"纸面计划"。RED 阶段验证这些测试是真实的、能确实失败的——不是形同虚设的摆设。

- **fix RED** = 确认 bug 可复现。bug 不存在 → 测试无意义。
- **feature RED** = 确认功能未实现。功能已存在 → 测试设计错了。

**不通过 RED，绝不允许进入 dev 写实现代码。**

## 输入

1. B2 产出的 `pre-tests.md`（全部 `red-green-status: pending`）
2. raw issue（fix: 理解 bug；feature: 理解功能需求）
3. 分支类型（`fix/*` 或 `feature/*`，从分支名自动判定）

## 职责

- 设计能失败的测试（如果 pre-tests 中缺少具体 test_command）
- 逐条执行，确认真的 FAIL
- 记录 RED 证据（actual_RED_output、red_how）
- 更新 pre-tests.md：`red-green-status: pending → red`

## 不负责

- 不写 pre-tests.md（B2 负责）
- 不写实现代码（dev-loop 负责）
- 不跑 GREEN（GREEN 阶段在 dev 之后，由 `skill:freely-test-execution` 负责）

---

## fix RED：确认 bug 可复现

```
核心问题：这个 bug 真的存在吗？能稳定复现吗？

1. 读 raw issue → 理解 bug 现象和影响范围
2. 读 pre-tests.md → 逐条 acceptance item:
   a. 已有 test_command → 直接执行
      - FAIL → ✅ red-green-status = red，记录 actual_RED_output
      - PASS → ❌ 测试有问题：bug 已修复 / 测试没测到真正的 bug → 回 B2 修
   b. 没有 test_command → 设计复现测试，写入 test_command，然后执行
   c. 测试层级不足以复现 → 补充手工端到端复现步骤到 red_how
3. 全部 red（或合理 not_applicable）→ 进入 dev

RED 证据要求（red_how 字段）:
- 已有测试: "使用 {test_name} 复现，执行结果: {actual_RED_output}"
- 新测试: "设计 {test_type} 测试，步骤: {steps}，执行结果: {actual_RED_output}"
- 手工端到端: "手工复现步骤: 1. ... 2. ... 3. ... 预期看到: {bug_现象}，实际看到: {actual_RED_output}"
```

## feature RED：确认功能未实现

```
核心问题：功能真的还没做吗？测试设计充分吗？

设计原则（按重要度，必须自上而下）:
  1. 端到端（E2E）：用户可见的完整业务流程。必须设计。AI 代码出错最多的层级。
  2. 集成：多模块协作、数据流。改 A 模块容易无意破坏 B 模块。
  3. 单元：单一函数/脚本验证。快速定位，不能替代上面两层。

1. 读 pre-tests.md → 检查每条 acceptance item:
   a. 缺少 test_command → 按上述原则设计测试，补到 test_command
   b. 测试层级不合理（只有单元没有端到端）→ 补充端到端测试
2. 确认测试设计打分:
   - 没有端到端测试 → ❌ 设计不完整，回 B2 补
   - 端到端覆盖了用户可见行为 → ✅ 可以进入 RED 执行
3. 逐条执行:
   - FAIL → ✅ red-green-status = red，记录 actual_RED_output
   - PASS → ❌ 功能已经存在 / 测试写错了 / 测试太弱 → 回 B2 修
4. 全部 red（或合理 not_applicable）→ 进入 dev

RED 证据要求（red_how 字段）:
- E2E: "端到端测试 {test_name}，覆盖 {user_visible_behavior}，设计理由: {why_this_matters}"
- 集成: "集成测试 {test_name}，覆盖 {module_boundary}，设计理由: {data_flow_risk}"
- 单元: "单元测试 {test_name}，覆盖 {function_signature}，设计理由: {edge_case}"
```

---

## 工作流

```
1. 确认上下文:
   - 当前在 fix 或 feature 工位
   - pre-tests.md 存在，全部 red-green-status = pending
   - 分支名可判定 fix/feature

2. 逐条处理 acceptance item:

   for each item in pre-tests.md:
     a. 读 requirement → 理解要测什么
     b. 如有 test_command → 直接执行
        如无 → 按 fix/feature 方式设计
     c. 记录 expected_RED_output（即: 期望看到什么 FAIL）
     d. 执行，记录 actual_RED_output
     e. 判定:
        - 真的 FAIL → red-green-status = red ✅
        - 意外 PASS → 回 B2 修 pre-tests ❌
     f. 填写 red_how

3. 全部 red 后，更新 pre-tests.md，git commit

4. 进入 skill:freely-dev-loop-execution（dev 实现阶段）
```

---

## 硬拦截

| 情况 | 处理 |
|------|------|
| pre-tests.md 不存在 | 回 B2 |
| 有一条 red-green-status != pending | 检查是否已执行过 RED |
| 测试意外 PASS（fix: bug 不复现；feature: 功能已存在） | 回 B2 修 pre-tests |
| feature 没有端到端测试 | 回 B2 补充端到端设计 |
| 全部 not_applicable | 疑似糊弄，回 B2 设计真实测试 |

---

## 完成后

```
全部 red-green-status = red（或合理 not_applicable）
→ git commit -m "test(RED): pre-tests RED confirmed — <fix: bug可复现 / feature: 功能未实现>"
→ 进入 skill:freely-dev-loop-execution
```

## 与上下层 skill 的关系

| 上游 | 本 skill | 下游 |
|------|----------|------|
| `freely-doc-B2_IBM-execution`（写 pre-tests，pending） | 执行 RED，确认全红 | `freely-dev-loop-execution`（写代码实现） |
