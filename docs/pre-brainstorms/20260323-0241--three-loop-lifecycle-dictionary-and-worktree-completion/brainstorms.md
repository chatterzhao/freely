# 预研：three-loop-lifecycle-dictionary-and-worktree-completion

## Context

- 日期：2026-03-23
- 触发：
  - 本轮在按 Freely 规范推进 `feature/external-codex-account-switch-integration` 时，先停在 verification / merge-ready，而没有一次性走到 `develop` merge 与 cleanup。
  - 用户进一步澄清：真正的问题不是先少了一个 completion 词典，而是 Freely 已经实现了很多能力，但 `three-loop-capability-lifecycle` 没继续把它们吸收进去，已经不再承担“整个应用所有事件、流转与分支的地图”这一职责。
- 当前共识：
  - Freely 是自治系统，不应靠人类每一步追加提醒。
  - 若用户说“按三层 loop 工作”，就应自动覆盖 worktree 生命周期，不存在 loop 之外的例外动作。
  - 三层 loop 是全应用地图，不只是高层原则摘要。
  - 所有事件、流转、终止条件、循环回跳、owner 和 skill/agent 落点，都必须能在三层 loop 里找到具体点位。
  - 在 AI 应用里，`skill` 应按传统软件模块对待，是可维护、可组合、可审计的“代码能力”，而不是零散提示词。

## Core Problem

当前项目里虽然已经有：

- `three-loop-capability-lifecycle`
- `branch-management`
- `worktree-maintenance-governance`
- `multi-worktree-supervision`
- `AGENTS.md` 入口规则

但真正的缺口不是“没几个词”，而是：

1. `three-loop-capability-lifecycle` 还不是 Freely 的全应用地图
- 它定义了很多原则和一部分能力归宿
- 但没有继续吸收后续新增的 skill / agent / runtime / worktree lifecycle 语义
- 因而当人类说“按三层 loop 工作”时，agent 仍然不知道：
  - 从哪里起跳
  - 当前为什么停
  - 下一跳是谁
  - 何时循环回流
  - 到哪里才算 terminal

2. 新能力已经很多，但没有被持续回收进 loop 地图
- 例如：
  - worktree lifecycle
  - promote / cleanup decision
  - checkpoint / hygiene intervention
  - manager restart-point routing
  - interruption / intake / delegation
  - verification 到 promote 的交界
- 这些能力虽然已经存在于 skill / agent / runtime 中，但没有全部在三层 loop 真源里形成统一流转图

3. 结果就是“按三层 loop 工作”无法直接驱动自治
- 因为它还不是完整状态机
- 只是高层框架 + 零散能力 inventory
- 中间很多流程分支、回路、终止条件和 owner handoff 仍靠人脑补

4. worktree 生命周期只是这个更大问题的一个子面
- 它当然必须收进三层 loop
- 但不应把问题缩成“只是定义 worktree completion”
- 根问题是：Freely 还没有一张持续更新的 loop map，去吸纳所有事件、行为、分支和技能落点

表面上 agent 停在：

- `in_verification`
- `merge-ready`
- `merged-not-cleaned`

本质上是因为：

- loop map 没告诉它“当前停点不是 terminal”
- 也没告诉它“下一跳是谁负责”
- 更没告诉它“这类事件属于哪层 loop、走哪条分支、何时回流”

## Proposed Model

### 1. 三层 loop 必须升级为全应用事件地图

所有能力、事件、行为都必须落在三层 loop 中，而且要写到可执行级别，不只是概念级别：

- `auto-loop`
  - 来源扫描
  - event intake
  - worktree/workcell 监督
  - routing
  - restart-point routing
  - promote decision
  - cleanup decision
  - fleet closure
  - runtime continuity / recovery
- `doc-loop`
  - pre-brainstorm
  - candidate
  - milestone intake
  - issue materialization
  - IBM + G
- `dev-loop`
  - implementation
  - tests
  - review
  - verification writeback
  - promotion-ready evidence

对每一类事件，都要能在地图中回答：

- 入口是什么？
- 当前属于哪层 loop？
- owner 是谁？
- 调用哪个 skill / agent？
- 成功后回流到哪一跳？
- 失败 / 阻塞 /分叉 时走哪条逻辑分支？
- terminal state 是什么？

结论：
- 三层 loop 不是摘要，而是 Freely 的总状态机 / 总地图
- worktree lifecycle 不是第四层 loop
- 它只是这张地图里的一个能力面，由 `auto-loop` 编排、`doc-loop` / `dev-loop` 消费

### 2. 统一词典是地图的一部分，不是全部

