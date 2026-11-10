# Tasks: 物化时保留 severity 优先级
- issue_id: I-20261108T141300Z-A
- pre_tests_path: docs/B2-docs/platform/issue-parity/raw-20261108T141300Z/verification/pre-tests.md

## 任务分解

- [x] T1: 逐条复核 issue 证据（物化丢字段 / 契约已支持可选第 22 / 对账仍排除 severity / labels 可读）。
- [x] T2: 写 AT-001（2 静态 + 7 行为，含真实 `pull_raw_issue`），基线确认 RED `1 ok / 8 failed`。
- [x] T3: 新增 `severity_from_replicas`；`pull_raw_issue` 两分支写入 `fm["severity"]`。
- [x] T4: 恢复 `canonical_projection` 对 severity/* 的比较；GREEN `9 ok / 0 failed` + 6 回归全绿。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
