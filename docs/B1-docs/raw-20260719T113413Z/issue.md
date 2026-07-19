---
local_id: raw-20260719T113413Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T113413Z-A
platform_ids:
  github:
    issue_id: '4012'
    url: https://github.com/chatterzhao/freely/issues/4012
    synced_at: ''
  gitee:
    issue_id: IK21RX
    url: https://gitee.com/zhaoquan/freely/issues/IK21RX
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T11:34:36Z'
updated_at: '2026-07-19T11:34:36Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

L13110 acp_session_register 调用时 slot 和 agent_id 未正确解析:

1. slot='${slot:-claude}' — $slot未设置 → 默认claude(Manager的tool), 永远写不对
2. ${agent_id} — 可能是role字符串(worker)而非实例ID(worker_01)
3. || true 吞掉L3校验错误 — 写入失败无感知

agent-table.toml 定义了每个role的slot和id, 但代码未正确使用。

## 修复

所有 agent_assign/acp_session_register 调用点:
1. slot从agent-table解析(agent-table-query --get-slot worker_01)
2. agent_id: Manager用manager_01, Worker用agent_next_free, Reviewer用reviewer_next_free
3. 错误不要吞掉 — 去掉|| true或至少log_warn
