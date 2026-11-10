# Tasks: execution-network 族迁移到安全协议
- issue_id: I-20261110T081029Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T081029Z/verification/pre-tests.md

## 任务分解

- [x] T1: 按形态 + 状态文件两维度重扫 54 处 source；否掉恢复点建议的 manager_worker_launch 族（11 键不在白名单 + 55 测试耦合），选 execution-network 族。
- [x] T2: 写 AT-001（5 静态 + 6 行为，source 真实 freely），基线确认 RED `4 ok / 7 failed`（注入 PoC 真的创建 marker）。
- [x] T3: 写侧改 `write --kv`；两处读者改 `values`（bash 3.2 用 `read`，不用 `mapfile`）。
- [x] T4: 耦合测试 3 处 grep 格式断言改为协议读值；两族 AT 的 lint 计数断言改单调守卫。
- [x] T5: GREEN `11 ok / 0 failed`、source 54→52、回归全绿；立项 #4264（白名单漏 21 键）并排进 goal。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
