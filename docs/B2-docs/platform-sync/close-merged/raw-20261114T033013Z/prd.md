# PRD: I-* 收口链路对齐设计

- issue_id: I-20261114T033013Z-A
- source_raw: raw-20261114T033013Z
- workflow_kind: fix
- milestone: M-20261114T033013Z-A
- story: platform-sync/close-merged（复用既有 story）

## 目标

让「merge 时收口 I-*」这条设计链路真正可执行：merge hook 能看到 B2 的 linked 文档、
linked 收口仍由 `issue-sync batch` 单一驱动、`platform_state` 对 linked 也由 create/close
管理、`wt-close` 预检读被裁决的工位副本。

## 唯一改动范围

- 新增 `docs/system/workspace/scripts/worktree/merge_issue_sync.py`（发现 B1+B2 / 按 raw-key 限定 / 判定 / 行替换落 phase）。
- `pr-merge-guarded::_sync_issues_changed_in_merge`：调该模块；linked 收口改由 `issue-sync batch <raw-key>`；只 `git add` 被改文件。
- `bin/issue-sync.d/cmd-create.sh`：去掉 `_fm_has_key` 守卫。
- 新增 AT `test-closeout-chain.py`，CORE/CI_CORE 各 +1（含 wt-close 读取源的设计钉子）。

## 不退化边界

- 不改 `close_linked` 的 `completed` 判据；不恢复 `issue-sync close` 直连 linked；
- 不放宽 GATE 1（scope 与 `git add` 都限定在本 lane）；
- 不处理 daemon 无范围 batch（`raw-20261114T031043Z` 单独处理）。

## 功能需求

- FR-1：发现层同时覆盖 `docs/B1-docs/*/issue.md` 与 `docs/B2-docs/**/issues/I-*.md`。
- FR-2：`--raw-key` 限定范围；其它 raw 零变更。
- FR-3：raw `proposed/"" → absorbed`、`absorbed|dropped → close`；linked `in_dev|in_b2_ibm|done_b2_ibm → in_verification`、`completed → close`。
- FR-4：phase 写入用行替换，保留其它字段顺序与取值。
- FR-5：hook 用 `issue-sync batch <raw-key>` 收口 linked；只 stage 被改文件。
- FR-6：`cmd-create` 对 linked 写 `platform_state: open`。
- FR-7：`wt-close` 的 children 预检**保持读 develop**（它在 merge 之后、在 project-root 执行；读工位副本会掩盖未合并状态）。

## 验收

AT-001 GREEN `30 ok / 0 failed`；基线（develop `f94f815ac`）`2 ok / 9 failed`；
`bin/test-all --ci` 全绿；GATE 1 语义不变。
