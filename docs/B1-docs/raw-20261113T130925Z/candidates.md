# B1 Candidates — raw-20261113T130925Z

## C-20261113T130925Z-A：linked 平台状态投影 + 收口判据单一化

- status: promoted
- promoted_issue_id: I-20261113T130925Z-A
- promoted_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261113T130925Z/issues/I-20261113T130925Z-A.md
- milestone: M-20261113T130925Z-A
- kind: fix
- decision: linked 复用 `platform_state`；`batch` 的 close 不依赖 hash；`wt-close` 改为只读检查；三者共用同一判据。
- 范围：
  1. `bin/issue-sync.d/cmd-create.sh`：linked 也写 `platform_state: open`（去掉 `_fm_has_key` 限制），与 raw 同语义。
  2. `bin/issue-sync.d/cmd-batch.sh`：linked 分支改为「先判 `phase==completed && platform_state!=closed` → `cmd_close_linked`（不受 hash 约束）；再 `_changed_since_last_sync` → `cmd_update`」。
  3. `wt-close` Phase 2.5：去掉关闭，改为只读检查——每个 child 必须 `phase_state == completed` 且 `platform_state == closed`，否则拒绝并提示「在工位内跑 `issue-sync batch`」；删除 `_close_platform_ids_readonly` 调用与 `dropped` 误用。
  4. 更新 `test-wt-close-children.py` 为检查语义；新增 `test-issue-sync-batch-closeout.py`。
- 验收：
  - batch：首次同步（无 hash）且 completed+open → 关闭且写 `platform_state: closed`；in_dev → 不关；已 closed → 不重复；
  - wt-close：children 全部 completed+closed → 通过；任一未完成或未关 → 拒绝且工位保留、平台零写入；
  - 两条入口判据一致（同一断言矩阵）；
  - 基线（develop）同场景：batch 0 关闭、wt-close 直接删工位 → 红。
- 不退化边界：raw 契约、`cmd_close` 拒绝直连 linked、protected/reason/closeout 门禁、`issue-sync` 唯一平台写入口。