当前仍然需要统一词典，但它只是为了让地图可执行：

- `active`
  - 当前 worktree 仍在承载生命周期，不可删除
- `merge-ready`
  - feature worktree 内 verification 已完成，但尚未向目标分支 promote
- `merged-not-cleaned`
  - 已并入目标分支，但本地 worktree / branch 还未退役
- `retire-ready`
  - 已满足 cleanup 门槛，可以删除本地 worktree / branch
- `completed`
  - 当前这棵 worktree 的生命周期已经闭环，cleanup 已完成

对应结论：
- “一个 worktree 开发完毕”的默认含义，应该是 `completed`
- 对普通实现型 `feature/*` worktree，默认必须走到删除 worktree / branch，才叫真正完成
- 若因明确原因保留，只能叫 `merged-not-cleaned` 或 `retire-ready`，不能笼统叫“做完”

但更关键的是：

- 这些词必须嵌到 loop map 的节点里
- 不是单独在别处定义完就结束

### 3. “按三层 loop 工作”必须成为统一触发入口

用户只要说：

- `按三层 loop 工作`

就自动等价于：

- 按 Freely 规范
- 按 task lifecycle
- 按 worktree lifecycle
- 直到当前轮应该达到的闭环终点

这不是同义词游戏，而是因为：

- 这些表述本来就都属于同一张 loop map
- 不应再让 agent 维护平行语义

### 4. 每层 loop 必须落成 agent / skill 模块

既然 Freely 是 AI 应用，那么三层 loop 的执行面必须落实到 agent / skill：

- `agent`
  - 决定 route / owner / next hop
- `skill`
  - 作为可维护模块承载具体能力

skill 在这里应视为传统软件的功能模块：

- 是代码能力
- 是模块边界
- 不是可有可无的提示拼接

### 5. 必须补“事件 -> loop 节点 -> owner -> next hop”总表

当前最缺的不是再讲原则，而是建立一张总表，覆盖：

- 所有主要事件
- 所有主要行为
- 所有状态流转
- 所有分支条件
- 所有回流点
- 所有终止条件

例如至少要覆盖：

- human interruption
- standing-source patrol
- event source intake
- pre-brainstorm
- candidate promotion / drop / needs_research
- milestone intake
- issue materialization
- IBM done / blocked
- dev
- verification
- merge
- cleanup
- recovery
- checkpoint / hygiene
- worktree retire / keep
- merged finding -> new worktree

否则三层 loop 还不能真正驱动自治。

### 6. Agent / skill owner 需要显式化

未来要让 Freely 自治不再“人说一步动一步”，至少需要：

- `manager-agent`
  - 负责 loop-level route / next hop / closure 判断
- `branch-management`
  - 承载 workspace / branch lifecycle 执行语义
- `worktree-maintenance-governance`
  - 承载 disposition 判定与 fleet closure
- `three-loop-capability-lifecycle`
  - 承载总地图、总词典和总映射

若这些 owner 不清楚，主管就会在 verification 后停住。

## Likely Landing

这条问题更像一个治理能力缺口，落点应优先在：

1. `docs/system/workspace/three-loop-capability-lifecycle.md`
- 升级为全应用事件地图
- 增加“事件 -> loop 节点 -> owner -> next hop -> terminal state”总表
- 明确 worktree lifecycle、promotion、cleanup、recovery、checkpoint 等都属于三层 loop 组合，而不是例外流程

2. `docs/LAWS.md`
- 定义地图节点使用的状态词典与门槛
- 定义哪些状态允许停，哪些状态必须自动继续

3. `docs/system/workspace/skills/branch-management/**`
- 明确它只是 loop map 中 workspace lifecycle 的执行模块
- 不再把 promote / cleanup 语义游离在总地图之外

4. `docs/system/workspace/skills/worktree-maintenance-governance/**`
- 明确 disposition 词典必须与三层 loop 地图节点一致

5. 项目级 `AGENTS.md`
- 只保留入口提醒：
  - 用户说“按三层 loop / 按 Freely 规范 / 按生命周期”时，直接进入这张地图，而不是再临时解释语义

## Expected Result

这条预研应最终收敛成：

1. 三层 loop 成为真正的总地图
- 所有事件、行为、流转、分支、回流、终止条件都能找到具体点位

2. 统一词典
- 所有涉及“做完 / 收口 / 完成 / retire”的词都成为地图节点的一部分，而不是散落说明

3. 统一触发
- 以后只要说“按三层 loop 工作”，agent 就能知道从哪里起、在哪里循环、为什么不能停、何时才是 terminal
