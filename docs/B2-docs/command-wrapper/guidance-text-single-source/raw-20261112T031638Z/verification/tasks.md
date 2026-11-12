# Tasks — raw-20261112T031638Z

- [x] T1: 修 `bin/issue-sync:126,127,131` protected guard 文案（真实 skill + `--kind`）
- [x] T2: 修 `pretests-gate:570`、`wt-close:1155/1159/1163` 文案
- [x] T3: 修 `runtime/freely:1110/10771/11361/11407/13430` 五处指引（补 `--kind`）
- [x] T4: 修 `hooks/reference-transaction.sh:118`（去重复选项 + `--kind`）、`AGENTS.md.example:146`、`three-loop-capability-lifecycle.md:206/359`、`pr-create-guarded:158` 注释
- [x] T5: 改 `test-wt-close-protected-branch-guard` Test5/Test6（反向断言 + `grep -E`），并加入 `bin/test-all`
- [x] T6: 新增 AT `test-guidance-text-single-source.py`（全域扫描 + 白名单 + `--kind` + 负向控制 + AT-002 各项）
- [x] T7: `bin/test-all` 的 `CORE`/`CI_CORE` 各 +1；epics 注册 story + `epics-map.svg`
- [x] T8: 修 `bin/raw-issue-pull:133` 显式传 `--project <工位根>`
- [x] T9: 新增 `tests/unit/t-guidance-01.sh`（Step 2.5 要求）
- [x] T10: RED（develop 基线快照）→ GREEN → 三门禁 → test-gate → PR → review → merge → wt-close