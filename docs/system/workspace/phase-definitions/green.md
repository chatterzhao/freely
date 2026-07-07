# GREEN 阶段定义

## 是什么

TDD 最后闸门——在 test-pre-merge 工位执行 pre-tests 确认全部通过。

## 输入

- dev 实现完成的代码（已 commit + merge 到 test 工位）
- pre-tests.md

## 输出

- pre-tests.md 更新（red-green-status: red → green）
- 每条 AT 的 actual_output 填写真实执行结果
- evidence_file 指向的测试证据文件
- test-gate.env: TEST_STATUS = completed

## 完成标志

- 全部 AT 的 red-green-status = green
- 全部 actual_output 是真实输出
- test-gate.env 的 TEST_STATUS = completed
- 无 ghost pass（status=pass 但 actual_output 为空）

## 完成后做什么

**调用 A2A PATCH state=input-required, reason=needs-review:test**

Reviewer 按 `review-guidelines/green-review.md` 检查证据真实性。
pass → 可以提 PR（pr-create-guarded）。fail → 修复后重新 GREEN。
