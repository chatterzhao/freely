# Tasks: pretests-gate 字段值解析统一化
- issue_id: I-20261104T082740Z-A
- pre_tests_path: docs/B2-docs/gate/pretests-gate-field-parsing-compat/raw-20261104T082740Z/verification/pre-tests.md

## 任务分解

- [x] T1: 编写脚本级回归测试 `docs/system/workspace/scripts/tests/test-pretests-gate-inline-code-fields`（unit 断言组 + e2e 隔离真实 git 仓库组），先在未修改的 gate 上跑确认 RED 并记录证据。
- [x] T2: 新增 `_field_line_value(text, key)` 唯一真源，用单行 `[ \t]*(.*)` 取剩余全部内容，仅剥离首尾成对的同型引号，保留 #3957 四格式兼容。
- [x] T3: 把 `phase_state()`、`parse_issue_binding()`、`derive_tasks_path()`、`parse_fields()`、`parse_scalar()`、`has_blocker_taxonomy()`、`issue_is_follow_on()` 全部改为复用真源，逐条保留空值语义。
- [x] T4: 跑 GREEN，写 `AT-001-GREEN.log`，更新 pre-tests.md 的 red-green-status 与 status 字段。
- [x] T5: 以 develop HEAD 的未修改 gate 与工作树修复版分别运行 10 个门禁相关测试，逐项比对退出码，确认零回归；确认 9 个预存失败已被 #4151 覆盖，不重复创建 raw issue。
- [x] T6: 复核 `docs/epics-map.svg` 对齐（复用既有 story `pretests-gate-field-parsing-compat`，无需改 SVG）；`bin/check-epics-map` 通过 16 epics / 205 stories aligned。
- [x] T7: 补齐 B1/B2 治理文档、milestone 与 Implementation Decision Note；物化的 raw issue 补回一级标题以对齐平台 title（#4181 已知缺陷的现场规避）。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2, T3 | AT-001 |
| T4, T5 | AT-001 |
| T6, T7 | 门禁治理链 |
