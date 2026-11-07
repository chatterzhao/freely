# PRD: issue-sync 能找到 B2 文档，promote 不再必然失败

- issue_id: I-20261104T082556Z-A
- source_raw: raw-20261104T082556Z
- workflow_kind: fix
- milestone: M-20261104T082556Z-A
- story: gate/platform

## 目标

issue 文档的定位必须与布局无关：无论 raw 在 `docs/B1-docs/` 还是 I-* 在 `docs/B2-docs/**/issues/`，同一条命令都应该找到它，找不到要说清楚找了哪里，找到多份要拒绝而不是猜。

## 改动范围（1 个真源 + 1 个测试）

1. `bin/issue-sync`：`_issue_file_for` + `_fm_has_key`；5 个命令改用解析器；`cmd_promote` 改用解析器；`platform_state` 条件写入。
2. 新增 `docs/system/workspace/scripts/tests/test-issue-sync-promote-b2`（AT-001）。

## 不退化边界

- raw 仍优先 `docs/B1-docs/<id>/issue.md`（既有目录优先，行为等价）。
- close 的四段式顺序与 0/3/1 退出码不变。
- 不改变任何平台的创建/关闭语义，只改变「从哪里读文档」。
- 既有 `test-platform-write-channel` / `test-issue-sync-close-terminal-first` 等 7 个回归基线对比零 DIFF。

## 功能需求

- FR-1: B2 I-* 的 `cmd_create` 成功，双平台 id 回写，不注入 `platform_state`。
- FR-2: `cmd_promote` 对 B2 目标成功（children + 平台建单 + promoted_from 注释）。
- FR-3: 文档缺失 → 非零且列出检查位置。
- FR-4: 文档歧义 → 非零且列出候选。
- FR-5: 无 `file="$ISSUES_DIR/$local_id/issue.md"` 硬编码。

## 验收

AT-001 基线快照 RED `7 ok / 16 failed` → GREEN `23 ok / 0 failed`；7 个回归全 MATCH。
