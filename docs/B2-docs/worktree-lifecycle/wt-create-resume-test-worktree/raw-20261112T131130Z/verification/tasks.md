# Tasks — raw-20261112T131130Z

- [x] T1: `_count` 改为 `grep -c . || true` + 首行 + `^[0-9]+$` 校验 + 非数字 return 1
- [x] T2: 无 fix/feature/hotfix 匹配时回退解析唯一的 `test-pre-merge-<key>-*`
- [x] T3: 新增 AT `test-wt-close-branch-count.py`（静态 6 + 行为 5 + 基线控制 1），CORE/CI_CORE 各 +1
- [x] T4: 新增 unit `tests/unit/t-wt-close-count-01.sh`（Step 2.5）
- [x] T5: RED 5/7 → GREEN 11/0 → unit 5/0 → test-all --ci 全绿
- [x] T6: PR → review → merge → 真机回收自证残留工位 → wt-close
