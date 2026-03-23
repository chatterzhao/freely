# 预研：three-loop-lifecycle-dictionary-and-worktree-completion

## Context

- 日期：2026-03-23
- 触发：
  - 本轮在按 Freely 规范推进 `feature/external-codex-account-switch-integration` 时，先停在 verification / merge-ready，而没有一次性走到 `develop` merge 与 cleanup。
  - 用户明确指出：对 Freely 自举和 Freely 未来开发其他应用来说，“按 Freely 规范”“按 worktree 生命周期”“按任务生命周期”“按三层 loop 工作”都不该产生不同理解。
- 当前共识：
  - Freely 是自治系统，不应靠人类每一步追加提醒。
  - 若用户说“按三层 loop 工作”，就应自动覆盖 worktree 生命周期，不存在 loop 之外的例外动作。
  - 在 AI 应用里，`skill` 应按传统软件模块对待，是可维护、可组合、可审计的“代码能力”，而不是零散提示词。

## Core Problem

当前项目里虽然已经有：

- `three-loop-capability-lifecycle`
- `branch-management`
- `worktree-maintenance-governance`
- `multi-worktree-supervision`
- `AGENTS.md` 入口规则

但还缺少一个统一词典和统一映射表，明确以下问题：

1. 什么叫“一个 worktree 做完了”？
- 是实现完成？
- 是 verification 通过？
- 是 merge-ready？
- 是已经 merge 到目标分支？
- 还是已经 cleanup 并删除 worktree / branch？

2. 什么叫“收口”？
- 是当前 batch writeback 完成？
- 是 worktree retirement？
- 是 issue completed？
- 还是整个 lifecycle closed？

3. worktree 生命周期到底归谁？
- 如果它属于 `auto-loop` 的 supervisor / promotion / cleanup 决策，那么它仍然必须是三层 loop 内的能力，而不是 loop 之外的“运维动作”
- 不能把“治理 worktree”说成一个独立于三层 loop 的第四套流程

4. 哪些表述以后必须视为同义触发词？
- `按 Freely 规范`
- `按 worktree 生命周期`
- `按任务生命周期`
- `按三层 loop 工作`
- `收口`

如果这些词不统一，agent 很容易停在：

- `in_verification`
- `merge-ready`
- `merged-not-cleaned`

却错误地宣称“这轮已经做完”。

## Proposed Model

### 1. 只保留三层 loop，不允许 loop 外语义

所有能力、事件、行为都必须落在三层 loop 中：

- `auto-loop`
  - 来源扫描
  - worktree/workcell 监督
  - routing
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

其中：

- worktree 创建：`auto-loop` 的 workspace preparation
- worktree 内执行 issue：`doc-loop` / `dev-loop`
- worktree promote / merge / cleanup：`auto-loop` 的 supervisor / governance / closure

结论：
- worktree 生命周期不是第四层 loop
- 它是三层 loop 的组合表现，尤其由 `auto-loop` 负责起止与闭环判定

### 2. 定义完成词典

建议统一词典：

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

### 3. 统一触发语义

用户只要说：

- `按三层 loop 工作`

就自动等价于：

- 按 Freely 规范
- 按 task lifecycle
- 按 worktree lifecycle
- 直到当前轮应该达到的闭环终点

除非用户显式说“只做到某一步”，否则 agent 不应停在中间态说明层。

### 4. Agent / skill owner 需要显式化

未来要让 Freely 自治不再“人说一步动一步”，至少需要：

- `manager-agent`
  - 负责判断当前 worktree 是否仍在 `active`
  - 何时从 `merge-ready` 推进到 `merged-not-cleaned`
  - 何时从 `merged-not-cleaned` 推进到 `completed`
- `branch-management`
  - 承载创建、进入、promote、cleanup 的执行语义
- `worktree-maintenance-governance`
  - 承载 disposition 判定与 fleet closure
- `three-loop-capability-lifecycle`
  - 承载统一词典和总映射

若这些 owner 不清楚，主管就会在 verification 后停住。

## Likely Landing

这条问题更像一个治理能力缺口，落点应优先在：

1. `docs/system/workspace/three-loop-capability-lifecycle.md`
- 增加统一词典
- 增加“所有行为都必须落在三层 loop”映射表
- 明确 worktree lifecycle 属于三层 loop 组合，而不是例外流程

2. `docs/LAWS.md`
- 定义 `active / merge-ready / merged-not-cleaned / retire-ready / completed`
- 定义“按三层 loop 工作”默认闭环到何处

3. `docs/system/workspace/skills/branch-management/**`
- 明确对单 feature worktree，若 gate 满足，默认继续到 merge + cleanup
- 不再允许把 promote 当成“下一轮可选动作”

4. `docs/system/workspace/skills/worktree-maintenance-governance/**`
- 明确 disposition 词典必须与三层 loop 词典一致

5. 项目级 `AGENTS.md`
- 只保留入口提醒：
  - 用户说“按三层 loop / 按 Freely 规范 / 按生命周期”时，默认目标是当前轮闭环终点

## Expected Result

这条预研应最终收敛成：

1. 统一词典
- 所有涉及“做完 / 收口 / 完成 / retire”的词都有唯一含义

2. 统一映射
- 所有能力、事件、行为都能落到三层 loop 的具体点位、owner、流程分支

3. 统一触发
- 以后只要说“按三层 loop 工作”，agent 就知道必须一路推进到当前轮闭环终点，而不是停在中间态
