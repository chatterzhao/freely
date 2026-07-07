# GREEN 阶段审查指南

## 定位

GREEN 是 TDD 的最后一道闸门。Reviewer 检查：pre-tests 是否全部执行、执行结果是否真实、evidence 是否可追溯、tasks 是否全部完成。

## 检查项

### 1. 测试全 GREEN
- [ ] 每条 acceptance item 的 red-green-status 是否为 green（或合理 not_applicable）？
- [ ] 是否有 failed 的项？
- [ ] 是否所有项都是 pending（根本没跑）？

### 2. 证据真实性（重点——堵 ghost pass）
- [ ] 每条 passed 的 actual_output 是否真实执行结果（不是占位符或 "(执行后填写)"）？
- [ ] evidence_file 指向的文件是否存在且内容合理？
- [ ] 是否存在 "status=pass 但 actual_output 为空" 的 ghost pass？
- [ ] 是否存在 "全部 not_applicable 且理由三个字'不适用'" 的糊弄？

### 3. Tasks 完成度
- [ ] tasks.md 的每个子任务是否标记 [x] 完成？
- [ ] 未完成的 task 是否有明确的阻塞说明？

### 4. test-gate.env
- [ ] test-pre-merge 工位的 test-gate.env 的 TEST_STATUS 是否为 completed？
- [ ] LAST_TESTED_COMMIT 是否与当前 test 工位 HEAD 一致？

## 通过标准

全部检查项通过 → `PASS`。
有 failed 项 → `FAIL, reason=AT-00X 测试失败: {actual_output}。回 dev 修复后重新 GREEN`。
有 ghost pass → `FAIL, reason=AT-00X 的 actual_output 为空但 status=pass，这是 ghost pass。执行真实测试并记录输出`。
全部 not_applicable 且理由敷衍 → `FAIL, reason=pre-tests 疑似糊弄——全部 not_applicable 但理由不充分。至少需要一条真实测试`。

## 失败处理

输出具体失败项 + 证据 → 回 dev-loop 修复 → 修复后重新 merge 到 test → 重新 GREEN → 重新审查。
