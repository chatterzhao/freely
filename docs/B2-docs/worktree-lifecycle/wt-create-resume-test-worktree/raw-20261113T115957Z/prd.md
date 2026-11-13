# PRD: wt-close 收口全部 I-* children

- issue_id: I-20261113T115957Z-A
- source_raw: raw-20261113T115957Z
- workflow_kind: fix
- milestone: M-20261113T115957Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story）

## 目标

按项目已有设计补齐 `wt-close` 的 I-* 收口：遍历 `promoted_children`（1:N）、用 B2 路径定位、非终态拒绝、终态逐个关平台、失败即停。
**删除工位前先确认所有 children 已终态**，避免把未完成的 I-* 变成永久孤儿。

## 唯一改动范围

- `docs/system/workspace/scripts/worktree/wt-close`：替换原「只关 absorbed_into + 走 B1-docs 路径」的死代码块为 Phase 2.5。
- 新增 AT `test-wt-close-children.py`，`bin/test-all` 双数组各 +1。

## 不退化边界

- 不改 raw `validate()` / promote / promote-finalize / `cmd_close` / `issue-sync batch`；
- 不放宽 protected branch / reason gate / closeout gate / pretests gate；
- 不回写 I-* 文档（保持 Phase 3 的「never writes issue files」）；
- `--dry-run` 零副作用；`--skip-platform` 保留终态检查但跳过关闭；`--force` 语义不变。

## 功能需求

- FR-1：读 `promoted_children`，合并 `absorbed_into` 兜底。
- FR-2：用 `docs/B2-docs/*/*/raw-*/issues/<I-id>.md` 定位（旧的 B1-docs 路径不存在）。
- FR-3：任一 child 非 `completed|dropped` → 拒绝并列出阻塞项，平台零写入。
- FR-4：终态且 `platform_state != closed` → 逐个 `_close_platform_ids_readonly`；失败即停。
- FR-5：dry-run / skip-platform / 已关闭不重复调用。
- FR-6：基线三条红（无 Phase 2.5、B1 路径、只读 absorbed_into）。

## 验收

AT-001 RED `4 ok / 14 failed`（develop `7697cae64` 快照）→ GREEN `15 ok / 0 failed`；`bin/test-all --ci` 全绿；三门禁不变。
