---
local_id: raw-20260719T074532Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T074532Z-A
platform_ids:
  github:
    issue_id: '4006'
    url: https://github.com/chatterzhao/freely/issues/4006
    synced_at: ''
  gitee:
    issue_id: IK216N
    url: https://gitee.com/zhaoquan/freely/issues/IK216N
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T07:45:55Z'
updated_at: '2026-07-19T07:45:55Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

agent-table.toml 的设计是: worker_id=worker_01(pool=10) = worker_01~10 共 10 个实例。agent_working.py 已实现 agent_next_free 和 agent_assign 函数。但 Runtime 的 worker launch 流程有两处断点:

1. freely L6064: agent_assign 写 agent_working 时 raw_key 硬编码为 'develop' 而非实际 raw_key
2. a2a_task.py L1112: a2a-exit 创建 task 时 agent_id 用 role 字符串而非 agent_next_free 返回的实例 ID

结果: agent_working.worker_id 永远是 NULL(写入了错误的 raw_key 行), a2a_tasks.agent_id 永远是 'worker'(role 字符串)

## 当前 vs 目标

当前:
  agent_working.worker_id = NULL
  a2a_tasks.agent_id = 'worker'
  Runtime: WHERE agent_id = 'worker'

目标:
  Manager 委派时: agent_next_free('worker', 10) → worker_03
  agent_working.worker_id = 'worker_03:session_xxx' (正确的 raw_key 行)
  a2a_tasks.agent_id = 'worker_03'
  Runtime: WHERE agent_id LIKE 'worker_%'

## 修复

1. freely L6064: agent_assign 的 raw_key 参数改为实际 raw_key
2. a2a_task.py L1112: agent_id 从 args.role 改为由调用方传入的实际实例 ID
3. Manager prompt 模板: 委派前调用 agent_next_free 获取实例 ID, 传给 a2a-exit --agent-id worker_NN
4. Runtime worker 发现: WHERE agent_id LIKE 'worker_%' 替代等值匹配
