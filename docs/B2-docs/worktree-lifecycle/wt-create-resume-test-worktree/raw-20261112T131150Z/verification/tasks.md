# Tasks — raw-20261112T131150Z

- [x] T1: wt-close Phase 6b（companion test-pre-merge 清理 + agent 释放）纳入 DRY_RUN 分支
- [x] T2: wt-create 新增 --reopen（usage + 解析 + 显式拒绝文案）
- [x] T3: wt-create 恢复模式不改写 phase；reopen 写入 dev 工位内文档（_reopen_file）
- [x] T4: 新增 AT test-wt-close-dryrun-safety.py（静态 8 + 行为 3 + 负向控制），接入 CORE/CI_CORE 各 +1
- [x] T5: 新增 tests/unit/t-worktree-preview-01.sh（Step 2.5 函数级证据）
- [x] T6: RED（develop 快照 3 ok / 9 failed）→ GREEN（12 ok / 0 failed）→ unit 5/0 → test-all --ci 全绿
- [x] T7: projection.lock 重录（wt-close / wt-create 是 delegate 投影）
- [x] T8: PR → review → merge → 合并后真实 wt-close --dry-run 自证 → wt-close
