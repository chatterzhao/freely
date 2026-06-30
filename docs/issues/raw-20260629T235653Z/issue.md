---
local_id: raw-20260629T235653Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260629T235653Z-A
platform_ids:
  github:
    issue_id: '3637'
    url: https://github.com/chatterzhao/freely/issues/3637
    synced_at: ''
  gitee:
    issue_id: IJXOT4
    url: https://gitee.com/zhaoquan/freely/issues/IJXOT4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-29T23:57:13Z'
updated_at: '2026-06-29T23:57:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

AGENTS.md 第 155-156 行：

    - 步骤 2-9 由 Worker 在 skill 约束下完成，完成后写 handoff JSON 汇报
    - wt-close 会自动消费该工位的所有 worker handoff

已被 three-loop-capability-lifecycle.md 第 39 行明确标记为过时：

    旧 handoffs 文件/表语义已被 a2a_tasks 取代。

实际运行时 Worker 通过 a2a-exit --state completed 更新 A2A Task，wt-close 通过 a2a_task.py auto-consume 消费。

注：LAWS.md 和 skills 中的 fresh_with_handoff 是 continuity launch kind（会话上下文交接），不是旧 worker handoff JSON，概念不同，不需要改。

## 改动

AGENTS.md 第 155-156 行改为 A2A tasks 表述。
