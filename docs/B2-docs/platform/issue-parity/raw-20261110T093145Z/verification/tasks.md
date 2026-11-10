# Tasks: raw H1 判定改为代码块感知
- issue_id: I-20261110T093145Z-A
- pre_tests_path: docs/B2-docs/platform/issue-parity/raw-20261110T093145Z/verification/pre-tests.md

## 任务分解

- [x] T1: 前置评审否掉立项假设 —— `git log -L` 找到既有 H1 注入逻辑（#4181）、`raw_title_contract` 单一所有者、`test-materialize-h1` 护栏；比对 #4264/#4269 物化差异，定位精确根因为三处裸正则不排除 fenced code block。
- [x] T2: 写 AT-001（6 静态 + 4 单元 + 4 行为），基线确认 RED `2 ok / 12 failed`（gate 借代码注释当 title）。
- [x] T3: `raw_title_contract` 新增 `find_local_heading`（``` / ~~~ 围栏感知，返回标题 + 结束偏移）。
- [x] T4: 物化侧 / gate 侧 / backfill 两处全部复用；gate 加 `missing_local_title` 显式诊断。
- [x] T5: GREEN `14 ok / 0 failed`；修一处返工（backfill 的 `--apply` 幂等复检漏改，导致既有套件 18 项中 1 项红）；10 项回归全绿。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
