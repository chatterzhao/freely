# Tasks — raw-20261113T074432Z

- [x] T1: `wt-close` 保护分支守卫增加窄例外（test-pre-merge-* + FORCE + DISCARD_UNMERGED），main/develop 仍拒绝
- [x] T2: 新增 AT `test-wt-close-test-premerge-guard.py`（静态 5 + 行为 7 + 基线控制 1），CORE/CI_CORE 各 +1
- [x] T3: 新增 unit `tests/unit/t-wt-close-premerge-guard-01.sh`（Step 2.5）
- [x] T4: RED 8/5 → GREEN 12/0 → unit 5/0 → test-all --ci 全绿
- [x] T5: PR → review → merge → 真机回收自证残留工位 → wt-close
