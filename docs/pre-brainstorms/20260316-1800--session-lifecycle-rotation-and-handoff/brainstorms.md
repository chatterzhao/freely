# 研究：Freely 会话生命周期轮换与交接

## Context

- 日期：2026-03-16 18:00 America/Los_Angeles
- 触发：当前 Freely supervisor 在 `codex exec resume --last` 路径上能持续把子进程拉起来，但在长期狗粮运行里暴露出两个缺口：
  1. 当 Codex 已经发生 `context compacted`，Freely 仍会盲目继续 `resume`
  2. Freely 还没有显式策略决定什么时候应该继续原会话、什么时候应该切 fresh session、什么时候应该附带交接摘要
- 现象证据：同一 worktree 的 `loop.log` 出现密集 `resume` 批次；cycle log 中能看到 `context compacted` 后又重复首跳路由输出，说明“会话仍可 resume”不等于“继续 resume 仍是最优决策”。
- 相关历史输入：
  - `docs/pre-brainstorms/20260303-0000--cli-orchestration-architecture/candidates.md` 已有 `C-20260303-103 会话管理机制（恢复/压缩/新会话）`
  - `docs/LAWS.md` 已明确恢复优先与 `resume_hint` 语义，但还没有把“何时停止 resume、改走 fresh_with_handoff”写成具体运行策略

## 现状观察

1. 当前 runtime 的 launch 策略过于粗糙
- `runtime/freely` 只有：
  - 第一轮 `fresh`
  - 之后一律 `resume`
- 它没有结合：
  - 最近一次 cycle 的退出内容
  - context compaction 信号
  - 连续 resume 次数
  - 会话轮换后的交接文件

2. Freely 已有恢复治理，但没有运行时轮换治理
- 恢复治理已经说明：
  - 可 resume 时优先 resume
  - 不可 resume 时再 restart
- 但这里还缺一层：
  - 可 resume 但已不值得继续 resume 时怎么办

3. Fresh session 不能是“丢上下文重开”
- 如果决定 fresh，就必须给新会话一个可追溯交接：
  - 上一轮 session id（如果可得）
  - 上一轮 cycle log
  - worktree / branch
  - 触发 fresh 的原因
  - 最近一段输出摘录

## 方案比较

### 1. 永远 resume

优点：
- 实现最简单

缺点：
- 会在 context compacted 后继续沿用退化会话
- 容易让首跳重复、会话价值持续下降

结论：
- 不能继续作为唯一策略

### 2. 每轮都 fresh

优点：
- 避免长会话退化

缺点：
- 丢失连续性
- 会让同一 issue 的推进不断回到首跳理解

结论：
- 也不合适

### 3. Resume 优先，但加 session rotation + handoff

规则方向：
- 默认继续 `resume`
- 当出现 context compaction 或达到轮换阈值时，改为 `fresh`
- 进入 fresh 前，写一个 handoff 文件，让新会话先吸收上一轮上下文摘要

优点：
- 保留恢复优先原则
- 同时避免盲目沉没在退化长会话中
- 和 Freely 的 recovery / evidence / worktree 治理兼容

缺点：
- 需要 supervisor 增加状态文件和交接 prompt

结论：
- 作为当前最小可行实现

## 收敛结论

1. Freely 需要把“会话可续接”与“会话仍值得续接”区分开。
2. 当前最小实现面应采用：
- `resume` 优先
- `context compacted => fresh_with_handoff`
- `连续 resume 次数达到阈值 => fresh_with_handoff`
3. handoff 的最小字段应包括：
- `rotation_reason`
- `previous_launch_kind`
- `previous_tool_session_id`（如有）
- `previous_cycle_log`
- `branch`
- `worktree_path`
- 最近输出摘录
4. `codex` 的默认运行配置继续固定为 `gpt-5.4 + medium`，避免会话轮换逻辑再次依赖用户全局配置。
