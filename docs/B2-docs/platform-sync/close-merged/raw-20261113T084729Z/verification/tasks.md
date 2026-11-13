# Tasks — raw-20261113T084729Z

- [x] T1: `cmd_close` 撤销 kind 分派，对 linked 拒绝并指向 `issue-sync batch`；新增 `cmd_close_linked`
- [x] T2: batch linked 分支改用 `cmd_close_linked`
- [x] T3: `close_linked` 补 Phase 1 严格校验（phase_state / pre_tests_path / verification_artifact_dir / 平台 issue_id，零平台写入），回写 `phase_state`/`platform_state`，移除 `status: closed`
- [x] T4: 更新 AT `test-issue-sync-close-linked.py`（静态 7 + 行为 12 + 基线控制 2）与 unit `t-linked-close-01.sh`
- [x] T5: RED 8/13 → GREEN 19/0 → unit 10/0 → test-all --ci 全绿
- [x] T6: PR → review → merge → 用 batch 核对遗留 linked → wt-close
