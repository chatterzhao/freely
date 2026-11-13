---
schema_version: '1'
local_id: raw-20261113T084729Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T084729Z-A
platform_ids:
  github:
    issue_id: '4327'
    url: https://github.com/chatterzhao/freely/issues/4327
    synced_at: ''
  gitee:
    issue_id: IKV5QB
    url: https://gitee.com/zhaoquan/freely/issues/IKV5QB
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform-sync/close-merged/raw-20261113T084729Z/issues/I-20261113T084729Z-A.md
last_synced_comment_at:
  github: '2026-11-13T09:41:44Z'
  gitee: '2026-11-13T09:41:44Z'
hash: ''
created_at: '2026-11-13T08:47:29Z'
updated_at: '2026-11-13T09:41:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T084729Z-A
source_candidate: ''
completed_at: '2026-11-13T09:41:44Z'
closeout_note: ''
severity: P1
---

# fix: linked 收口必须回到 batch 驱动与等价强度的 phase_state 门禁

workflow_kind: fix

## fix: linked 收口必须回到 batch 驱动与等价强度的 phase_state 门禁

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T084729Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T08:47:29Z |
| updated | 2026-11-13T08:47:29Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T084729Z`。实现前请用 `wt-create --raw-key 20261113T084729Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 背景：项目设计意图（已核实）

- `bin/issue-sync` 头注释：`raw-* kind: raw` 是 B1 输入，`I-* kind: linked` 是 B2 输入；生命周期 `chat → raw proposed → B1 promotion_started (1:N children) → promotion_finalized (absorbed/open) → configured-platform close (absorbed/closed)`。
- `bin/issue-sync.d/cmd-batch.sh` 是 linked 收口的**唯一驱动路径**：扫描 `docs/B2-docs/**/I-*.md`，`kind=linked` 时先 `cmd_update`，**只有 `phase_state == completed` 才 `cmd_close`**；且前置 `_changed_since_last_sync`（内容 hash 变化）与 `platform_state != closed`。
- `cmd_close` 对 `schema_version: 1` 的文档走 `_raw_effect close-platforms`，其 Phase 1 用 `raw_metadata_contract.transition(..., "platform_closed")` 做**本地严格校验**（终态判据、字段序列、canonical path），非终态一律拒绝且零平台写入。这是一道门禁。

## 缺陷（R33.8 / #4315 的实现违背设计意图）

本轮合并的 `close_linked`（`raw_lifecycle_effects.py`）+ `cmd-close.sh` 按 kind 分派存在三处偏离：

1. **绕过生命周期门禁**：`close_linked` 只校验 `kind == "linked"` 与 `platform_ids` 非空，就调用 adapter `close-multi`。**没有检查 `phase_state`**，因此 `in_dev` / `proposed` 的 linked 文档同样会被关单。原设计里 linked 必须 `completed` 才能收口。
2. **与 batch 单一路径冲突**：AI 逐条执行 `issue-sync close <I-id>` 绕开 `_changed_since_last_sync` 与 batch 的收口驱动，形成第二套收口通道；两套判据未来必然漂移。
3. **回写字段语义不一致**：`close_linked` 只回写 `status: closed` / `updated_at`，而项目里驱动收口的字段是 `phase_state`（batch 判据）与 `platform_state`（batch 跳过判据）。关闭后 batch 仍会把该文档当未收口项反复处理。

## 期望（按设计意图修正，不是放宽门禁）

1. `cmd_close` 处理 linked 时，必须执行**等价强度**的本地校验：`kind=linked`、`phase_state ∈ {completed, dropped}`、`platform_ids` 双平台齐全、`canonical_issue_path` / `pre_tests_path` 指向的文件存在；不满足则拒绝且零平台写入（与 raw 的 Phase 1 对称）。
2. linked 的收口回到 `issue-sync batch` 驱动：`cmd_close <I-id>` 不得成为绕过 batch 判据的独立通道（可拒绝直连调用，或复用 batch 的同一判据函数，保证单一真源）。
3. 成功后回写 `phase_state` / `platform_state`（与 batch 的跳过判据一致），不要引入新的 `status: closed` 语义。
4. AT 必须覆盖：`in_dev` linked 被 `close` 时拒绝且平台零写入（负向控制）；`completed` linked 由 batch 驱动关闭；raw 的严格契约未被放宽。

## 边界

- 不放宽 raw 的 `validate()`；不删 `issue-sync batch` 的 linked 分支；
- 不改 promote / promote-finalize 语义；平台写仍只经 adapter；
- 不引入新的 CLI 子命令或 phase 枚举。

### comment-20261113T094144Z
- source: system
- event: promote_finalized
- children: ["I-20261113T084729Z-A"]

拆解为以下任务:
1. [I-20261113T084729Z-A](will-be-updated)
