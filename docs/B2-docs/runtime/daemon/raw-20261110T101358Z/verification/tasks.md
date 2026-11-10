# Tasks: 恢复 a2a_task.py CLI 可加载性
- issue_id: I-20261110T101358Z-A
- pre_tests_path: docs/B2-docs/runtime/daemon/raw-20261110T101358Z/verification/pre-tests.md

## 任务分解

- [x] T1: R23.10 真源普查时实测 develop 与安装态均 `NameError: name 'SSEPool' is not defined`；`git diff` 确认为现状、`git log -S` 定位引入提交 `eb03edc74`；证伪现有 open issue 未覆盖，用 `feedback` 立 P0 #4272。
- [x] T2: 在文件副本上预演 `from __future__ import annotations`，确认 CLI 返回明确业务错误；写 AT-001（3 静态 + 5 行为），基线确认 RED `2 ok / 6 failed`。
- [x] T3: 加 future import；新增冒烟 AT 并同时接入 `bin/test-all` 的 `CORE` / `CI_CORE`（用 `replace_all` 一次命中两个列表）。
- [x] T4: GREEN `8 ok / 0 failed`；`bin/test-all --ci` 实际执行新冒烟且全绿；6 个相关测试 + `test-materialize-h1` 全绿；对比基线确认 `test-github-label-autocreate.py` 是既有失败。

## 验收关联

| 任务 | acceptance item |
|---|---|
| T1, T2 | AT-001 |
| T3, T4 | AT-001 |
