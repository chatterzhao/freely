# Tasks: I-20261102T133249Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | wiring 回归测试（守卫 + stderr） | `test-owner-lane-claim-wiring.py` | — | AT-001 |
| T2 [x] | 删除路径守卫、捕获失败原因 | `runtime/freely` | T1 | AT-001 / AT-003 |
| T3 [x] | 同路径两条锁定用例 | `test-owner-lane-claim.py` | — | AT-002 |
| T4 [x] | 新工位自建 `.freely/run` | `runtime/freely` | — | AT-003 |
| T5 [x] | 真实工位 daemon 启动验证 | 证据日志 | T2 / T4 | AT-003 |

## 备注

- T4 不在最初 candidate 范围内：首次真实验证时 db daemon 因 `.freely/run` 不存在而失败（`db-daemon.log: No such file or directory`）。属同一目标“daemon 能否在工位里跑起来”的断面，并入本 issue。
- 未处理：`daemon stop` 在启动失败后仍写 `TEST_STATUS=completed`（另立 raw）。
