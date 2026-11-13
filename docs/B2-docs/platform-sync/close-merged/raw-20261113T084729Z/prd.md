# PRD: linked 收口回归 batch 单一路径与等价门禁

- issue_id: I-20261113T084729Z-A
- source_raw: raw-20261113T084729Z
- workflow_kind: fix
- milestone: M-20261113T084729Z-A
- story: platform-sync/close-merged（复用既有 story）

## 目标

恢复 R33.8 降级的 linked 收口门禁，使其符合 `bin/issue-sync` 头注释与 `cmd-batch.sh` 所定义的设计意图：
**状态驱动、batch 单一路径、关闭前等价于 raw 的本地严格校验**。

## 唯一改动范围

- `bin/issue-sync.d/cmd-close.sh`、`bin/issue-sync.d/cmd-batch.sh`、`docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py::close_linked`。
- 更新既有 AT `test-issue-sync-close-linked.py` 与 unit `t-linked-close-01.sh`（它们是 R33.8 的产物，随实现同步修正，不算夹带）。

## 不退化边界

- `raw_metadata_contract.validate`、`close_platforms`、`promote-finalize`、`platform-adapter` 一行不改；
- batch 的 `_changed_since_last_sync` 与 `platform_state` 跳过判据不改；
- 不新增 CLI 子命令 / phase 枚举；不放宽任何门禁；linked 仍可被收口（由 batch 驱动）。

## 功能需求

- FR-1：直连 `cmd_close` 对 linked 拒绝并指向 batch。
- FR-2：batch linked 分支调用 `cmd_close_linked`；该函数校验 `schema_version=1` 与 `phase_state=completed`。
- FR-3：`close_linked` Phase 1 校验 `phase_state`、`pre_tests_path`、`verification_artifact_dir`、每平台 `issue_id`；失败零平台写入。
- FR-4：成功后回写 `phase_state: completed` / `platform_state: closed` / `updated_at`，不写 `status: closed`。
- FR-5：部分关单不改本地状态；raw 的严格契约未被放宽。
- FR-6：develop 基线必须复现宽松行为（负向控制）。

## 验收

AT-001 RED `8 ok / 13 failed`（develop `7715ef030` 快照 + 基线控制 R1/R2）→ GREEN `19 ok / 0 failed`；
unit `10 ok / 0 failed`；`bin/test-all --ci` 全绿；三门禁不变。
