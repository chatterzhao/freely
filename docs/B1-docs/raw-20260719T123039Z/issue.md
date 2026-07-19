---
local_id: raw-20260719T123039Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T123039Z-A
platform_ids:
  github:
    issue_id: '4014'
    url: https://github.com/chatterzhao/freely/issues/4014
    synced_at: ''
  gitee:
    issue_id: IK21VM
    url: https://gitee.com/zhaoquan/freely/issues/IK21VM
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T12:31:02Z'
updated_at: '2026-07-19T12:31:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因

Python/DB层(agent_working.py, freely_db_manager.py)的agent_next_free/agent_assign/agent_release_all逻辑全部正确。断点在shell调用层传参错误(L13310 slot用AGENT_AI_TOOL, L13110 agent_id格式不对+错误被吞)。

已有PR修复了shell层传参。但还有问题:
1. 旧agent_working行worker_id=NULL, slot=claude → 需清理
2. 测试全是grep -c查代码存在, 不验证DB实际值 → GREEN但worker_id仍然是NULL
3. 没有端到端测试验证 agent_next_free→assign→release 完整生命周期

## 修复

1. 清理旧agent_working行(worker_id=NULL的无用行)
2. 新增测试: 直接查SQLite验证agent_working写入正确
3. 测试覆盖: assign写入→next_free排除→release释放→next_free恢复
