# Tasks — raw-20261113T084851Z

- [x] T1: `pull_raw_issue` 镜像 `details["comments"]` 为本地 `### comment-platform-<n>` 块（meta 行可被 `_strip_meta` 剥除）
- [x] T2: 物化前识别本地终态 raw，保留 `phase_state / platform_state / absorbed_into / canonical_issue_path / completed_at / promoted_children / closeout_note / source_candidate`
- [x] T3: 新增 AT `test-raw-issue-pull-parity.py`（静态 5 + 行为 8 + 基线控制 3），CORE/CI_CORE 各 +1
- [x] T4: 新增 unit `tests/unit/t-raw-issue-pull-parity-01.sh`（Step 2.5）
- [x] T5: RED 6/10 → GREEN 13/0 → unit 4/0 → test-all --ci 全绿
- [x] T6: PR → review → merge → 关 linked → wt-close
