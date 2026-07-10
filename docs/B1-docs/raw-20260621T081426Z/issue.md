---
local_id: raw-20260621T081426Z26Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T081426Z-A
platform_ids:
  github:
    issue_id: '3208'
    url: https://github.com/chatterzhao/freely/issues/3208
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T08:14:45Z'
updated_at: '2026-06-21T09:46:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

人类 chat → Manager → worker 的介入通路设计是正确的，但 `.freely/intake/` → `docs/issues/` 的存储迁移卡在半路，导致链路断裂：

### 断裂点 1: `handle_interruption_intake_once` 对 raw-* 直接 return 0

`freely` L18692-18697: 遇到 `docs/B1-docs/raw-*` 的 intake 项时直接 early return，注释说 "deferred to handler migration"。但迁移从未完成，导致所有 chat 消息被静默丢弃。

### 断裂点 2: `append_human_chat_intake_if_needed` 仍从旧位置读取

`freely` L15928: `intake_snapshot_for_project` 只读 `.freely/intake/`，但 `write_intake_item`（L6063）已不再写入该目录。Manager patrol 永远看到空的 intake 队列。

### 断裂点 3: `a2a_task.py prompt` 存在但从未被运行时调用

`a2a_task.py prompt`（L725-736）已完整实现，Manager agent 文档中也指示使用，但 `freely` 脚本中无任何调用。Manager 无法实际向 worker 发送 steer 消息。

### 断裂点 4: `steer` reaction 无 dispatch 逻辑

`apply_interruption_manager_decision`（L18632）只处理 `answer` 和 `delegate`。`steer` 在 validation 中存在但无任何动作。

## 设计（不改架构，只完成迁移）

### 1. 修复 intake 消费

`handle_interruption_intake_once` 对 raw-* 项不应 early return，应：
- 读 issue.md frontmatter（status=proposed → 待处理）
- 调 `interruption-manager-handler` triage
- 根据 DECISION 分发

同时修复 `intake_snapshot_for_project` 从 `docs/B1-docs/raw-*` 读取（status=proposed 的项）。

### 2. 实现 steer dispatch

`apply_interruption_manager_decision` 增加 `steer` case:
- 找到目标 worker（通过 raw_key）
- worker session alive → `a2a_task.py prompt`
- worker session dead → `fork+handoff`

### 3. Manager patrol 集成

Manager patrol Step 1.5: 拉取 `status=proposed` 的 raw-* intake，分拣为 steer/followup/collect，按优先级并入 patrol 决策。

## 不改的部分

- chat → intake 存储路径：`docs/B1-docs/raw-*` ✓（已完成）
- interruption-manager-handler 的快速路径 + AI triage：✓（已实现，只需重新接通）
- a2a_task.py prompt 的 ACP session/prompt 机制：✓（已实现，只需 wiring）
- 人类的旁路注入角色：✓（设计正确）
- Manager 的唯一决策者角色：✓（设计正确）
