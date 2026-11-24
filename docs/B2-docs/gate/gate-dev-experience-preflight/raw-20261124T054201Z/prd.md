# PRD: test-all 失败诊断
- issue_id: I-20261124T054201Z-A

## Goal
CI 失败时提供可定位的断言证据，使 AI 能自主诊断→修复→验证，而不是盲改或人工重跑。

## 实现方案
1. `bin/test-all` 执行循环：每个测试的 stdout/stderr 写入独立日志（如 `.freely/run/test-all-logs/<name>.log`），不再 `>/dev/null 2>&1`。
2. 成功：删除或保留空日志（默认清理），只打印 `[ok]` 与 SUMMARY——格式不变。
3. 失败：打印 `[FAIL] name (rc=N)` + 日志尾部关键行（如最后 40 行，含 Traceback/FAIL/SUMMARY 断言），并保留完整日志到可预测路径。
4. 每个测试记录耗时（可选，若易实现）与退出码（已有 rc）。
5. 日志目录在每次运行开始时清理上一次残留，避免陈旧证据。

## 不退化边界
- SUMMARY 行格式与退出码语义完全不变（下游 test-gate / pretests-gate / AT 依赖）。
- known-broken 清单打印不变。
- 不改任何被测测试、不改 gate 判据。

## Dev-Loop Handoff
见 pre-tests.md。RED：构造必然失败的测试，基线只显示 `[FAIL]` 无断言；GREEN：显示断言细节且 SUMMARY 不变。
