# 研究：主管工位、多工位监督与项目级连续性

## Context

- 日期：2026-03-18
- 触发：Freely 已经能托管单工位的 `auto-loop`，但在“Freely 用 Freely 开发自己”的狗粮场景里，还缺一个真正像项目负责人的主管工位。
- 当前暴露问题：
  - `wt-fleet-status` 把所有工位误显示成同一个 issue/phase，主管视图失真。
  - 首跳 prompt 只有当前 worktree 的脏树提醒，没有项目级工位快照。
  - `lead-agent` / `auto-loop-orchestrator` 还没有正式写出主管如何分配 worktree、并行 subagent、控制集成批次。
  - 会话轮换时只有单工位 continuity，没有项目级 continuity。

## 核心判断

这不是一次性的 prompt 调整，而是 Freely 控制面的正式能力：

1. 主管工位必须成为一等运行模型。
2. 多 worktree 监督必须优先读取每个工位自己的 runtime state，而不是读 milestones 的首个 committed issue。
3. 首跳 prompt 必须显式带项目级工位快照，并要求在可并行场景下使用 subagent 提高效率。
4. 当主管会话超过上下文阈值或自然退出时，必须先把项目级连续性写回磁盘，再 `fresh_with_handoff`。

## 最小可行落点

### 1. 项目级工位快照

- `wt-fleet-status` 需要优先读每个工位自己的 `.freely/run/session-state.env`
- 若运行态没有结构化 `issue/phase`，宁可显示 `unavailable`，不要伪造 milestones 第一个 committed issue

### 2. 首跳 prompt 注入主管上下文

- 在 `start-lead-agent.sh` / `runtime/freely` 注入项目级 fleet snapshot
- 同时明确：
  - 当前轮次若承担主管职责，优先排班和监督
  - 在可并行的 doc-loop / verification / review 场景下，使用 subagent 提高效率

### 3. lead-agent / orchestrator 协议

- `lead-agent.md` 需要补主管职责：
  - 哪些工位继续 dev-loop
  - 哪些工位只做 doc-loop
  - 哪些工位冻结等待上游
  - 哪些工作值得委派 subagent
  - 哪些共享热点需要串行
- `auto-loop-orchestrator` 需要补 manager-worker 模式

### 4. 项目级 continuity

- `runtime/freely` 生成 handoff 时，附带项目级 fleet snapshot
- 让新会话看到：
  - 哪些工位在线
  - 哪些工位脏树/checkpoint 压力更高
  - 当前监督应先关注哪里

## 约束

- 主管运行位驻留 `develop`，只读统筹，不修改受版本控制文件
- 实现主管能力的代码和文档改动仍在独立 `feature/*` worktree 中完成
- 仍然遵守 CLI First；主管能力先体现在 CLI / runtime / prompt，不先做 UI
