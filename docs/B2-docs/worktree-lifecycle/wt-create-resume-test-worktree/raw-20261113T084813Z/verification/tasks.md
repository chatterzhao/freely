# Tasks — raw-20261113T084813Z

- [x] T1: 恢复 `_is_protected_branch` 守卫对 test-pre-merge-* 的一律拒绝，删除 R33.10 例外
- [x] T2: 撤销 resolver 的 test-pre-merge 回退（保留 R33.9 `_count` 数值守卫）
- [x] T3: 新增 `_wt_retire_orphan_test_sandbox` + `ORPHAN_SANDBOX_KEY` 解析标记（reason gate 之后执行，零平台/Phase 7 副作用，支持 dry-run）
- [x] T4: 更新 guard AT / count AT 与两个 unit（含修正「临时目录已清理导致假绿」的夹具缺陷）
- [x] T5: 双 AT RED→GREEN、双 unit 全绿、test-all --ci 全绿、projection.lock 重录
- [x] T6: PR → review → merge → 关 linked → wt-close
