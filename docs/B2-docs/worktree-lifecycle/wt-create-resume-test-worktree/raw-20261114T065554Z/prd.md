# PRD: merge 后残留提交的补合并优先规范

- issue_id: I-20261114T065554Z-A
- source_raw: raw-20261114T065554Z
- workflow_kind: fix
- milestone: M-20261114T065554Z-A
- story: worktree-lifecycle/wt-create-resume-test-worktree（复用既有 story）

## 目标

让「PR 已 merge、分支上有追加提交」不再被误判为「没有 merge」，也不再被默认 `--force --discard-unmerged` 丢弃。
判定基于**可验证的 git 事实**（merge 历史 + patch-id 等价性 + 承接 raw 是否真实存在），不是自由文本理由。

## 唯一改动范围

1. 新增 `docs/system/workspace/scripts/worktree/postmerge_commit_guard.py`：`has_merge` / 逐提交 `equivalent_in_develop` / `all_equivalent` / `allow_discard`，输出 JSON，零写入。
2. `docs/system/workspace/scripts/worktree/wt-close`：
   - 新增 `--extracted-into <raw-key>`（校验 `docs/B1-docs/raw-<key>/issue.md` 真实存在）；
   - USAGE、`_require_reason` 之外的合法理由清单同步；
   - 未合并提交守卫改调判定器，按情形 A/B 分诊并打印逐提交判定；
   - Phase 6 提示按情形给出补合并路径，不再一律「分支未合并到 develop」。
3. `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md` 阶段 9 新增「merge 后残留提交」决策树（规范权威）。
4. `docs/system/workspace/commands.md` 选项表同步。
5. 新增 AT `test-postmerge-commit-guard.py`，CORE/CI_CORE 各 +1；`projection.lock` 重录。

## 不退化边界

- **不放宽** `--force` / `--discard-unmerged` 的现有拒绝判定；不动 protected 分支守卫（`test-wt-close-test-premerge-guard.py` S2 保持绿）；
- 不改 GATE 1、不改 `pr-merge-guarded`、不改 verdict 契约；
- 不自动创建 PR、不自动 merge；不把「逐提交判定」做成可补字段通过的门禁。

## 功能需求

- FR-1：区分 `never_merged` 与 `post_merge_additions`，后者不得打印「没有 merge / pr-merge-guarded 未成功」。
- FR-2：逐提交按 patch-id（`git cherry`）判定 `equivalent_in_develop`，并打印 hash + subject + 判定。
- FR-3：情形 A 保持原拒绝强度与 `--force` 策略；情形 B 仅当全部等价落盘才允许丢弃。
- FR-4：情形 B + 未落盘内容 → 拒绝丢弃，给出补合并 PR 命令与 two-dot diff 说明。
- FR-5：`--extracted-into` 指向的 raw 文档必须真实存在，否则不生效。
- FR-6：skill / commands.md / 合法理由清单三处文本与实现一致，含「先落盘、再丢弃」顺序铁律。
- FR-7：基线（develop）在 FR-1..FR-6 上必须红。

## 验收

AT-001 GREEN `25 ok / 0 failed`；基线 `2 ok / 14 failed`；`bin/test-all --ci` 全绿；既有 wt-close 测试保持绿。
