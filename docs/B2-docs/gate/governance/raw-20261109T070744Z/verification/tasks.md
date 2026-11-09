# Tasks: 门禁区分「修复既有损坏」与「多 issue 混入」
- issue_id: I-20261109T070744Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261109T070744Z/verification/pre-tests.md

## 任务分解

- [x] T1: 复现死锁——`raw-20261103T132517Z` 的 `pr-merge-guarded develop` 被 18+10 条错误挡住；核对 hook 执行路径（`pre-merge-commit` → `--staged`）与安装态不参与（`git rev-parse --show-toplevel`）。
- [x] T2: 写 AT-001（6 夹具 + 6 仓库/选择 + 1 反向守护），develop 基线快照确认 RED `5 ok / 8 failed`。
- [x] T3: 新增 `baseline_text()`，覆盖 `--staged`（取 `HEAD`）与 `--range`（取左端）。
- [x] T4: 新增 `legacy_frontmatter_damaged()`（纯 YAML 判定三类损坏）与 `select_repair_only_paths()`。
- [x] T5: 在 GATE 1 之前把豁免路径整体从 `issue_paths` 剔除并逐条 warning；GREEN `13 ok / 0 failed`。
- [x] T6: 真机验证——`raw-20261103T132517Z` 的 PR 在 develop 侧通过合并门禁。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6 | AT-001（Real-Environment） |
