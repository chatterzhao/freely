---
local_id: raw-20260719T071858Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260719T071858Z-A
platform_ids:
  github:
    issue_id: '4003'
    url: https://github.com/chatterzhao/freely/issues/4003
    synced_at: ''
  gitee:
    issue_id: IK214Q
    url: https://gitee.com/zhaoquan/freely/issues/IK214Q
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-19T07:19:22Z'
updated_at: '2026-07-19T07:19:22Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

Manager prompt 模板（runtime/freely 中的 `_manager_exit_contract_instructions` 或等效段落）的 a2a-exit 示例缺少 `--role worker`：

```bash
# 当前（错误）
a2a-exit --state submitted --summary "created 3 workers" --workers "..."

# 应为
a2a-exit --state submitted --role worker --summary "created 3 workers" --workers "..."
```

同时 a2a_task.py L830 `--role` 有默认值 `default="manager"`——当 Manager AI 按模板调用时忘传 `--role`，task 就以 `agent_id=manager` 创建，Runtime `list --role worker` 查不到。

## 完整故障链

```
Manager AI 按 prompt 模板调用 a2a-exit
  ↓ 模板缺 --role worker
a2a_task.py: --role 默认 manager → agent_id=manager
  ↓
A2A tasks 表: agent_id=manager（错误! 应为 worker）
  ↓
Runtime: list --role worker --status submitted → 查不到
  ↓
worker_prompts_csv=none → Worker ACP session 永不启动
  ↓
agent_dead
```

## 证据

1. A2A DB: 本轮 2 个 task agent_id=manager, 但 message 是 Worker 内容 ("# Worker: Fix...")
2. runtime-events.log: worker_prompts_csv=none
3. lifecycle-trace.log: delegate_workers 后直接回到 prompt_build_begin, 无 worker bridge 启动
4. Manager prompt 模板 (prompt-20260719-000621.txt L481-490): 示例无 --role worker

## 修复

1. Manager prompt 模板: a2a-exit 模板和示例加上 `--role worker`
2. a2a_task.py: `--role` 移除默认值, 改为 required=True, 或至少 default=worker 对委派场景更安全
3. 清理: 关闭/删除 agent_dead 的旧空 message worker task (message='')

## 影响

所有新委派的 Worker task 均无法被 Runtime 发现, 整条 Worker 委派链路断掉。Manager 运行正常但 Worker 永远不启动。
