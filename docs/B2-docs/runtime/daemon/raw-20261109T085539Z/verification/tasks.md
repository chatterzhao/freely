# Tasks: worker 派发 JSON 化 + 边界 lint
- issue_id: I-20261109T085539Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261109T085539Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真源普查——TSV 唯一消费点、4 处 `IFS=$'\t'` 分辨、20 读/15 写状态文件、154 处 `python3 -c`；决定 scope 收敛并拆 #4252。
- [x] T2: 写 AT-001（5 静态 + 2 对照 + 9 行为），完整 develop 基线确认 RED `3 ok / 13 failed`。
- [x] T3: 实现 JSON Lines 发射、NUL 解码、派发循环改造、boundary lint。
- [x] T4: GREEN `16 ok / 0 failed`；真机 bash 冒烟；6 回归基线对比 0 新增失败；拆分协议迁移 issue 并排期。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
