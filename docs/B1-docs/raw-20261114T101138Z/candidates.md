# B1 Candidates — raw-20261114T101138Z

## C-20261114T101138Z-A：dropped 收口自动写关闭理由并防重新物化

- status: promoted
- promoted_issue_id: I-20261114T101138Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261114T101138Z/issues/I-20261114T101138Z-A.md
- milestone: M-20261114T101138Z-A
- kind: fix
- decision: 方案 A——复用 `wt-close --force --discard-unmerged` 骨架（不新造 flag、不走正常 close 分支），在 `--force` 分支内部编排 `transition("dropped")` + 平台 `close-dropped`；adapter 新增 `close_dropped`（先写关闭评论再 `not planned` 关单），并给 `pull_raw_issue` 加全 CLOSED 副本 fail-closed。**不改 `runtime/freely`**（27158 行预算）。
- design_verdict: 实现未完成 + 实现偏差
- anchor_refs: `wt-close:1279/569/986/1008/1338`（FORCE 已满足的骨架）；`raw_metadata_contract.py:258-266`（transition dropped 写 phase_state+completed_at+closeout_note）；`raw_metadata_contract.py:194-196`（dropped 必填 completed_at/closeout_note）；`platform-adapter.py:329`（GitHub close_issue 无 --reason）、`:671`（Gitee close_issue 无 --comment）；`platform-adapter.py:1491`（平台 phase/* 标签是创建时快照，非第二真相源）
- 范围:
  1. `platform-adapter.py`：`close_issue` / 两个 handler 的 `close_issue` 扩展默认参数 `close_reason=""` / `comment_body=""`（既有调用零改动）；新增 `close_dropped(raw_key, platform_ids, comment_body)`——逐平台先 `add_comment`（issue 仍 OPEN 方可写），任一评论失败则整体失败、不关任何平台；全部成功后逐平台 `close_issue(close_reason="not planned")`；GitHub `--reason not planned`、Gitee `--comment`。
  2. `platform-adapter.py` CLI 新增 `close-dropped` 分派（评论失败返回 `_dropped` 标记 → 退出码 1）。
  3. `wt-close` `--force` 分支编排：关平台前 `transition("dropped", reason=FORCE_REASON)` 写瞬时本地态（不 commit）→ 组装关闭评论 = `FORCE_REASON` + 工位内 B1 研究（`brainstorms.md`/`candidates.md`，未提交也读得到）→ 调 `close-dropped`；失败原子（评论/关单失败不删工位）；加 `--dry-run` 守卫。
  4. `platform-adapter.py` `pull_raw_issue`：所有可读副本 `state` 均为 `CLOSED` → fail-closed 返回 None，杜绝本地文档抹除后被重新物化。
  5. 新增 AT `test-wt-close-dropped-closeout.py`，CORE/CI_CORE 各 +1。
- 验收:
  - `close_dropped` 评论先于关闭；GitHub 以 `not planned` 关闭；Gitee 关闭带 `--comment`；评论失败不关任何平台；
  - `close_issue` 扩展默认参数后既有 `close-raw`/`close-multi`/CLI `close` 行为不变；
  - `wt-close --force --reason` 关单前本地瞬时 `phase_state=dropped` 且 `completed_at`/`closeout_note` 齐全、`validate()` 通过；
  - `pull_raw_issue` 全 CLOSED 副本返回 None；
  - 回归既有 adapter / wt-close 测试全绿；基线（develop）各条红。
- 不退化边界:
  - 不新造 `--drop` flag、不走正常 close 分支、不要求先手动 `issue-sync drop`；
  - 不给平台写 `phase/dropped` 标签（避免第二真相源）；
  - 不把 B1 研究合进 develop、不追溯重开历史 issue；
  - 不走 `freely comment`（#4654 独立）、不改 `runtime/freely` 行数预算、不改 `validate()`/GATE 1。
