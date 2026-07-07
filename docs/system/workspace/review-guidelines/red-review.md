# RED 阶段审查指南

## 定位

RED 是 TDD 的第一道闸门。Reviewer 检查：Worker 是否真的执行了 pre-tests，测试是否真的失败了（confirm RED），actual_RED_output 是否真实（不是占位符）。

## 检查项

### 1. RED 执行真实性
- [ ] 每条 acceptance item 的 actual_RED_output 是否填写了真实执行结果（不是 "(执行后填写)" 或占位符）？
- [ ] actual_RED_output 的内容是否合理（描述了具体的失败现象，不是 "FAIL" 或 "test failed" 这种无意义文本）？
- [ ] red_how 字段是否描述了怎么确认 RED 的（fix: 是否复现了 bug？feature: 测试设计理由是否充分）？

### 2. RED 一致性
- [ ] 是否有意外 PASS（expected_RED 但 actual 却 PASS）→ 测试设计有问题，需要回 B2 修
- [ ] fix: 确认 bug 可复现（bug 不存在 = 测试无意义）
- [ ] feature: 确认功能未实现（功能已存在 = 测试设计错了）

### 3. 覆盖完整性
- [ ] 是否有 acceptance item 被标记为 not_applicable？→ 检查理由是否充分
- [ ] feature 是否至少有一条端到端测试？→ 没有 = 设计不完整
- [ ] 全部 not_applicable → 疑似糊弄 → FAIL

## 通过标准

全部 actual_RED_output 真实且 RED 一致 → `PASS`。
actual_RED_output 为占位符 → `FAIL, reason=AT-00X 的 actual_RED_output 是占位符，请真实执行测试并记录失败输出`。
有意外 PASS → `FAIL, reason=AT-00X 预期 RED 但实际 PASS，说明测试设计有问题或功能已存在`。

## 失败处理

输出具体失败项 → Worker 回到 RED 重新执行 → 重新提交审查。
