# Tasks: I-20261104T074512Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | RED：守卫测试 | docs/system/workspace/scripts/tests/test-freely-package-output-guard | — | AT-001 |
| T2 [x] | 实现 refuse_dangerous_output 并接入 rm 之前 | bin/freely-package | T1 | AT-001 |
| T3 [x] | 真实 RED/GREEN 证据落盘 | verification/test-evidence/AT-001-RED.log, AT-001-GREEN.log | T2 | AT-001 |
