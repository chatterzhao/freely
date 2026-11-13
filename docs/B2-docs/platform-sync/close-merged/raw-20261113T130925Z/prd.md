# PRD: linked 平台状态投影与收口判据单一化

- issue_id: I-20261113T130925Z-A
- source_raw: raw-20261113T130925Z
- workflow_kind: fix
- milestone: M-20261113T130925Z-A
- story: platform-sync/close-merged（复用既有 story）

## 目标

让「本地 completed ↔ 平台 closed」可以被**幂等**判定与执行，且只有一条收口判据：
linked `phase_state == completed && platform_state != closed`。

## 唯一改动范围

- `bin/issue-sync.d/cmd-create.sh`：linked 也写 `platform_state: open`（去掉 `_fm_has_key` 限制）。
- `bin/issue-sync.d/cmd-batch.sh`：
  - 修正两处 `local_id` 推导（B2 文档是 `*/issues/I-*.md`，取文件名；旧实现取 `issues` 导致 linked **全部被过滤**）；
  - linked 的 close 提前到 hash 判定之外（状态判据 vs 变更判据解耦）。
- `docs/system/workspace/scripts/worktree/wt-close`：Phase 2.5 改为**只读检查**（children 必须 completed + platform_state closed；不再调 adapter、不再写文档）。
- 更新 `test-wt-close-children.py`；新增 `test-issue-sync-batch-closeout.py`，CORE/CI_CORE 各 +1。

## 不退化边界

- raw 契约、`cmd_close` 拒绝直连 linked、`cmd_close_linked` 的 Phase 1 校验不变；
- `issue-sync` 仍是唯一平台写入口（wt-close 不再直调 adapter）；
- 不放宽 protected / reason / closeout / pretests 门禁。

## 功能需求

- FR-1：linked 有 `platform_state`（open/closed），与 raw 同语义。
- FR-2：batch 能识别并处理 B2 linked 文档（id 取自文件名）。
- FR-3：batch 对 completed+未关闭的 linked 关闭，**不受** `_changed_since_last_sync` 约束。
- FR-4：wt-close 只检查，不写平台/文档；未就绪则拒绝并提示 batch。
- FR-5：基线必须红（batch 0 关闭；wt-close 直接写平台）。

## 验收

双 AT GREEN；基线红；`bin/test-all --ci` 全绿；合并后用 batch 完成一次真实对齐。
