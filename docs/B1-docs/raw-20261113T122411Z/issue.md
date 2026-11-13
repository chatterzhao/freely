---
schema_version: '1'
local_id: raw-20261113T122411Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T122411Z-A
platform_ids:
  github:
    issue_id: '4346'
    url: https://github.com/chatterzhao/freely/issues/4346
    synced_at: ''
  gitee:
    issue_id: IKV7NT
    url: https://gitee.com/zhaoquan/freely/issues/IKV7NT
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-create-resume-test-worktree/raw-20261113T122411Z/issues/I-20261113T122411Z-A.md
last_synced_comment_at:
  github: '2026-11-13T12:40:40Z'
  gitee: '2026-11-13T12:40:40Z'
hash: ''
created_at: '2026-11-13T12:24:11Z'
updated_at: '2026-11-13T12:50:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T122411Z-A
source_candidate: ''
completed_at: '2026-11-13T12:40:40Z'
closeout_note: ''
severity: P1
---

# fix: wt-close children 报告空 platform_state 导致 TSV 列错位，收口必失败

workflow_kind: fix

## fix: wt-close children 报告空 platform_state 导致 TSV 列错位，收口必失败

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T122411Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T12:24:11Z |
| updated | 2026-11-13T12:24:11Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T122411Z`。实现前请用 `wt-create --raw-key 20261113T122411Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

R33.15（#4343，已合并 `f1be6b5c3`）新增 `wt-close` Phase 2.5 收口所有 I-* children 后，真机收口立即失败：

    wt-close: closing I-* issue: I-20261113T115957Z-A
    Error: no platform_ids for I-20261113T115957Z-A
    Error: platform close failed for I-20261113T115957Z-A; cleanup stopped

但该 I-* 文档的 `platform_ids` 明明是齐全的（github 4344 / gitee IKV7KY）。

## 根因（已定位）

Phase 2.5 用 TSV 在 python 与 bash 之间传 children 报告：

    print("%s\t%s\t%s\t%s" % (child, phase_state, platform_state, path))

bash 侧用 `while IFS=$'\t' read -r cid phase platform_state path` 解析。

**当 `platform_state` 为空时**（`promote-finalize` 后 linked 文档通常没有该字段），输出是 `child\tcompleted\t\t/path`。bash 的 IFS 把 tab 当作**空白字符**，连续 tab 会被折叠，于是：

- `platform_state` = `/path`
- `path` = 空

`_close_platform_ids_readonly "" "$cid"` → `_fm_get ""` 读不到文件 → 空 → 报 `no platform_ids`。

AT 的 fixture 当时都给了非空 `platform_state`（open/closed），所以没覆盖真实形状。

## 影响

- 本轮 R33.15 的工位卡在 merge 之后、wt-close 之前（工位残留，平台 raw 已 closed、child 未关）。
- 任何 `platform_state` 为空的 I-*（即 promote-finalize 后的默认形状）都会触发，属**稳定复现**。

## 期望

1. 空字段不得输出空 TSV 列：用占位符（如 `-`）或改用非空白分隔符（`\x1f`）；bash 侧对应处理。
2. 增加 AT 用例：`platform_state` 为空时仍能正确定位并关闭两个 children（负向控制：修复前必须红）。
3. 修复后重跑 R33.15 的 `wt-close --raw-key 20261113T115957Z`，确认 child 被关闭、工位被清理。

## 边界

- 只改 `wt-close` Phase 2.5 的序列化与对应 AT；
- 不改 R33.15 的其余逻辑（遍历 promoted_children / 终态门禁 / 逐个关闭）；
- 不放宽任何门禁；不手工关平台 issue。

### comment-20261113T124040Z
- source: system
- event: promote_finalized
- children: ["I-20261113T122411Z-A"]

拆解为以下任务:
1. [I-20261113T122411Z-A](will-be-updated)
