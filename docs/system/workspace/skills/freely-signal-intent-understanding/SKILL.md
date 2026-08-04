---
name: freely-signal-intent-understanding
description: >-
  在 manager routing 之前收敛 signal 的最小意图结构：要推进什么、
  是否需要 live inspection、是否需要 analysis/execution。

  Use when: 主管面对 interruption、review、test、runtime anomaly 或
  standing-source derived signal 需要先理解意图再路由。
  触发词："signal intent"、"意图理解"、"triage"、"这条消息想干什么"。
---

# skill:freely-signal-intent-understanding

## 目标

这不是一个“问题类型大全”，也不是替主管做最终调度。

它只回答一件事：

> 这条 signal 真实想推进什么，下一步应该先澄清、先分析，还是可以直接进入执行。

补充：
- 若 signal 来自人类插话，默认把它当成 advisory signal。
- 这一步要帮助主管识别“插话者想推动什么”，而不是默认承认“插话者已经替项目做完调度判断”。

## 输入

- signal source record
  - 例如 `docs/B1-docs/raw-*/`
  - review finding
  - test / verification evidence
  - runtime / recovery continuity
  - standing-source scan result
- 当前项目上下文
  - 当前活跃 milestone / issue / progress / recovery
  - relevant pre-brainstorm lifecycle state
  - 当前 fleet / runtime / worktree 状态
  - `PROJECT_INTENT`

## 输出

输出保持最小，不扩成大词典。至少应收敛出：

- `intent_kind`
  - 例如：`clarify` / `audit` / `propose` / `fix` / `continue` / `recover`
- `needs_live_inspection`
  - `true` / `false`
- `needs_execution`
  - `true` / `false`
- `scope`
  - 例如：`manager-only` / `current-issue` / `fleet` / `runtime` / `project`
- `complexity`
  - `direct` / `multi-step`
- `current_context`
  - 这条 signal 与当前项目主线、当前 issue、当前 runtime 的关系摘要
- `source_effect`
  - 例如：`compatible` / `corrective` / `blocking` / `conflicting` / `advisory`

这些字段是帮助主管继续判断，不是为了替代主管。

## 主管如何使用

主管读取这层结果后，再做后续 routing：

- 自己直接澄清/回答
- 委派 `analysis worker`
- 委派 `execution worker`
- 先 `analysis` 再 `execution`
- 决定 restart point 与 canonical absorption target
- 决定是否需要 queue / freeze / supersede 当前 lane

## 三个 loop 下的职责边界

### manager

- notice / claim
- 调用或吸收本 skill 的结果
- 决定 `answer / analyze / execute / analyze_then_execute`
- 决定 restart point
- 监督 completion 与 writeback

### analysis worker

- 读取 live context
- 还原问题结构
- 输出 action-oriented handoff
- 不直接把复杂问题压成单步执行

### execution worker

- 执行明确动作
- 例如：doc update / review / test / commit / merge / cleanup / recovery

## 示例

示例只用于帮助理解职责，不是 runtime 规则表。

### 示例 1：监督面澄清

signal:

> 看看后台 AI 进程都在做什么？

可能的 intent understanding：

- `intent_kind=clarify`
- `needs_live_inspection=true`
- `needs_execution=false`
- `scope=runtime`
- `complexity=direct`

后续通常由主管自己回答即可。

### 示例 2：fleet 审计

signal:

> 检查脏的位置，仔细思考他们是否过时，还是有用但是没提交没合并

可能的 intent understanding：

- `intent_kind=audit`
- `needs_live_inspection=true`
- `needs_execution=true`
- `scope=fleet`
- `complexity=multi-step`
- `source_effect=corrective`

后续通常不是主管直接给抽象说明，而是先委派 analysis worker，再决定 review / commit / merge / cleanup。

## 不要做什么

- 不要把未来场景全部提前枚举成类型表
- 不要替主管直接拍板最终 restart point
- 不要把 execution worker 变成“先分析再决定”的混合角色
- 不要把这层做成另一套与三个 loop 脱节的新系统
- 不要把“来自用户”误翻译成“具有调度权”

## 完成标志

- 新 signal 已得到最小意图结构化理解
- 主管可以基于此继续 routing，而不是从 raw signal 直接跳到执行桶
