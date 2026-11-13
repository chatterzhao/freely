# B1 Candidates — raw-20261113T084729Z

## C-20261113T084729Z-A：linked 收口回归 batch 单一路径与等价门禁

- kind: fix
- 范围：
  1. `bin/issue-sync.d/cmd-close.sh`：`cmd_close` 撤销 kind 分派，遇 linked 明确拒绝并提示 `issue-sync batch`；新增仅供 batch 调用的 `cmd_close_linked`（校验 schema_version / phase_state 后调 effect，处理 0/3/1）。
  2. `bin/issue-sync.d/cmd-batch.sh`：linked 分支的 `cmd_close` 改为 `cmd_close_linked`。
  3. `raw_lifecycle_effects.py::close_linked` 补 **Phase 1 本地严格校验**（零平台写入）：`phase_state == completed`、`pre_tests_path` 指向文件存在、`verification_artifact_dir` 指向目录存在、每个平台 `issue_id` 齐全；成功后回写 `phase_state: completed` + `platform_state: closed` + `updated_at`，移除 `status: closed`。
  4. 更新 AT `test-issue-sync-close-linked.py`（静态 7 + 行为 12 + 基线控制 2）与 unit `t-linked-close-01.sh`，两者已在 CORE/CI_CORE 中。
- 验收：
  - 直连 `issue-sync close <I-id>` 被拒；batch 的 linked 分支调用专用动作；
  - `in_dev` linked 被 effect 拒绝且**平台零写入**（stub adapter 记录调用）；缺 B2 证据路径同样拒绝且零写入；
  - `completed` linked 收口成功，文档写 `platform_state: closed`、不出现 `status: closed`；
  - 部分关单不改本地状态；`kind: raw` 被 `close-linked` 拒绝；`close-platforms` 对 linked 仍报 raw 契约错误（严格性未放宽）；
  - develop 基线必须复现「`in_dev` 被关」与「写 `status: closed`」两项红。
- 不退化边界：
  - raw 的 `validate()` / `close_platforms` / `promote-finalize` / `fetch_issue` / 平台 adapter 不改；
  - `issue-sync batch` 的 `_changed_since_last_sync`、`platform_state` 跳过判据不改；
  - 不新增 CLI 子命令、不新增 phase 枚举、不放宽任何门禁。
- 合并后动作：用 `./bin/freely issue-sync batch --project <工位>` 按设计路径核对遗留 linked（R33.8 已关的 8 条 + #4330 等），不再逐条 `close`。
