# B1 Brainstorm — raw-20261113T115957Z

## 1. 问题

一个 raw issue 可以 promote 出多个 I-*（`promoted_children` 列表），但**一个 raw 只有一个 worktree**。`wt-close` 删除 worktree 后，未完成的 I-* 再也没有工位可以实现；已完成的 I-* 若未关平台，会永久 OPEN。

## 2. 设计意图（已核实，设计是完整的）

1. `bin/issue-sync` 头注释：`B1 promotion_started (1:N children) → promotion_finalized (absorbed/open) → configured-platform close`。
2. `cmd-promote-finalize.sh`：关闭 raw 前把 `promoted_children` 列成 comment——children 是**集合**。
3. `wt-close` 自身注释：「Also close the absorbed I-* issue…otherwise completed I-* issues accumulate as open on GitHub」；Phase 3「Raw and linked issue metadata **must already be terminal** before cleanup starts」；已有 helper `_close_platform_ids_readonly`（读 `platform_ids` → adapter `close-multi`）。

结论：作者已经设计了「wt-close 检查并关闭 I-*」，只是实现没接对。

## 3. 三处实现缺陷（已定位到行）

1. **路径错**：`_wt_i_file="$wt_path/docs/B1-docs/$_wt_i_absorbed_i/issue.md"`——I-* 实际在 `docs/B2-docs/{epic}/{story}/raw-{key}/issues/<I-id>.md`。实测 B1 路径不存在 → 整段逻辑被跳过。
2. **只关一个**：只取 `absorbed_into`（单个），而 `promoted_children` 是列表。实测 R33.6：`absorbed_into=A`、`promoted_children=[A,B]` → B 永不关闭。**这是历史所有 linked 残留的根因。**
3. **无前置检查**：「must already be terminal」只是注释；Phase 1 只检查 raw 的 `phase_state`。若某 child 仍 `in_dev`，工位会被删，该 child 永远无法实现且无告警。

## 4. 方案

| 方案 | 做法 | 评价 |
|---|---|---|
| A | Phase 2 里用一段 python 一次解析 `promoted_children`（合并 `absorbed_into` 兜底）+ B2 glob 定位 → 输出 `child/phase/platform_state/path`；bash 先做终态前置检查（非终态拒绝），再逐个 `_close_platform_ids_readonly` 关闭，失败即停 | 复用现有单点、fail-closed、一次遍历 ✅ |
| B | 让 `issue-sync batch` 负责，wt-close 不管 | batch 需工位外运行，工位删了就无法收口；用户明确要求 wt-close 封装 |
| C | 只修路径，仍只关一个 | 不解决 1:N |
| D | 非终态时用 `--force` 允许删工位 | 会丢失未完成工作，属能力降级 |

## 5. 证伪

- 「children 是单个」→ 否：`promoted_children` 是列表，`cmd-promote.sh` 逐条 append。
- 「wt-close 不该管平台」→ 否：它已经在关 raw 平台 issue，且 Phase 3 注释明确要求 linked 终态。
- 「batch 会兜底」→ 否：batch 必须在工位内跑（`--project` 受 protected branch guard 约束），工位删掉就无法收口；这正是当前残留的来源。
