# Tasks — raw-20261112T131115Z

- [x] T1: cmd-close 按 kind 分派（linked → close-linked）
- [x] T2: raw_lifecycle_effects 新增 close_linked + CLI 分派（linked 专属校验、复用 adapter close-multi、只回写 status/updated_at）
- [x] T3: 新增 AT test-issue-sync-close-linked.py（静态 6 + 行为 9 + 双向负向控制），接入 CORE/CI_CORE
- [x] T4: 新增 tests/unit/t-linked-close-01.sh（Step 2.5）
- [x] T5: RED 7/8 → GREEN 15/0 → unit 6/0 → test-all --ci 全绿
- [x] T6: PR → review → merge → 关掉现存 linked 残留 → wt-close
