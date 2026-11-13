# B1 Candidates — raw-20261113T084851Z

## C-20261113T084851Z-A：pull 与平台副本保持天然一致

- kind: fix
- 范围（`platform-adapter.py::pull_raw_issue`）：
  1. 从 `details["comments"]` 生成 `### comment-platform-<n>` 块追加到 `rendered_body`；meta 行交给 `_strip_meta()` 剥除，正文与平台 comment 逐字一致；已存在于 body 的相同文本跳过，保证重复 pull 不累积。
  2. 物化前读取本地已有 `issue.md`：若 `phase_state ∈ {absorbed, closed, dropped}`，保留该终态及 `platform_state / absorbed_into / canonical_issue_path / completed_at / promoted_children / closeout_note / source_candidate`，只让平台真源字段（`platform_ids / primary_platform / updated_at / severity`）覆盖；`phase` 不再被创建时快照标签回退。
  3. 新增 AT `test-raw-issue-pull-parity.py`（静态 5 + 行为 8 + 基线控制 3）与 unit `t-raw-issue-pull-parity-01.sh`，CORE/CI_CORE 各 +1。
- 验收：
  - 新 raw：pull 后本地含镜像 comment 块，用**真实** `raw_reconciliation.reconcile` + `raw-reconciliation-gate._local_record` 判 `ok=True`、diagnostics 为空（无需任何手工编辑）；
  - 终态 raw：连续 pull 后 `phase_state: absorbed` / `platform_state: closed` 不变；
  - 幂等：连续两次 pull 不生成第二个 comment 块；
  - 基线负向控制：develop 的 pull 确实会丢 comments、判 diverged、把 absorbed 降级成 proposed。
- 不退化边界：
  - **不放宽** `raw_reconciliation` 的 comments/labels/state 任一比较；不改 canonical projection；
  - 不改 `promote-finalize` 的 comment 内容，不改 `fetch_issue` 的返回结构；
  - 不改 `issue-sync batch` / `cmd_close` / 任何门禁；
  - 新 raw 仍按平台 `phase/*` 起始为 `proposed`（不改变首次物化语义）。
