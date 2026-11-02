# Tasks: I-20261102T113816Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | 观测三态化 + 有界重试 + 并行读 | `platform-adapter.py` | — | AT-001 / AT-002 |
| T2 [x] | receipt 增加 decision/degraded/debt，默认语义不变 | `raw_reconciliation.py` | T1 | AT-003 / AT-004 |
| T3 [x] | gate 增加 --allow-degraded（仍只读） | `raw-reconciliation-gate.py` | T2 | AT-005 |
| T4 [x] | 债账本 record/list/clear | `sync-debt.py` | T2 | 手工往返：record→list→clear |
| T5 [x] | wt-create 接降级通道并记账 | `wt-create` | T3 / T4 | 语法检查 + 降级 receipt 落账 |
| T6 [x] | 回归与证据 | `verification/test-evidence/*` | T1–T5 | 三份测试日志 + 四份 gate receipt |

## 备注

- T6 不新增第 5 个测试文件：既有 `test-raw-reconciliation.py` 更新了一条断言（把 `diagnostics[0].code == error` 换成更强的 `decision == block` + `degraded` 断言），语义没有放宽。
- `pull_raw_issue`（materialize）保持严格：该路径没有本地副本可核对，不接 `allow_degraded`。
