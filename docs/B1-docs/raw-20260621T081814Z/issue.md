---
local_id: raw-20260621T081814Z14Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T081814Z-A
platform_ids:
  github:
    issue_id: '3209'
    url: https://github.com/chatterzhao/freely/issues/3209
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T08:18:33Z'
updated_at: '2026-06-21T08:58:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

Manager 当前 patrol 缺少两个关键的自主监督能力：

### 缺失 1: 评审闸门（Step 2 改进）

Manager patrol Step 2 消费已完成的 Worker 时，缺少评审环节。Worker 完成产出后，Manager 应评审：
- 产出是否符合 acceptance criteria
- 方向是否正确
- 是否需要修正

结果：
- ✅ 通过 → 推进下一门（PR、merge、close）
- ❌ 不通过 → 介入（session/prompt 或 fork+handoff，与 #3208 共用 dispatch 机制）

### 缺失 2: 主动纠偏（Step 3 改进）

Manager patrol Step 3 当前只设计了卡顿检测（stall timeout → session/prompt 问询），缺少主动纠偏：
- Manager 巡检时发现 worker 产出方向偏离预期 → 主动插话纠正
- 不等 worker 完成才评审，中途就可以调整方向

## 设计

两处改进共用同一套介入 dispatch（与人类 chat 的 steer 通路一致）：

```
Manager patrol:
  Step 2: 消费完成 worker
    → 读产出 → 评审
    → accept → 推进下一门
    → revise → dispatch_intervention(task_id, "请修改 X...")
  
  Step 3: 巡检工作中的 worker
    → stall? → dispatch_intervention(task_id, "Status check")
    → off-track? → dispatch_intervention(task_id, "方向调整: ...")
    → 正常 → 跳过
```

dispatch_intervention 内部分发逻辑：
- worker session alive → session/prompt (a2a_task.py prompt)
- worker session dead → fork+handoff (重建 worker 带上下文)

## 与 #3208 的关系

- #3208 解决人类→Manager→worker 的通路（intake 迁移 + steer dispatch）
- 本 issue 解决 Manager→worker 的自主监督通路（review gate + proactive steer）
- 两者底层共用同一套 dispatch_intervention 机制
- 建议先做 #3208（打通 dispatch 通道），再做本 issue（增加 patrol 中的调用点）
