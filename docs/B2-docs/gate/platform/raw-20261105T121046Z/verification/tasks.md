# Tasks: 安装态版本可证明且与 develop 同步
- issue_id: I-20261105T121046Z-A
- pre_tests_path: docs/B2-docs/gate/platform/raw-20261105T121046Z/verification/pre-tests.md

## 任务分解

- [x] T1: 真机复现安装态落后（PACKAGED_FROM=444985f50 vs develop c1949aa24），逐行核对 freely-package / pr-merge-guarded / cmd_doctor / FREELY_HOME。
- [x] T2: 写 AT-001（10 静态 + 13 行为），develop 基线快照确认 RED `2 ok / 21 failed`。
- [x] T3: 新增 install_state.py 唯一真源 + install-state-check.py CLI。
- [x] T4: freely-package 写 hash 清单、auto 版本、原子激活、幂等。
- [x] T5: pr-merge-guarded followthrough + cmd_doctor 接线。
- [x] T6: GREEN `23 ok / 0 failed` + 21 个回归基线对比。
- [x] T7: B1/B2/milestone/review 落盘，按封装命令收口。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
