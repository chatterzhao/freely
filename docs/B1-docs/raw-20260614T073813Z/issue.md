---
local_id: raw-20260614T073813Z13Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '2646'
    url: https://github.com/chatterzhao/freely/issues/2646
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-14T07:38:30Z'
updated_at: '2026-06-17T00:20:48Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

A2A 重构（f543f8f2）引入了标准 A2A 协议基础设施（a2a_server.py + a2a_task.py），
但 AI 的退出交接仍然通过文本解析实现：
- AI 输出文本 → freely bash tail 提取 → regex 匹配 json block → json.loads → alias 映射

这导致状态值不可靠（json5 标签、state:clean 等非法值），
且违反标准 A2A 协议中 Agent 通过 TaskStatusUpdateEvent 显式声明状态迁移的原则。

## 设计

让 AI 通过 ACP 工具直接设置 A2A Task 状态：
1. AI patrol 结束时调用 a2a-exit 工具（传 state/summary/workers/next）
2. 工具直接与 A2A Server 通信，创建 Task + TaskStatusUpdateEvent
3. 状态迁移是显式 action，不再需要文本解析
4. 旧 JSON block 解析降级为 fallback

## 范围
- a2a_task.py: 增加 a2a-exit 子命令
- freely bash: parse_a2a_task_json_reply 优先读 A2A Task 的 state
- prompt: 告知 AI 使用 a2a-exit 工具
