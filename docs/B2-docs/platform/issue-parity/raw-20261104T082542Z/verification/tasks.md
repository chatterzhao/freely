# Tasks: 物化时写入达标 H1
- issue_id: I-20261104T082542Z-A
- pre_tests_path: docs/B2-docs/platform/issue-parity/raw-20261104T082542Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `docs/system/workspace/scripts/tests/test-materialize-h1`（unit / static / backfill 三组），在未修改真源上跑确认 RED 并记录证据。
- [x] T2: 实现前评审：核查 `_local_record` 的 H1 提取与 `canonical_projection` 的前缀剥离，统计 805 份本地 raw 的 H1 覆盖率（700 缺 H1、18 多 H1）与标题来源可靠性，判定「批量回填 700 份」不纳入本 PR。
- [x] T3: `raw_title_contract.py` 新增纯函数 `local_heading_title()`，复用 `canonical_raw_title()`；按精确 key 剥前缀覆盖 4 个历史非标准 raw key；折叠空白保证单行。
- [x] T4: `platform-adapter.py::pull_raw_issue()` 落盘时写入一个 H1，body 已有 H1 时保留原样，重复 pull 幂等；Q2 三个既有函数与 created_at 兼容分支不动。
- [x] T5: 新增 `bin/raw-issue-backfill-h1`：默认 dry-run、标题只取 frontmatter 或平台副本、无来源 SKIP、已有 H1 不动、`--apply` 原子写且幂等；本 PR 不执行批量回填。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log；真实双平台副本 fingerprint parity；805 份真实 issue.md 的 Q2 契约退化审计；7 个相关回归测试。
- [x] T7: 复用既有 story `platform/issue-parity`（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、Implementation Decision Note，并现场补回本轮物化 issue.md 的一级标题。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
