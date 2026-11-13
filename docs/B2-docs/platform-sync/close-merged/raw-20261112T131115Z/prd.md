# PRD: issue-sync close 支持 kind=linked

- issue_id: I-20261112T131115Z-A
- source_raw: raw-20261112T131115Z
- workflow_kind: fix
- milestone: M-20261112T131115Z-A
- story: platform-sync/close-merged（复用既有 story）

## 目标

让 `issue-sync close <I-id>` 可用：按 kind 分派，linked 文档走独立校验与同一 adapter 关单，
成功后本地 `status: closed`；raw 路径的严格契约保持原样。

## 唯一改动范围

- `bin/issue-sync.d/cmd-close.sh`：读取 kind，linked → `close-linked`。
- `docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py`：新增 `close_linked` + CLI 分派。
- 新增 AT `docs/system/workspace/scripts/tests/test-issue-sync-close-linked.py`。
- 新增 unit `docs/system/workspace/scripts/tests/unit/t-linked-close-01.sh`。
- `bin/test-all` 的 CORE / CI_CORE 各 +1。

## 不退化边界

- raw 的 `validate()`、`transition`、`close_platforms` 一行不改；仍拒绝 linked。
- 平台写只经 `platform-adapter.py close-multi`；禁止直连 gh/gitee。
- 不改 promote / promote-finalize；不改 phase 状态机；不新增 phase 枚举。

## 功能需求

- FR-1：全绿关单 → rc=0，文档 `status: closed` + `updated_at` 更新，body 与所有 linked 字段逐字保留。
- FR-2：部分/失败 → rc!=0 且文档字节不变（可重试）。
- FR-3：`close-linked` 对 kind=raw 拒绝并给出原因。
- FR-4：`close-platforms` 对 linked 仍报 raw 契约错误（一致性守卫）。

## 验收

AT-001 RED `7 ok / 8 failed`（develop 基线）→ GREEN `15 ok / 0 failed`；unit `6 ok / 0 failed`；
`bin/test-all --ci` 全绿；三门禁不变。
