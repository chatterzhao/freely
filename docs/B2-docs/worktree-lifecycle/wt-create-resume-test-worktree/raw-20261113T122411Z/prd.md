# PRD: children 报告的空字段不再折叠 TSV 列

- issue_id: I-20261113T122411Z-A
- source_raw: raw-20261113T122411Z
- workflow_kind: fix
- milestone: M-20261113T122411Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story）

## 目标

修复 R33.15 引入的序列化缺陷：`platform_state` 缺失时 TSV 空列被 bash IFS 折叠，导致路径错位、`wt-close` 无法关闭 children。

## 唯一改动范围

- `wt-close` Phase 2.5 的 python 输出两处加 `or "-"`（空字段占位）。
- AT `test-wt-close-children.py`：fixture 支持「字段缺失」（不只是空值），新增 B8；基线断言改为对已含 R33.15 的现状。

## 不退化边界

- 不改 Phase 2.5 的遍历 / 终态门禁 / 关闭顺序；
- 不改 `_close_platform_ids_readonly` / `_fm_get`；
- 不放宽任何门禁。

## 功能需求

- FR-1：缺失 `platform_state` 时输出 `-`，bash 侧不折叠列。
- FR-2：B8 用例：两个 child 都缺 `platform_state` → 关闭 2 次。
- FR-3：基线在该用例上必须失败（R3 + B8 红）。

## 验收

AT RED `18 ok / 1 failed`（develop `651214f27`）→ GREEN `16 ok / 0 failed`；`bin/test-all --ci` 全绿。
