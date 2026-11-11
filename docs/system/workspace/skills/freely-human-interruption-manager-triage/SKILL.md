---
name: freely-human-interruption-manager-triage
description: >-
  主管型插话 triage 技能。判断 signal 该由主管直接回答，还是委派到
  `freely-human-interruption-handling` skill 或 worker 处理链。

  Use when: 收到 human interruption signal 需要做首次路由判定。
  触发词："interruption triage"、"插话路由"、"signal routing"。
loop: intake
owner: manager
supersedes: [freely-signal-intent-understanding, freely-chat-issue-routing]
---

# skill:freely-human-interruption-manager-triage

## 职责

- 第一时间接住任意人类插话。
- 把人类插话先视为 advisory signal，而不是自带调度权的命令。
- 以主管职责为边界，判断：
  - 主管是否应先给出必要澄清或监督面回答
  - 还是应委派给后续 worker / runtime 处理链
- 明确这条 signal 应从哪个 restart point 重新开始。
- 产出最小 routing 决策，而不是发明很多问题类型。

## 最小输出契约

- `DECISION=answer|delegate`
- `REACTION=<followup|steer|collect|interrupt|noise>`
- `CLASSIFICATION=<control|discovery|continuation|noise>`
- `RESTART_POINT=<pre_brainstorm|candidate|milestone|ibm|dev|review|verification|continuation|runtime|cleanup>`
- `OWNERSHIP=<manager|worker|runtime>`
- `WHY=<单行原因>`
- `HANDOFF=<若 delegate，则给出单行交接摘要>`
- `ANSWER=<若 answer，则给出单行回答摘要>`

这些字段是 routing 契约，不是问题类型词典。

## 不负责

- 不直接创建 pre-brainstorm / issue
- 不替代主主管做完整排班
- 不发明第二套业务词典
- 不把 runtime 实现细节写成硬编码规则表

## 设计原则

- 少枚举、强边界、重职责。
- 插话者是提供外部 signal 的人，不是项目调度者；主管才是项目主人。
- 先判断这件事是否能由主管职责闭环；若不能，再判断最合适的 restart point。
- 让 AI 做判断，不靠长话术表穷举。
- 示例可以帮助理解边界，但示例不是 if/else 规则。
- 主管只拥有 routing / continuity / 必要澄清职责；凡是需要实际执行的变更动作，都不应把 ownership 留在 manager。
- 只要正确回答依赖 live repo / live runtime / live fleet 的真实检查结果，也应优先委派，而不是让主管给抽象规则答复。
- 默认不要把项目级不确定性反抛给插话者澄清；除非缺失的是高风险外部事实，且现有真源与 analysis 路径都无法恢复。
- 判断插话时，要先看它与当前主线是兼容、纠偏、冲突、阻塞，还是只是建议；不要把用户原话直接当成最终调度方案。

## 示例

- 主管监督面事实查询：
  - 例如“后台 AI 进程现在在做什么”
  - 通常可 `answer`
  - 常见输出是 `CLASSIFICATION=control`、`OWNERSHIP=manager`、`RESTART_POINT=continuation` 或 `runtime`
- 需要实际分析、执行、清理、收口的任务：
  - 例如“检查已经合并到 develop 的 worktree，应该怎么收口”
  - 通常应 `delegate`
  - 常见输出是 `CLASSIFICATION=control`、`OWNERSHIP=worker`、`RESTART_POINT=cleanup`
  - 因为这类事最终需要真实检查和执行 git/worktree 收口，不能只停在主管 continuity

示例只用于说明主管职责边界，不代表固定类型表。


## 合并自（别名兼容期）

以下章节来自已删并的 skill。原目录已移除，但名字作为 alias 保留在 `skill-map.yaml`，由 `bin/skill-route` 解析到本入口；知识以章节形式承接，不随删并丢失。

### 合并自 freely-signal-intent-understanding

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

### 合并自 freely-chat-issue-routing

# freely-chat-issue-routing

将 `freely chat` 消息路由到正确的 issue。

## 职责

只做路由，不做价值判断。判断消息属于哪个已有 issue，还是需要新建 raw issue。

## 输入

- 用户消息文本
- `docs/B1-docs/ISSUES.md` 索引（用于快速匹配 open issue）
- 当前活跃的 issue（phase_state in {in_dev, in_verification}）

## 输出

```json
{
  "action": "new_issue" | "comment",
  "target": "<local_id>" | null,
  "label": "proposed" | "needs_research" | "forward_looking" | "reopen_candidate",
  "urgent": false,
  "reason": "简短说明路由决策理由"
}
```

## 路由规则

### 快速路径（脚本匹配，不调 AI）

1. 消息中包含明确的 issue 引用（`#123`、`raw-20260427T1030Z`、`I-20260426T0000Z-A`）
   → action=comment, target=<引用>

2. 消息长度 < 10 字符，且无实质内容
   → action=new_issue, label=proposed（B1 将判断为 dropped）

### AI 路径（语义匹配）

3. 消息内容与已有 open issue 的 title 语义相关
   → action=comment, target=<匹配的 issue>

4. 消息内容与已关闭 issue 相关
   → action=new_issue, label=reopen_candidate, 消息 body 引用关闭的 issue

5. 消息内容超前/探索性
   → action=new_issue, label=forward_looking

6. 无法判断
   → action=new_issue, label=needs_research

## 紧急判断

如果 target 指向的 issue 正在 dev-loop 中（phase_state in {in_dev, in_verification}），标记 `urgent: true`。

## 执行

路由结果返回后，由 `freely chat` 命令执行实际的写入操作：
- `action=new_issue` → 写入 `.freely/freely.db`（SQLite，不污染 protected branch），后续由 AI 创建工位时 wt-create 自动 materialize 到 `docs/B1-docs/`
- `action=comment` → 写入 `.freely/freely.db`；有对应工位时直接追加到 worktree 的 `docs/B1-docs/{target}/issue.md`

## 边界

- 不读完整的 issue.md 内容（只读 ISSUES.md 索引和 frontmatter 关键字段）
- 不做价值判断（不决定 promote/absorb/drop）
- 不做平台同步（sync 由 issue-sync 脚本异步执行）
