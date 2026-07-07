# Dev 阶段审查指南

## 定位

Dev 是实现阶段。Reviewer 检查：代码是否按照 pre-tests 的指导来驱动实现（TDD），实现是否忠实于 prd 和 tasks 的设计，是否产生了 scope creep。

## 检查项

### 1. TDD 忠实度
- [ ] 代码是否严格按照 pre-tests 的测试指导来驱动（每条 AT 对应实际代码改动）？
- [ ] RED 阶段的 actual_RED_output 是否在 dev 后被对应的代码改动覆盖？
- [ ] 实现顺序是否正确（B1→B2→RED→dev→GREEN 提交顺序）？

### 2. PRD 忠实度
- [ ] prd 的每个模块/改动点是否在 diff 中有对应实现？
- [ ] 是否有 prd 没有描述的功能（scope creep）？
- [ ] prd 描述的功能是否有遗漏？

### 3. Tasks 完整性
- [ ] tasks.md 的每个子任务是否在 diff 中有对应变更？
- [ ] 未完成的 task 是否有明确标注？
- [ ] task 是否有对应的 code-review evidence？

### 4. Code Review Evidence
- [ ] code-reviews/ 目录是否有 Implementation Decision Note？
- [ ] IDN 的 5 字段是否具体反映了本次实现？
- [ ] 代码质量（聚焦性、commit 消息规范性）是否合理？

## 通过标准

全部检查项通过 → `PASS`。
有 scope creep → `FAIL, reason={文件} 实现了 prd 未描述的功能，需要移除或更新 prd`。
prd 描述的功能遗漏 → `FAIL, reason=prd 中的 {功能} 在 diff 中没有对应实现`。
tasks 有未完成项无标注 → `FAIL, reason=tasks.md 中 {任务} 标记完成但无对应代码变更`。

## 失败处理

输出具体失败原因 + 建议修复方向 → Worker 回到 dev 修复 → 重新提交审查。
