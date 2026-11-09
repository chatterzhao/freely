# Tasks: 外部输入不进代码体 + sed 跨平台
- issue_id: I-20261103T132636Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261103T132636Z/verification/pre-tests.md

## 任务分解

- [x] T1: 重新定位注入点（issue 行号已漂移）——`pr-review-guarded` 2 处；扫出 6 处 BSD sed + 1 处 `.bak` 残留。
- [x] T2: 写 AT-001（3 静态 + 4 行为，含可执行 PoC），基线确认 RED `4 ok / 3 failed`。
- [x] T3: 两处插值改 heredoc + `sys.argv`。
- [x] T4: 6 处 `sed -i ''` 改 `sed -i.bak` + 同命令清理；补 `wt-close` 的 `.bak` 清理。
- [x] T5: GREEN `7 ok / 0 failed`；拆 #4247（状态文件/TSV/剩余 `python3 -c`）并排进 goal。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
