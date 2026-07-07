# RED 阶段定义

## 是什么

TDD 第一道闸门——执行 pre-tests 确认全部失败。

## 输入

- B2 产出的 `pre-tests.md`（全部 red-green-status: pending）
- raw issue（fix: 理解 bug；feature: 理解功能需求）

## 输出

- pre-tests.md 更新（red-green-status: pending → red）
- 每条 AT 的 actual_RED_output 填写真实执行结果
- red_how 字段描述确认 RED 的方式

## 完成标志

- 全部 AT 的 red-green-status = red（或合理 not_applicable）
- 所有 actual_RED_output 是真实输出，不是占位符
- fix: bug 可复现。feature: 功能确认未实现

## 完成后做什么

**调用 A2A PATCH state=input-required, reason=needs-review:red**

Reviewer 按 `review-guidelines/red-review.md` 检查 RED 真实性。
pass → 进入 dev。fail → 修复测试或回 B2 修正测试设计。
