# Tasks: raw 身份不漂移与平台标题达标
- issue_id: I-20261105T051136Z-A
- pre_tests_path: docs/B2-docs/platform/issue-parity/raw-20261105T051136Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `docs/system/workspace/scripts/tests/test-raw-key-drift`（unit + static + wtcreate 三组），在未修改真源上跑确认 RED 并记录证据。
- [x] T2: 新增纯模块 `docs/system/workspace/scripts/sync/raw_title_contract.py`，定义 `canonical_raw_title()` / `is_canonical_raw_title()` / `platform_title()` 三个契约。
- [x] T3: 改造 `platform-adapter.py.pull_raw_issue()`：保留 created_at 兼容分支只做诊断，删除身份与落盘路径改写，遍历所有 replica 同步达标标题。
- [x] T4: 收敛三处调用方：`bin/issue-sync._platform_title()` 复用 `platform_title()`；`runtime/freely.cmd_feedback` edit 对 raw 标题复用 `canonical_raw_title()`；`bin/raw-issue-pull` 去掉静默吞错并输出可诊断告警。
- [x] T5: 强化 `wt-create._pull_raw_issue()`：严格比对 expected_local_id 并校验 expected_issue_file 存在，复用既有失败清理分支。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log，更新 pre-tests.md 的 red-green-status 与 status 字段。
- [x] T7: 退化审计：803 份真实 B1 issue.md 的新旧达标契约对比；14 个相关回归测试 + 2 个失败项的未修改 develop HEAD 基线对比；确认四处兼容能力未删、零新增失败。
- [x] T8: 复用既有 story `platform/issue-parity`（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、Implementation Decision Note，并现场补回物化 issue.md 的一级标题（Q3 现场规避）。
- [x] T9: PR review 阶段实测发现「去掉静默吞错后 issue-sync 多行 stdout 污染 raw-issue-pull 的 JSON 输出，导致 wt-create 严格身份校验必然失败」。补 AT-002 隔离仓库测试先跑 RED，再把所有诊断导向 stderr、让 wt-create 转发 stderr，跑 GREEN 并记录证据。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T3 | AT-001 |
| T4, T5 | AT-001 |
| T6, T7 | AT-001 |
| T8 | 门禁治理链 |
| T9 | AT-002 |
