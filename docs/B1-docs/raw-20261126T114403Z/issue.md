---
schema_version: '1'
local_id: raw-20261126T114403Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261126T114403Z-A
platform_ids:
  github:
    issue_id: '4722'
    url: https://github.com/chatterzhao/freely/issues/4722
    synced_at: ''
  gitee:
    issue_id: IKY9I7
    url: https://gitee.com/zhaoquan/freely/issues/IKY9I7
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/issues/I-20261126T114403Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-26T11:44:04Z'
updated_at: '2026-11-26T11:44:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children:
- I-20261126T114403Z-A
source_candidate: docs/B1-docs/raw-20261126T114403Z/candidates.md#C-20261126T114403Z-A
completed_at: '2026-11-26T12:20:00Z'
closeout_note: '已由 I-20261126T114403Z-A 完整实现并 GREEN'
severity: P2
---

# feat: issue-sync close-orphans 批量模式复用平台读取

workflow_kind: feature

## feat: issue-sync close-orphans 批量模式复用平台读取

| Field | Value |
|-------|-------|
| local_id | `raw-20261126T114403Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/issues/I-20261126T114403Z-A.md` |
| created | 2026-11-26T11:44:04Z |
| updated | 2026-11-26T11:44:04Z |

---

> **Freely 治理**：这是 raw issue `raw-20261126T114403Z`。实现前请用 `wt-create --raw-key 20261126T114403Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
P1-3 清理 48 个 completed/dropped linked 孤儿副本时，逐 ID 调用 `freely issue-sync close-orphans <id> linked`，每次都经 adapter `list_open_issue_records()` 全量拉取 GitHub+Gitee 的 OPEN issue。实测单 ID 约 60–90 秒，48 个接近一小时；期间 Gitee 偶发抖动导致 rc=3 部分成功，需要人工重试。

## 根因
`bin/issue-sync.d/cmd-close.sh:cmd_close_orphans()` 每次调用都重新发现副本，未复用已经读取的 records；adapter 的 `close_local_id()` 接口只接受单个 local_id。平台读取次数与 local_id 数成正比，是 O(N) 全量扫描。

## 期望
新增 `freely issue-sync close-orphans --all-completed [--kind linked|raw]`：一次 `list_open_issue_records()`，按本地 `phase_state ∈ {completed, dropped}` 枚举 local_id，复用同一份 records 计算每个 id 的副本并逐平台关闭。输出逐 id 汇总（closed/absent/error）与可直接执行的 retry 命令；沿用 0/3/1 退出码语义。

## 边界
- 不放宽 terminal 判据，不关闭非 completed/dropped 的本地文档；
- 不写平台以外的新通道，不改本地 frontmatter；
- 单 id 模式行为逐字不变；Gitee 抖动仍显式报错，禁止吞错；
- 不新增绕过 raw-reconciliation 的快捷路径。

## 验收
- fixture：60 个本地 terminal linked 文档 + 双平台 200 个副本，stub 记录 `list_open_issue_records` 调用次数必须为 1，全部关闭 rc=0；
- 单平台失败：rc=3 且打印逐 id `freely issue-sync close-orphans <id> linked` 重试命令；
- 非 terminal 文档对应副本保持 OPEN；
- 与逐 id 模式结果集合一致（差集为空）。
