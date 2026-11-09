---
schema_version: '1'
local_id: raw-20261104T075910Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T075910Z-A
platform_ids:
  github:
    issue_id: '4163'
    url: https://github.com/chatterzhao/freely/issues/4163
    synced_at: ''
  gitee:
    issue_id: IKSW98
    url: https://gitee.com/zhaoquan/freely/issues/IKSW98
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261104T075910Z/issues/I-20261104T075910Z-A.md
last_synced_comment_at:
  github: '2026-11-09T08:22:20Z'
  gitee: '2026-11-09T08:22:20Z'
hash: ''
created_at: '2026-11-04T07:59:10Z'
updated_at: '2026-11-09T08:22:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261104T075910Z-A
source_candidate: ''
completed_at: '2026-11-09T08:22:19Z'
closeout_note: ''
---

# fix: freely.db 单写者不变量被多处直连破坏

workflow_kind: fix

## 根因
架构声明 `freely_db_manager.py` 持有单 SQLite connection，但多处代码绕过 db manager 直连 `.freely/freely.db`，并各自建表，单写者不变量已失效。

## 证据
- `runtime/task-lifecycle-scan.py:599-605` 直接 `sqlite3.connect(<project>/.freely/freely.db)`。
- `runtime/watchdog_sse.py:378-382` 同样直连。
- 另有 `runtime/agent_protocol.py:80`、`runtime/handoff_store.py:42`、`runtime/discussion_events.py:175` 各自 connect 并自带 schema。
- `three-loop-capability-lifecycle.md` 明确「`freely_db_manager.py` 持有单 SQLite connection」。

## 影响
- 单写者假设被破坏；WAL 并发下可能读到半提交状态。
- 3 个辅助 store 无 schema 文档、无迁移路径。
- 排查数据问题时无法确定唯一写入方。

## 修复方案
1. 读路径统一走 `freely-db-cli` 或显式 `mode=ro`；写路径只允许 db manager。
2. 辅助 store 登记进 State 契约：表名、列、owner、迁移脚本。
3. 加 boundary lint：`sqlite3.connect` 只允许出现在 db manager 与显式只读连接处。
4. 补并发测试：两个写者同时写同一表，断言不出现半提交读。

## 验收标准
- RED：当前 `grep -rn "sqlite3.connect" scripts/` 命中 ≥6 处；修复后只允许 db manager + 显式只读连接。
- GREEN：`freely.db` 的所有写入都能追溯到 db manager。
- GREEN：3 个辅助 store 在 State 契约中有表结构与迁移记录。
- GREEN：并发写测试通过，无半提交读。

### comment-20261109T082220Z
- source: system
- event: promote_finalized
- children: ["I-20261104T075910Z-A"]

拆解为以下任务:
1. [I-20261104T075910Z-A](will-be-updated)
