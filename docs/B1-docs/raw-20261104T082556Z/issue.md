---
schema_version: '1'
local_id: raw-20261104T082556Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T082556Z-A
platform_ids:
  github:
    issue_id: '4183'
    url: https://github.com/chatterzhao/freely/issues/4183
    synced_at: ''
  gitee:
    issue_id: IKSWRD
    url: https://gitee.com/zhaoquan/freely/issues/IKSWRD
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/platform/raw-20261104T082556Z/issues/I-20261104T082556Z-A.md
last_synced_comment_at:
  github: '2026-11-07T13:07:16Z'
  gitee: '2026-11-07T13:07:16Z'
hash: ''
created_at: '2026-11-04T08:25:56Z'
updated_at: '2026-11-07T13:31:41Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T082556Z-A
source_candidate: ''
completed_at: '2026-11-07T13:03:01Z'
closeout_note: ''
---

# fix: issue-sync promote 到 B2 的 I-* 时找不到文件，必然失败

workflow_kind: fix

## 根因
`issue-sync promote` 在创建 I-* 平台 issue 时调用 `cmd_create "$i_id"`，而 `cmd_create` 固定读 `docs/B1-docs/<local_id>/issue.md`。I-* 实际位于 `docs/B2-docs/**/issues/`，因此 promote 必然报文件不存在。

## 证据
- `bin/issue-sync` 的 `cmd_promote()`：`cmd_create "$i_id"`。
- `cmd_create()`：`file="$ISSUES_DIR/$local_id/issue.md"`（`ISSUES_DIR=docs/B1-docs`）。
- 实测：`issue-sync promote raw-20261104T074512Z I-20261104T074512Z-A` 输出 `[ERROR] docs/B1-docs/I-20261104T074512Z-A/issue.md not found`。
- 同一命令的 `promote-finalize` 依赖 `promoted_children`，promote 失败后 finalize 也失败。

## 影响
- B1 → B2 的平台同步链路断开：I-* 无法在平台创建，raw 无法正常 finalize。
- 只能手工 `issue-sync close` + 手改 phase_state 绕过，产生状态分叉。

## 修复方案
1. `cmd_create` 支持 B2 路径解析：先查 `docs/B1-docs/<id>/issue.md`，再查 `docs/B2-docs/**/issues/<id>.md`。
2. `cmd_promote` 改为直接按 I-* 文件路径创建，不依赖 `cmd_create` 的 B1 假设。
3. 补单测：promote 一个 B2 I-* 成功创建平台 issue 并写回 `platform_ids`。

## 验收标准
- RED：对 B2 的 I-* 执行 promote，断言平台 issue 创建成功；当前报文件不存在。
- GREEN：promote + promote-finalize 全链路成功，raw 变 absorbed 且平台关闭。
- GREEN：`platform_ids` 在 I-* 文件中被回写。

### comment-20261107T130301Z
- source: system
- event: promote_finalized
- children: ["I-20261104T082556Z-A"]

拆解为以下任务:
1. [I-20261104T082556Z-A](will-be-updated)
