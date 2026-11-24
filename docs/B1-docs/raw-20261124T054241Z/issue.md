---
schema_version: '1'
local_id: raw-20261124T054241Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261124T054241Z-A
platform_ids:
  github:
    issue_id: '4672'
    url: https://github.com/chatterzhao/freely/issues/4672
    synced_at: ''
  gitee:
    issue_id: IKXKZ8
    url: https://gitee.com/zhaoquan/freely/issues/IKXKZ8
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/issues/I-20261124T054241Z-A.md
last_synced_comment_at:
  github: '2026-11-24T11:20:49Z'
  gitee: '2026-11-24T11:20:49Z'
hash: ''
created_at: '2026-11-24T05:42:41Z'
updated_at: '2026-11-24T11:21:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261124T054241Z-A
source_candidate: ''
completed_at: '2026-11-24T11:20:48Z'
closeout_note: ''
severity: P1
---

# fix: agent_session_restore 恒返回 0，部分恢复失败被误判成功

workflow_kind: fix

## fix: agent_session_restore 恒返回 0，部分恢复失败被误判成功

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T054241Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-24T05:42:41Z |
| updated | 2026-11-24T05:42:41Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T054241Z`。实现前请用 `wt-create --raw-key 20261124T054241Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

`docs/system/workspace/scripts/runtime/agent_session_restore.py:73-80` 的 `main()` 逐条打印 outcome（resumed / failed / slot_unavailable），但无论结果如何恒 `return 0`。外部调用者只看退出码会把部分恢复失败当作整体成功。

## 影响

Runtime 重启后若部分 Worker/Reviewer 的 ACP `session/resume` 失败，进程看起来已恢复、实际有 Agent 缺席。与 fail-closed 原则冲突。相邻 `watchdog_sse.py` 也存在捕获异常后忽略、连续失败在日志里消失的路径（需单独核实，不在本条 scope）。

## 修复方向

- main() 汇总 resumed / failed / slot_unavailable 计数并打印结构化摘要。
- 存在 failed 或关键 Agent 未恢复时非零退出；slot_unavailable 按策略区分处理。
- 不改变 `resume_persisted_sessions()` 的返回结构（现有调用方依赖）。

## 验收

- RED：mock 一条 resume 抛异常，main() 非零退出。
- GREEN：全部 resumed 时行为与当前一致，退出码 0。

### comment-20261124T112049Z
- source: system
- event: promote_finalized
- children: ["I-20261124T054241Z-A"]

拆解为以下任务:
1. [I-20261124T054241Z-A](will-be-updated)
