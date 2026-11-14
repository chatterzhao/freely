# Tasks — raw-20261114T101138Z

- [x] T1: `platform-adapter.py` 新增 `close_dropped`（先写关闭评论再 not-planned 关单，评论失败不关任何平台）；`close_issue` 及两 handler 扩展默认参数（既有调用零改动）；CLI 新增 `close-dropped` 分派
- [x] T2: `wt-close` `--force` 分支编排 `transition("dropped")` 瞬时本地态 → 组装关闭评论（理由 + B1 研究）→ `close-dropped`，加 `--dry-run` 守卫
- [x] T3: `pull_raw_issue` 全 CLOSED 副本 fail-closed 防重新物化
- [x] T4: 新增 AT `test-wt-close-dropped-closeout.py`（10/10 OK），CORE/CI_CORE 各 +1；实现评审补测后修复 3 项实现问题
- [x] T5: promote → absorb → governance gate（已完成，raw #4653 已 absorbed/closed）
- [x] T6: RED/GREEN 证据落盘（develop 基线 RED 1/9、实现评审补测 RED 7/3、GREEN 10/0，三份日志）
- [x] T7: test-pre-merge 工位 FF 到 `764e29df1`，`test-gate run --command "bin/test-all --ci"` → 41 ok / 0 failed，`TEST_STATUS=completed`、`LAST_TESTED_COMMIT=764e29df1`；`pretests-retirement-gate` 与 `governance-merge-gate --range develop..HEAD` 均 rc=0
- [x] T8: 副本一致性门禁解除阻塞（2026-11-14T13:50Z，详见 pre-tests「副本一致性门禁」节）：`lib-state.sh` 记录 `hash` 且历史条目视为已变更、`cmd-update.sh` 去掉批量 dedup、`raw_reconciliation._COMMENT_BLOCK` 块边界修正、`issue_create_contract.platform_body` 不再重复输出本地 H1；新增 AT `test-issue-sync-update-not-noop.py`（16/0）并扩展 `test-raw-reconciliation.py`（4/0）；平台侧用 `freely feedback edit` + `issue-sync update` 归一副本
- [ ] T9: `pr-create-guarded` → `pr-review-guarded` → `pr-merge-guarded`
- [ ] T10: `issue-sync close <linked>` → `wt-close` → 更新 goal 恢复点 / memory

> 进度校正（2026-11-14T12:27Z）：T5 原先整条打勾，实际 pr-create/review/merge/wt-close 全部未执行，属提前宣告完成，已拆分为 T5–T9 并如实标注。
