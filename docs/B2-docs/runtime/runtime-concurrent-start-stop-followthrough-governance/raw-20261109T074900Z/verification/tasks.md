# Tasks: pkill -f 项目路径正则转义
- issue_id: I-20261109T074900Z-A
- pre_tests_path: docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/raw-20261109T074900Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真源普查——5 处 pkill 定位、仅 2 处含项目路径；面 1/2 的符号在最新 develop 零命中（行号漂移），决定 scope 收敛并拆 #4254。
- [x] T2: 写 AT-001（4 静态 + 2 对照 + 6 行为，含真实 pgrep 反向 PoC），完整 develop 基线确认 RED `5 ok / 7 failed`。
- [x] T3: 实现 `freely_escape_regex()` 单一 helper 与两处站点接线。
- [x] T4: GREEN `12 ok / 0 failed`；5 回归基线对比 0 新增失败；拆分 issue 并排期。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
