---
local_id: raw-20260719T101009Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T101009Z-A
platform_ids:
  github:
    issue_id: '4010'
    url: https://github.com/chatterzhao/freely/issues/4010
    synced_at: ''
  gitee:
    issue_id: IK21L4
    url: https://gitee.com/zhaoquan/freely/issues/IK21L4
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T10:10:32Z'
updated_at: '2026-07-19T10:10:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

freely L13258-13264: worker launch fork路径用Worker的base_tool(opencode)去查Manager的bridge socket。

```bash
_worker_slot=opencode-apikey-ds-flash-auto
_worker_base=opencode  # Worker的tool
_manager_bridge_socket=$(_acp_bridge_socket $manager_project $worker_base)
# → /tmp/freely-acp-xxx-opencode.sock ← Manager的opencode bridge不存在(Manager用claude)
```

ACP session/fork不能跨bridge。不同base_tool之间fork必然失败。

## 修复

L13258-13266 改为:

1. 取Manager的base_tool (从AGENT_AI_TOOL或agent-table-query --get-slot manager_01)
2. 比较Manager和Worker的base_tool
3. 相同 → fork from Manager bridge (用Manager的base_tool)
4. 不同 → 先 _ensure_acp_bridge_running Worker的bridge → session/new

## 影响

Worker和Manager配置不同tool配置时, Worker启动失败(超时后fallback到agent mode, 但worker bridge未启动导致最终超时)
