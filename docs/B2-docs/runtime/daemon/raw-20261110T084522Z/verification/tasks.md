# Tasks: 状态键白名单由自动扫描 lint 守护
- issue_id: I-20261110T084522Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T084522Z/verification/pre-tests.md

## 任务分解

- [x] T1: 严格真源普查——5 种写入形态、15 heredoc / 2 here-string / 4 printf / 3 echo / 6 --kv；实测差集 65 键（issue 报 21）。
- [x] T2: 写 AT-001（4 静态 + 7 扫描器夹具 + 5 行为），基线确认 RED `1 ok / 15 failed`；唯一 PASS 是「未知键仍拒绝」。
- [x] T3: 新增 `bin/check-state-file-keys`；修两轮扫描器自身漏判（命令替换目标 `[^"\s]*` 漏 15 键；`.*<<` 把 `<<<` 当 heredoc 误抓局部变量）。
- [x] T4: `ALLOWED_KEYS` 77 → 142、注释改为 lint 校验；lint missing=0 且 stale=0。
- [x] T5: GREEN `16 ok / 0 failed`；16 项回归 + 两个 lint 全绿；未改 `read_state` 拒绝语义与任何调用点。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
