# Brainstorms: raw-20261105T062203Z

## 问题

`wt-create` 恢复模式（`resume_mode=1`）补建缺失的 test-pre-merge 工位后，用 `freely_wt_resolve_target_path "$dev_branch"` 取 dev 工位路径，用在恢复摘要打印与 `_update_scan_state` 写入 `scan_state_worktree`。该函数的语义是「为**即将新建**的工位计算目标路径」：目标目录已存在时追加分支名 sha1 前 8 位后缀以避免冲突。恢复模式下 dev 工位本来就存在，因此必然返回带后缀、实际不存在的路径。

## 证据（本轮 RED 隔离仓库实测）

构造「dev 分支 + 真实 dev 工位在、test 分支缺」的恢复场景，运行同一 `wt-create` 命令：
- 恢复摘要打印 `dev (kept): .../fix-raw-20261105T062300Z-recovery-path-300efa56`（该目录不存在）；
- `.freely/run/manager-task-source-scan-latest.json` 的 `scan_state_worktree` 被写成同一错误路径；
- 真实 dev 工位路径无后缀。

与 issue #4191 的真实项目实测（`package-output-guard-0dd8a968`）完全同源。旧 AT-002 只断言 test 工位创建与初始化，没有断言 dev 路径解析，因此未捕获。

## 规模与边界评审

- 只改恢复块的 2 处调用；正常创建（`:948`）、test 工位新建（`:967`）、legacy 补建（`:1082`）仍用 `freely_wt_resolve_target_path`，它们确实是「新建」，需要冲突避让，**不得改动**。
- R3 已引入 `_wt_registered_dir()`（`git worktree list --porcelain` 反查 + `-d` 校验）与 `_dev_dir`，本轮直接复用同一真源，不新增第二套路径推导。
- 反查失败必须明确报错并退出，不得回退到猜测路径（issue 修复方向 2）。
- 反查结果与 pre-flight 的 `_dev_dir` 若不一致也报错，避免两个事实来源漂移。
- R2 物化 H1 在本轮再次自举验证通过；R3 四态判定、Q1/#4186 恢复与 legacy 补建、Q2 身份、R1 门禁批量化全部不退化。

## 关键设计

1. 恢复路径在写 scan state 前调用 `_wt_registered_dir "$dev_branch"` 得到 `_recovery_dev_path`；失败 → 打印「反查 dev 工位失败」并 `exit 1`。
2. 校验 `_recovery_dev_path == _dev_dir`，不一致 → 报错退出。
3. `_update_scan_state` 与恢复摘要 `dev (kept):` 均使用 `_recovery_dev_path`。
4. 行为回归测试覆盖：摘要路径存在且等于预建 dev 工位、scan_state_worktree 一致、test 工位仍完整初始化、二次重跑幂等。

## Related findings

- 无新增 raw issue：本轮发现的问题均已被现有 open issue 覆盖（#4201 顶层 return、#4151 预存红测试、#4192 seed 声明），或属本 issue 自身范围。未重复立项。
