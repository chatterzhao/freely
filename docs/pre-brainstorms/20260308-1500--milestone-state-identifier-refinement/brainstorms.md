# 研究：里程碑状态标识符语义收敛

日期：2026-03-08 15:00 UTC

## Context

用户反馈：`milestone_state=in_progress` 配合 `loop_stage` 的设计不够直观。

问题来源：
- 用户认为 `in_progress` 太泛化，建议改为 `in_ibm_progress` 这样的阶段感知标识
- 当前需要同时看两个字段才能理解 issue 状态

## 当前设计

### 现有标识体系

| 标识 | 值域 | 层次 | 用途 |
|------|------|------|------|
| `source_class` | `discovery \| milestone \| continuation` | 来源层 | 判断输入来源类型 |
| `route_kind` | `pre_brainstorm \| ibm \| dev_loop \| completion_verification \| recovery` | 路由层 | 决定下一跳 skill |
| `loop_stage` | `pre_brainstorm \| ibm \| ready_for_dev \| dev_in_progress \| blocked \| completed` | 执行层 | 标识执行阶段 |
| `milestone_state` | `committed \| in_progress \| completed` | Milestone 层 | 标识归属状态 |

### 当前用法示例

```yaml
# IBM 阶段的 issue
milestone_state: in_progress
loop_stage: ibm

# dev-loop 阶段的 issue
milestone_state: in_progress
loop_stage: dev_in_progress
```

### 当前设计的逻辑

LAWS 2C 第 3 条明确定义：
> `milestone_state=in_progress` 不是 progress 的同义词；只有 `loop_stage=dev_in_progress` 时才要求匹配 `progress` 证据。

## 问题分析

### P1: 语义重叠

`milestone_state` 和 `loop_stage` 存在部分语义重叠：
- `milestone_state=completed` vs `loop_stage=completed`
- `milestone_state=in_progress` 需要配合 `loop_stage` 才能理解具体阶段

### P2: 认知负担

判断 issue 状态需要同时读取两个字段，增加 AI 和人类的认知负担。

### P3: 命名不够自解释

`in_progress` 不能一眼看出是 IBM 进度还是 dev 进度。

## 候选方案

### 方案 A: 保持正交，改进命名

保持两层正交设计，但改进命名使其更自解释：

**改进后的标识**：

| 原标识 | 改进后 | 说明 |
|--------|--------|------|
| `milestone_state=in_progress` | `milestone_state=active` | "活跃"而非"进行中" |
| `milestone_state=completed` | `milestone_state=delivered` | "已交付"而非"已完成" |

**示例**：
```yaml
milestone_state: active      # milestone 归属层面：活跃
loop_stage: ibm              # 执行层面：IBM 阶段
```

**优点**：
- 保持正交设计的清晰边界
- 减少与 `loop_stage=completed` 的命名冲突
- 语义更明确：`active` 只表示"属于活跃队列"

**缺点**：
- 仍需看两个字段

### 方案 B: 阶段感知标识（用户建议）

将阶段信息融入 `milestone_state`：

```yaml
# IBM 阶段
milestone_state: in_ibm

# dev-loop 阶段
milestone_state: in_dev

# blocked
milestone_state: blocked
```

**优点**：
- 一眼能看出阶段
- 字段更少

**缺点**：
- 组合爆炸：如何处理 `in_ibm` + `blocked`？需要 `blocked_in_ibm`？
- 失去正交性：无法独立表示"milestone 归属"和"执行阶段"
- 与 `loop_stage` 语义重叠

### 方案 C: 合并为单一标识

只保留 `loop_stage`，去掉 `milestone_state`：

```yaml
loop_stage: ibm              # 替代 milestone_state=in_progress + loop_stage=ibm
loop_stage: dev_in_progress  # 替代 milestone_state=in_progress + loop_stage=dev_in_progress
loop_stage: completed        # 替代 milestone_state=completed
```

**优点**：
- 最简单，只有一字段

**缺点**：
- 失去 milestone 归属语义
- `committed` 状态（已接纳但未开始）无法表达
- 无法区分"从未进入 milestone"和"已完成"

### 方案 D: 重新定义职责边界

重新思考两个标识的职责：

**`milestone_state`**：只管"在哪个队列"
- `candidate` - 在候选队列
- `committed` - 在已提交队列（已接纳）
- `active` - 在活跃队列（正在处理）
- `delivered` - 在已交付队列

**`loop_stage`**：只管"执行到哪一步"
- `pre_brainstorm` - 前置研究
- `ibm` - 文档收敛
- `ready_for_dev` - 开发就绪
- `dev_in_progress` - 开发中
- `blocked` - 阻塞
- `completed` - 完成

**关键改变**：`milestone_state` 不再用 `in_progress`，改为 `active`。

**示例**：
```yaml
# 刚被 milestone 接纳，尚未开始
milestone_state: committed
loop_stage: pre_brainstorm

# 正在 IBM 阶段
milestone_state: active
loop_stage: ibm

# 开发中
milestone_state: active
loop_stage: dev_in_progress

# 已完成
milestone_state: delivered
loop_stage: completed
```

## 初步倾向

**方案 D** 最为合理：

1. **保持正交**：两个标识各司其职，不混淆
2. **命名自解释**：`active` 比 `in_progress` 更准确表达"活跃队列"语义
3. **避免重叠**：`delivered` vs `completed` 不再冲突
4. **可扩展**：未来增加新队列（如 `suspended`）不影响 `loop_stage`

## 待确认问题

1. `committed` 是否需要独立状态？还是直接从 `candidate` 跳到 `active`？
2. `blocked` 应该在 `milestone_state` 还是 `loop_stage` 表达？
3. 是否需要 `suspended`（暂停）状态？

## 下一步

- 本研究不再单独进入 milestone 或 issue materialization。
- 其核心问题已被后续 `20260308-1630--stage-prefixed-progress-identifier` 吸收，并升级为 `phase_state=<prefix>_<stage>` 的正式方案。
- 若需追溯本轮探索，只作为“为何不采用 `active/delivered` 改名方案”的背景材料使用。
