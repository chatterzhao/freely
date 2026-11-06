# Tasks: 批量化治理门禁读取
- issue_id: I-20261106T065711Z-A
- pre_tests_path: docs/B2-docs/gate/governance/raw-20261106T065711Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写 `docs/system/workspace/scripts/tests/test-governance-gate-batch-read`（static / unit / equivalence / perf 四组），在未修改真源上跑确认 RED 并记录证据。
- [x] T2: 实现前评审：证伪「改用 title 精确搜索」等方向，实测 `git cat-file --batch` 对 `:path` 与 `REF:path` 均与 `git show` 字节级一致，Step 2e 计数在 804 份真实文件上等价。
- [x] T3: 新增 `docs/system/workspace/scripts/quality/governance_repo_view.py`：长驻 `git cat-file --batch` + 按 spec 缓存 + 非 blob/异常回退 + universal newline 与严格 UTF-8 对齐 `text=True`。
- [x] T4: 改造 `governance-merge-gate` 四个函数委托 `RepoView`；分支优先级、`FileNotFoundError` 文案、`path_exists` 布尔语义逐行保留；`atexit` 关闭批量进程。
- [x] T5: 新增 `docs/system/workspace/scripts/quality/comment-resolution-scan.py`；`pr-create-guarded` Step 2e 改为单进程调用，缺扫描器时 fail-closed，失败块文案完整保留。
- [x] T6: 跑 GREEN，写 AT-001-GREEN.log，更新 pre-tests.md 的 red-green-status 与 status。
- [x] T7: 退化审计：6 种 gate 调用模式 verdict parity（47.436s → 0.879s）；4,363 份真实治理文档 × 2 函数 × 双视图 0 差异；7 个相关回归测试以未修改 develop HEAD 做基线对比，0 新增失败；子进程 3423 → 8。
- [x] T8: 复用既有 story `gate/governance`（无需改 epics-map.svg），`bin/check-epics-map` 校验对齐；补齐 B1/B2 治理文档、milestone、Implementation Decision Note，并现场补回物化 issue.md 的一级标题（R2 现场规避）。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4, T5 | AT-001 |
| T6, T7 | AT-001 |
| T8 | 门禁治理链 |
