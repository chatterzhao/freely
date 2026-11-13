# PRD: pull 与平台副本保持天然一致

- issue_id: I-20261113T084851Z-A
- source_raw: raw-20261113T084851Z
- workflow_kind: fix
- milestone: M-20261113T084851Z-A
- story: platform-sync/close-merged（复用既有 story，epics-map.svg 无需改动）

## 目标

让 `raw-issue-pull` 产出的本地文档**天然**满足 `raw-reconciliation-gate` 的双向镜像契约：
平台评论有本地 comment 块，本地终态不被创建时快照标签降级。
目标是消除「手工编辑文档去凑门禁」这一绕过手法，而不是降低门禁强度。

## 唯一改动范围

- `docs/system/workspace/scripts/sync/platform-adapter.py::pull_raw_issue`：评论镜像 + 终态保护。
- 新增 AT `docs/system/workspace/scripts/tests/test-raw-issue-pull-parity.py`。
- 新增 unit `docs/system/workspace/scripts/tests/unit/t-raw-issue-pull-parity-01.sh`。
- `bin/test-all` 的 CORE / CI_CORE 各 +1。

## 不退化边界

- `raw_reconciliation.py` / `raw-reconciliation-gate.py` 一行不改；
- `promote-finalize` / `fetch_issue` / `issue-sync batch` / `cmd_close` 不改；
- 首次物化的 `phase_state: proposed` 语义不变；`validate()` 的严格契约不变；
- 不新增 CLI 参数、不新增 phase 枚举、不引入「手工补 comment 块」的流程。

## 功能需求

- FR-1：pull 读取 `details["comments"]` 并写成可被引擎解析的 `### comment-*` 块；
- FR-2：pull 后 `reconcile(local, replica)` 为 `ok=True` 且 diagnostics 为空（不依赖人工编辑）；
- FR-3：本地终态 raw 再 pull 时 `phase_state` / `platform_state` 等终态字段逐字保留；
- FR-4：重复 pull 不累积重复 comment 块；
- FR-5：develop 基线跑同一 AT 必须复现「丢 comments / 判 diverged / 降级 absorbed」三项红。

## 验收

AT-001 RED `6 ok / 10 failed`（develop `02ee82705` 快照，基线控制 R1–R3 全通过）→ GREEN `13 ok / 0 failed`；
unit `4 ok / 0 failed`；`bin/test-all --ci` 全绿；三门禁不变。
