# Tasks: 跨进程数据契约（第一阶段）
- issue_id: I-20261104T075857Z-A
- pre_tests_path: docs/B2-docs/data-contracts/cross-process-contract/raw-20261104T075857Z/verification/pre-tests.md

## 任务分解

- [x] T1: 进已建工位（不重复 `wt-create`）；真源普查证伪 issue 旧描述（22 处而非 52 处、位置参数已由 R26 修过、`state_file.py` 已存在）。
- [x] T2: 前置评审把「22 处归零」收敛为「契约声明 + 三态 runner + lint」；写 AT-001（14 静态 + 3 行为）。
- [x] T3: develop `c159e6cef` 基线 RED `0 ok / 17 failed`（`git archive` 快照 + 最终版 AT）。
- [x] T4: `contracts/cross-process/contract.yaml`（state 协议/错误信封/退出码 0–4/四 kind/超时/4 条边界/known_gaps）+ 单页 README。
- [x] T5: `quality/cross_process_boundary.py` 三态边界（缺字段 3、类型错 3、超时 4）；`bin/check-cross-process-contract`（0/1/2）。
- [x] T6: AT 接入 `CORE`/`CI_CORE`；`epic-runtime` 注册 `cross-process-contract` story（40 story，其后整体 +18）。
- [x] T7: GREEN `17 ok / 0 failed`；lint `ok (4 boundaries)`；`test-all --ci` 18/0。
- [x] T8: `known_gaps` 写清 22 处夹具、33 处 `|| echo`、消费方机检三项留后续轮次。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T3 | AT-001（RED fidelity） |
| T4 | AT-001（静态 1–9） |
| T5 | AT-001（静态 10–11、14 + 行为 15–17） |
| T6 | AT-001（静态 12–13） |
| T7, T8 | 回归/CI 与范围标注 |
