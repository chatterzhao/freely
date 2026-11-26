---
schema_version: '1'
local_id: raw-20261124T131119Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261124T131119Z-A
platform_ids:
  github:
    issue_id: '4687'
    url: https://github.com/chatterzhao/freely/issues/4687
    synced_at: ''
  gitee:
    issue_id: IKXQN7
    url: https://gitee.com/zhaoquan/freely/issues/IKXQN7
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/issues/I-20261124T131119Z-A.md
last_synced_comment_at:
  github: '2026-11-26T07:37:02Z'
  gitee: '2026-11-26T07:37:02Z'
hash: ''
created_at: '2026-11-24T13:11:19Z'
updated_at: '2026-11-26T07:37:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261124T131119Z-A
source_candidate: ''
completed_at: '2026-11-26T07:37:01Z'
closeout_note: ''
severity: P2
---

# fix: 无封装命令可关闭 stale linked 孤儿副本（部分成功反模式）

workflow_kind: fix

## fix: 无封装命令可关闭 stale linked 孤儿副本（部分成功反模式）

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T131119Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/issues/I-20261124T131119Z-A.md` |
| created | 2026-11-24T13:11:19Z |
| updated | 2026-11-24T13:11:19Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T131119Z`。实现前请用 `wt-create --raw-key 20261124T131119Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
R60.1 的 linked issue I-20261124T054201Z-A 留下 GitHub 孤儿副本 #4678（标题前缀 [I-...]，body phase_state: done_b2_ibm，平台 OPEN）；canonical #4680 与 Gitee IKXP2V 均已 CLOSED。现有 packaged 命令均够不到该孤儿：issue-sync close 对 schema_version=1 linked 显式拒绝；issue-sync batch 因 doc platform_state: closed 直接跳过；wt-close --platform-only 按 [RAW-<key>] 标题前缀解析身份，匹配不到 [I-...] 标题。

## 风险
为了关掉它只能手工 import platform_adapter 调 close_issue() 并自拼 platform_ids={github:4678}，回执变成 github: closed / gitee: error no issue_id —— 正是 R60.2 刚修掉的「部分成功伪装整体成功」反模式，绕过双平台原子性，且给后续会话留下错误先例。

## 期望
提供封装入口：按 local_id 枚举并关闭平台上所有真实副本（含 title 前缀不符的 stale linked 孤儿），双平台结果汇总、任一失败非零退出；诊断必须可操作（打印可直接执行的封装命令）。严禁手工调用内层 adapter / 子命令 / 自拼 platform_ids 来兜底。

### comment-20261126T073701Z
- source: system
- event: promote_finalized
- children: ["I-20261124T131119Z-A"]

拆解为以下任务:
1. [I-20261124T131119Z-A](will-be-updated)
