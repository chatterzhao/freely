# Tasks: issue-sync 拆模块 + 平台投影单一契约 + bootstrap delete 收口
- issue_id: I-20261110T130144Z-A
- pre_tests_path: docs/B2-docs/platform/issue-sync-modules/raw-20261110T130144Z/verification/pre-tests.md

## 任务分解

- [x] T1: 建 feature/test 工位（基于 `d32546e19`）。普查 `_issue_body()` 的 awk 语义、`_labels()` 与 `feedback` 的标签字面量、`pull_raw_issue()` 对 frontmatter 的依赖、`bootstrap --delete`；确认 0/3/1 部分成功语义已由 R26 覆盖。
- [x] T2: 写 AT-001（24 静态 + 11 行为），develop 基线 RED `6/29`。
- [x] T3: 按行区间机械切分 `bin/issue-sync` → `bin/issue-sync.d/`（5 个 `lib-*` + 9 个 `cmd-*`），主文件只留路径解析、模块加载、分支守卫、`main()`；新增 `_issue_sync_rebind_paths()` 让 `--project` 后派生路径跟随。
- [x] T4: 新增 `sync/issue_create_contract.py`（`strip_frontmatter` / `split_workflow_kind` / `drop_comment_channel` / `platform_body` / `labels_for` + `body`/`labels` CLI）；`lib-content.sh` 的 `_issue_body`、`_labels` 改调契约；`freely feedback` 的 body 与标签改调契约。
- [x] T5: adapter 新增 `delete_issue`（GitHub）与 `issue-write-one … delete` 分派；`bin/issue-sync-bootstrap --delete` 改走 adapter。
- [x] T6: GREEN `35/0`；补 6 个夹具的 `issue-sync.d` 复制与「读完整程序」的静态断言；`test-platform-write-channel` 夹具补 adapter/契约/list stub（22/0）。`test-all --ci` 12/0，local 仅剩既有 `test-github-label-autocreate.py`。
- [x] T7: `docs/epics-map.svg` 增 `platform/issue-sync-modules` story（platform epic 重排为 6 story、高度 142，其后整体下移 26）。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001（RED fidelity） |
| T3, T4, T5 | AT-001（静态 24 + 行为 11） |
| T6 | 回归 + CI |
| T7 | epics-map 对齐门禁 |
