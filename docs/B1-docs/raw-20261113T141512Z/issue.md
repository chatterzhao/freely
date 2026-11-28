---
schema_version: '1'
local_id: raw-20261113T141512Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261113T141512Z-A
platform_ids:
  github:
    issue_id: '4436'
    url: https://github.com/chatterzhao/freely/issues/4436
    synced_at: ''
  gitee:
    issue_id: IKV86B
    url: https://gitee.com/zhaoquan/freely/issues/IKV86B
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/issues/I-20261113T141512Z-A.md
last_synced_comment_at:
  github: '2026-11-28T09:09:18Z'
  gitee: '2026-11-28T09:09:18Z'
hash: ''
created_at: '2026-11-13T14:15:12Z'
updated_at: '2026-11-28T09:09:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261113T141512Z-A
source_candidate: ''
completed_at: '2026-11-28T09:09:17Z'
closeout_note: ''
severity: P2
---

# fix: status/scan 只读视图语义错，空 agent_working 与无同步历史都会误判

workflow_kind: fix

## fix: status/scan 只读视图语义错，空 agent_working 与无同步历史都会误判

| Field | Value |
|-------|-------|
| local_id | `raw-20261113T141512Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-13T14:15:12Z |
| updated | 2026-11-13T14:15:12Z |

---

> **Freely 治理**：这是 raw issue `raw-20261113T141512Z`。实现前请用 `wt-create --raw-key 20261113T141512Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象 1：`status --view live` 整视图不可用

    ./bin/freely status --view live
    [ERROR] owner-lane claim skipped: no claim: rows_unreadable: AgentWorkingError
    [ERROR] unable to resolve agent identity for <project>: agent_working has no entry
    [ERROR] agent-table: unable to resolve agent identity (agent_working empty) — fail-closed

只读视图在 `agent_working` 表为空时**整体 fail-closed**，连 baseline/live 的 issue 状态都看不到。空表是「没有活跃 agent」的正常状态，不是错误。

## 现象 2：`issue-sync scan` 把「没同步过」当成「有变更」

    ./bin/freely issue-sync --project <工位> scan
    last_sync_at: never
    Changed issues since last sync:
      CREATE raw-20260502T000000Z ...
      ...（17 条，全部是历史 legacy 文档）

`scan` 以 `_scan_state_get last_sync_at` 为变更源；从未同步过（never）+ 空 scan-state 时，把所有历史文档当成变更。这些「CREATE」并不是真的要在平台新建（很多只是本地缺 platform_ids 或 phase 为 dropped），会误导执行者去跑全量 batch。

## 期望

1. `status`：`agent_working` 为空 → 降级为 info（「no active agents」），baseline / live / fleet 的 issue 状态照常输出；只有真正读表失败（DB 不可用、schema 错）才 fail-closed。
2. `scan`：改成**平台对账视图**——逐条比较「本地 phase/platform_state」与「平台实际状态」，只报真实差异（本地 completed 但平台 open、本地 open 但平台 closed、platform_ids 缺失等）；`last_sync_at` 只用于显示「上次同步时间」，不再作为变更判据。
3. `scan` 输出按差异类型分组并给出建议动作（`issue-sync batch` 仅本 raw / governance-only lane 全量），避免「17 条 CREATE」这种不可执行的噪声。
4. AT：
   - agent_working 空时 `status --view live` rc=0 且输出 issue 段；
   - scan 在「本地与平台一致」时输出 0 条差异（负向控制：无 scan-state 也不误报）；
   - scan 在「本地 completed、平台 open」时报告该条并给出建议动作。

## 边界

- 不改 `issue-sync batch` 的收口判据（那是 #4349 / R33.18 的范围）；
- 不放宽任何门禁；不引入新的平台写通道。

### comment-20261128T090918Z
- source: system
- event: promote_finalized
- children: ["I-20261113T141512Z-A"]

拆解为以下任务:
1. [I-20261113T141512Z-A](will-be-updated)
