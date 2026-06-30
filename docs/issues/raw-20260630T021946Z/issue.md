---
local_id: raw-20260630T021946Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3639'
    url: https://github.com/chatterzhao/freely/issues/3639
    synced_at: ''
  gitee:
    issue_id: IJXQAS
    url: https://gitee.com/zhaoquan/freely/issues/IJXQAS
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T02:20:08Z'
updated_at: '2026-06-30T02:20:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 背景

当前 a2a_tasks 使用自定义状态名 `blocked`，Google A2A 标准对应状态是 `input-required`。且缺少标准终止态 `canceled`。

## 需要改动

### 1. a2a_task.py 状态机
- State 类：`BLOCKED` → `INPUT_REQUIRED`，新增 `CANCELED`
- SQLite CHECK constraint 更新
- 所有 `state=blocked` → `state=input-required`

### 2. 所有消费者
- wt-close：`state=input-required` 检测
- manager cycle：`state=input-required` 触发 review dispatch
- a2a-exit：Worker 写 `state=input-required`（不新增参数，仅改值）
- worker agent prompt 模板：指令文本 `PATCH state=input-required`

### 3. 新增 canceled 路径
- manager_01 主动取消：`PATCH state=canceled`
- wt-close --force 时设置 canceled 而非 completed
- canceled 与 failed 区分：canceled=主动取消，failed=崩溃

### 4. 间接影响
- 所有 grep/awk 匹配 `blocked` 的脚本
- 文档中引用 `blocked` 的地方
- agent-table reviewer 配对逻辑中的 state 检查

## 验收
- a2a_tasks 状态完全对齐 Google A2A: submitted/working/input-required/completed/failed/canceled
- 所有 `blocked` 引用已替换
- canceled 路径可用
