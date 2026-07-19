---
local_id: raw-20260719T143409Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T143409Z-A
platform_ids:
  github:
    issue_id: '4021'
    url: https://github.com/chatterzhao/freely/issues/4021
    synced_at: ''
  gitee:
    issue_id: IK22CO
    url: https://gitee.com/zhaoquan/freely/issues/IK22CO
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T14:34:33Z'
updated_at: '2026-07-19T14:34:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
实际实现已支持跨base_tool的Worker/Reviewer启动(fork→session/new)和agent实例ID(worker_01), 但架构文档仍描述旧行为。

## 需修改
1. acp-a2a-architecture.md L77: worker启动从'(ACP fork)'改为'fork(同tool)或session/new(跨tool)'
2. three-loop-capability-lifecycle.md L65: agent_id示例从'worker'改为'worker_01(实例ID)或worker(role)'
3. manager-agent.md L44: Worker启动加跨tool说明
4. manager-agent.md L83: a2a-exit命令示例加--agent-instance参数
