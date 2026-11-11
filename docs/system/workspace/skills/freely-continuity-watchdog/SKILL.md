---
name: freely-continuity-watchdog
description: >-
  管理 Freely 运行时上下文连续性。覆盖 context warn、context rotate、
  fresh_with_handoff、continuity artifact 选择与旧会话证据引用边界。

  Use when: 上下文超限预警、需要 rotate 或 fresh start、handoff 传递。
  触发词："上下文超了"、"context rotate"、"handoff"、"fresh start"。
loop: runtime
owner: runtime
supersedes: [freely-mem9-continuity-bridge]
---

# skill:freely-continuity-watchdog

> 这是 `skill:freely-watchdog-control-plane` 的 continuity watchdog 子模块。

## 何时使用

- `context_ratio` 接近或达到本地 warn / rotate 阈值
- 出现 `context compacted`、resume 退化、或需要 `fresh_with_handoff`
- 需要判断本轮应先更新哪一种 continuity artifact，而不是继续扩 scope
- 需要区分“watchdog 负责恢复进程”与“AI 负责语义 continuity”这两层 owner

## Trigger Matrix

### 1. Context Warn

条件：
- 当前 AI 仍健康
- 只命中 warn 阈值，尚未进入 rotate / compacted

动作：
- 先更新 phase-appropriate continuity artifact
- 不立即 rotate
- continuity 内容优先写：
  - 当前 issue / pre-brainstorm / IBM / progress / recovery 的最小摘要
  - 当前 branch / worktree / phase_state
  - 下一跳要继续的最小任务边界

### 2. Context Rotate

条件：
- `context compacted`
- `context_ratio >= rotate`
- resume 质量已退化，继续 resume 风险高

动作：
- runtime 触发 `fresh_with_handoff`
- 新会话默认只消费：
  - continuity artifact
  - handoff
  - 必要的旧证据路径引用
- 不把整份旧 `jsonl` / cycle log 当主 prompt 内容

### 3. Deep Recovery

条件：
- 旧会话已退出
- 但 runtime / watchdog 仍能恢复执行链

动作：
- 保留 `session_id` / `jsonl_path` / `cycle_log` / `resume_hint`
- 优先 decide `resume` 还是 `fresh_with_handoff`
- 若证据不足，不盲目 resume

## Artifact Selection

continuity artifact 必须遵循 loop 分层：

- `dev-loop`: `docs/B2-docs/**`
- `doc-loop`: 当前 issue / IBM / pre-brainstorm 产物
- `recovery`: `docs/recovery/**`

研究阶段等价规则：
- 若 `docs/B2-docs/**` / `docs/recovery/**` 尚未启用，允许把 continuity 写入 `docs/B1-docs/CONVERGENCE.md`

## Owner Boundary

- `current AI session`
  - 负责写 continuity artifact
  - 负责给出最小 handoff 语义

- `worktree runtime`
  - 负责触发 `fresh_with_handoff`
  - 负责启动新进程
  - 不负责替 AI 做高质量语义压缩

- `outer watchdog`
  - 负责恢复 manager / account / target lifecycle
  - 不负责 continuity 的语义摘要

## Minimal Handoff

`fresh_with_handoff` 默认应保留：

- `tool_session_id`（若可得）
- `branch`
- `worktree_path`
- `phase_state`
- `runtime_state`
- `resume_hint`
- `cycle_log` / `jsonl_path` 的路径引用
- 当前 continuity artifact 的路径
- 一段最小下一跳说明

## Non-Goals

- 不要求 watchdog 脚本自己生成长摘要
- 不把旧日志整份塞进 prompt
- 不把 account recovery 和 continuity summary 混成一个 owner

## References

- `docs/B2-docs/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- `../freely-recovery-subagent-governance/SKILL.md`
- `../freely-context-source-skill/references/continuation-recovery-routing.md`


## 合并自（别名兼容期）

以下章节来自已删并的 skill。原目录已移除，但名字作为 alias 保留在 `skill-map.yaml`，由 `bin/skill-route` 解析到本入口；知识以章节形式承接，不随删并丢失。

### 合并自 freely-mem9-continuity-bridge

# skill:freely-mem9-continuity-bridge

## 职责

- 评估 mem9 是否适合作为 Freely 的可选 continuity backend。
- 明确哪些内容可以外部化，哪些必须继续保留在本地治理事实源。
- 给出 `local-only` 与 `local + mem9` 两种模式的切换边界。
- 为未来 runtime / doc-loop 集成提供最小、可追溯的接入约束。

## 不负责

- 不把 mem9 提升为 Freely 的正式治理事实源。
- 不替代 `docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/PROJECT_INTENT.md` 或 `docs/B1-docs/`。
- 不直接实现网络调用、鉴权或同步代码。

## 工作流

1. 先读取对应 issue 与 pre-brainstorm，确认这条研究到底是在评估什么边界。
2. 先列出本地权威事实源，再决定哪些 continuity artifact 可以外发。
3. 给出清晰的 `local-only` / `local + mem9` 运行边界。
4. 若后续要进入实现，继续把结果交给 `freely-doc-B2_IBM-execution` 或 `freely-dev-loop-execution`，不要在 skill 内偷跑实现。

## 完成判定

- mem9 的角色被明确限定为可选连续性增强层。
- 本地治理事实源优先级没有被削弱。
- 后续 runtime/bridge 是否接入 mem9 的决策路径已经稳定。
