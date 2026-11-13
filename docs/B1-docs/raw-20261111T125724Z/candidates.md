# B1 Candidates — raw-20261111T125724Z

## C-20261111T125724Z-A：注册表分类落地（本轮唯一 candidate）

- status: promoted
- promoted_issue_id: I-20261111T125724Z-A
- promoted_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261111T125724Z/issues/I-20261111T125724Z-A.md
- milestone: M-20261111T125724Z-A
- kind: feature
- decision: 按项目设计意图逐条判定 35 条 `implementation-in-bin`，分类落地；13 条真实迁移另立新 raw 承接（见 brainstorms §3 的流程约束）。
- 依据：brainstorms §1 / §2 / §3。
- 范围：
  1. `docs/system/workspace/scripts/bin-projections.yaml`：`classes` 增加 `standalone-tool`；35 条 `implementation-in-bin` 按 §2 逐条改成 `standalone-tool`（22）或保留 `implementation-in-bin`（13），每条 `reason` 写成**具体判定依据**，删除统一占位文案。
  2. `bin/check-bin-projection`：新增 class 白名单校验（只接受 `classes` 中声明的值）、拒绝占位/空 reason；**保留** coverage / staleness / shrink 三条既有规则且对所有 class 一视同仁（不新增豁免）。
  3. `docs/system/workspace/scripts/bin-inventory.md`：总览与 35 条表格按新分类同步。
  4. 新增 AT `test-bin-projection-classification.py` 与 unit `t-bin-projection-01.sh`，接入 CORE/CI_CORE。
- 验收：
  - 35 条全部有明确 class 与非占位 reason；22 条 standalone、13 条待迁移；
  - lint 三条规则逐条负向验证（未登记 >40 行判红、stale 条目判红、已变投影的条目判红、非法 class 判红、占位 reason 判红）；
  - `bin/check-bin-projection` / `bin/test-all --ci` / 三门禁全绿；
  - **不迁移任何实现**，行为零变化。
- 不退化边界：
  - `threshold_lines` 不变，三条规则不变，不新增任何豁免；
  - 不改 `bin/` 下任何业务脚本内容；不改 `projection.lock`；
  - 不夹带后续迁移。

## 后续规划（不属于本 raw 的 candidate）

`pr-create-guarded` Step 0b 要求 raw `phase_state: absorbed`（必须先 `promote-finalize`），因此同一个 raw **不可能跨多个 PR 保持 open**。按项目既有惯例「部分完成 → 另立新 raw」（R25、R28.5 等），C-A 合并后用 `./bin/freely feedback` 登记**一条新 raw** 承接下面 13 条迁移，再由它的 B1 按域拆 candidate/批次，每批独立 PR、独立 RED→GREEN、独立 wt-close：

- `sync/` 与 `skills/` 域：`bin/raw-issue-pull`、`bin/issue-sync-bootstrap`、`bin/deploy-skills`
  （`raw-issue-pull` 在 R33.11 刚修过 comments 镜像与终态保护，迁移必须逐字保留行为并用 `test-raw-issue-pull-parity.py` 回归）。
- `runtime/` 与 `agents/` 域：`bin/agent-table-query`、`bin/freely-package`、`bin/freely-cycle`、`bin/cache-baseline`、`bin/freely-watchdog`、`bin/pre-init-runtime`（改到 `scripts/runtime/` 的批次同轮补 `tests/unit/t-*.sh`，R27 契约）。
- `worktree/` / `tests/` / `lifecycle/` 域：`bin/freely-review`、`bin/git-worktree-guard`、`bin/test-pre-merge-selfhost`、`bin/issue-index`。

本 raw 的完成范围如实标注为「**分类落地**；13 条实现迁移另立 raw」，不谎称全部完成。
