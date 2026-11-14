# B1 Candidates — raw-20261114T065554Z

## C-20261114T065554Z-A：merge 后残留提交的补合并优先规范

- status: promoted
- promoted_issue_id: I-20261114T065554Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261114T065554Z/issues/I-20261114T065554Z-A.md
- milestone: M-20261114T065554Z-A
- kind: fix
- decision: 方案 C——新增独立判定器 `postmerge_commit_guard.py`（git 事实：merge 历史 + patch-id 等价性）；`wt-close` 守卫分情形放行；skill 阶段 9 定义规范权威；两处提示语逐提交追问；`commands.md` 与合法理由清单同步。
- design_verdict: 实现偏差 + 实现未完成（设计本身正确）
- anchor_refs: wt-close:795/797-800 提示语；wt-close:198-201 `_has_merge`；commands.md 收口定义；workflow-skill 阶段 9
- 范围:
  1. 新增 `docs/system/workspace/scripts/worktree/postmerge_commit_guard.py`：`has_merge` / 逐提交 `equivalent_in_develop` / `allow_discard`，输出 JSON。
  2. `docs/system/workspace/scripts/worktree/wt-close`：
     - 新增 `--extracted-into <raw-key>` 参数（校验承接 raw 文档存在）；
     - USAGE、`_require_reason`、合法理由清单同步；
     - 未合并提交守卫（782-813）改调判定器、按情形 A/B 分诊、打印逐提交判定；
     - Phase 6 提示（1290-1306）纠正「没 merge」误判，指向补合并路径。
  3. `docs/system/workspace/skills/freely-workflow-guarded-execution/SKILL.md` 阶段 9 新增「merge 后残留提交」决策树（分情形 / 逐提交判定 / 先落盘再丢弃 / two-dot diff 坑）。
  4. `docs/system/workspace/commands.md` 选项表同步。
  5. 新增 AT `test-postmerge-commit-guard.py`，CORE/CI_CORE 各 +1。
- 验收:
  - 情形 A（从未 merge）：`allow_discard=true`，原提示强度不变；
  - 情形 B（已 merge + 追加提交未落盘）：`allow_discard=false`，守卫不得打印「没有 merge」，必须给出补合并 PR 命令；
  - 情形 B + 内容已等价落盘：`allow_discard=true` 且列出比对证据；
  - 情形 B + `--extracted-into` 指向不存在的 raw：拒绝；
  - 两处提示语含逐提交 hash、补合并命令、two-dot diff 说明；
  - skill / commands.md / 合法理由清单三处文本与实现一致；
  - `test-wt-close-test-premerge-guard.py` S2（protected 守卫无 --force 例外）保持绿；
  - 基线（develop）各条红。
- 不退化边界:
  - 不放宽 `--force` / `--discard-unmerged` 现有拒绝判定；不动 protected 分支守卫；
  - 不改 GATE 1 / `pr-merge-guarded` / verdict 契约；
  - 不自动建 PR、不自动 merge；不把判定做成补字段式门禁。
