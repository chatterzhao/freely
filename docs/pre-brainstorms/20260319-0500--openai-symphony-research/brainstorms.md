# OpenAI Symphony Research

## Trigger

用户要求在独立 worktree 中研究 `openai/symphony` 仓库：

- URL: https://github.com/openai/Symphony
- research_date: 2026-03-19

目标不是评估它“酷不酷”，而是判断它对 Freely 这个“三层循环下自治开发应用”的系统目标是否真的有可复用价值。

## Primary Source Summary

基于仓库首页、`SPEC.md`、`elixir/README.md`、`elixir/AGENTS.md`、`elixir/WORKFLOW.md`，Symphony 当前可以概括为：

1. 一个长期运行的 issue-tracker orchestration service。
   - 持续轮询 Linear。
   - 为每个 issue 创建独立 workspace。
   - 在该 workspace 中启动 Codex app-server session。

2. 它的核心产物不是“文档闭环”，而是“每张工单的隔离执行”。
   - 问题来源以 Linear issue 为主。
   - 运行策略主要来自 repo-owned `WORKFLOW.md`。
   - agent 负责执行、回写 ticket 评论、处理 PR、等待 review、最终 land。

3. 它有较完整的运行器视角。
   - 单一 orchestrator state
   - bounded concurrency
   - retry/backoff/reconciliation
   - per-issue workspace lifecycle hooks
   - optional status surface / dashboard / logs
   - 可扩展到 SSH workers

4. 它明确把自己限制在 scheduler/runner 边界。
   - spec 明说自己是 scheduler / runner / tracker reader。
   - ticket 写入通常由 coding agent 用工具完成，而不是 orchestration core 自己承载全部业务语义。

## What Symphony Is Good At

从 Freely 视角看，Symphony 真正做强的是“自治执行控制面”，尤其是单 issue 执行：

1. 以 issue 为单位做隔离执行。
   - 每个 issue 一个 workspace。
   - continuation retry 在原 workspace 上继续，而不是每轮全新开始。

2. 把运行规则放进 repo-owned workflow contract。
   - `WORKFLOW.md` 同时承载 typed config 和 prompt contract。
   - orchestration service 读它来决定 poll interval、workspace root、hooks、agent limits、sandbox posture。

3. 把 agent 执行纳入显式状态机。
   - `Todo -> In Progress -> Human Review -> Merging -> Done`
   - `Rework` 代表完整重来，不是补丁式返工。

4. 把“单 persistent workpad comment”当作 issue 执行态的事实源。
   - 计划、验收、验证、过程 notes 都写在同一个 comment 里。
   - 这解决了多 comment 漂移问题。

5. 对 app-server orchestration 做了具体规范化。
   - app-server 启动、JSON line protocol、retry、timeout、stderr handling、tool extension、observability 字段都有正式 spec。

## Where Symphony Does Not Match Freely

如果以 Freely 的系统目标来判断，Symphony 不是同一类系统，只覆盖了 Freely 的一部分：

1. 它没有 Freely 的三层循环。
   - Symphony 主要是 `tracker -> issue -> execute -> review/merge`。
   - 它没有显式的 `doc-pre-brainstorm`。
   - 也没有独立的 `doc-ibm` 来做 issue-bound 文档收敛与治理一致性处理。

2. 它假设“issue 已经存在且边界足够清晰”。
   - Freely 的核心之一是从 chat / tests / reviews / runtime exceptions / governance drift 中发现问题，并先收敛成 candidate。
   - Symphony 基本把这个问题前置给 Linear 和人类流程了。

3. 它不把治理文档当成强约束层。
   - Symphony 有 `SPEC.md`、`AGENTS.md`、`WORKFLOW.md`，但没有类似 Freely 的 `CONSTITUTION + LAWS + PROJECT_INTENT` 这套硬分层治理。
   - 它的规则更像“运行约定 + 工程规范”，不是“自治项目 owner 的制度层”。

4. 它的恢复模型比 Freely 窄。
   - Symphony 很强于 issue-run retry / reconciliation / host failover。
   - 但 Freely 关心的是更宽的恢复：会话续接、bridge recovery、phase continuity、跨 loop 状态回流。

5. 它的输入面比 Freely 窄。
   - 主要输入是 tracker issue。
   - Freely 需要处理多来源发现和路由，不允许退化成单一待办系统。

6. 它并不直接面向“自治开发应用”这个产品目标。
   - 它更像针对工程团队的 autonomous work runner。
   - Freely 还要把 runtime / session / governance / recovery 状态暴露给应用内 UI，并以此狗粮开发自己。

## Useful Imports For Freely

尽管不是同一类系统，Symphony 仍有一些可移植的局部思路：

1. `repo-owned workflow contract`
   - 把执行策略和 agent prompt 收敛成一个 repo-owned 合约文件，而不是散在脚本和临时 prompt 里。
   - 对 Freely 有启发，但 Freely 不能把它提升到宪法/法律之上。

2. `single-workpad execution record`
   - 每个 issue 用一个持续更新的 execution artifact，而不是多处碎片化记录。
   - 这个思路可以映射到 Freely 的 progress / recovery / issue continuity 设计。

3. `explicit orchestrator conformance spec`
   - Symphony 的 `SPEC.md` 很像一个可实现、可移植的运行器规范。
   - Freely 可以借鉴这种写法，为自己的 auto-loop / recovery / worktree supervision 写更强的 executable spec。

4. `workspace lifecycle hooks`
   - `after_create / before_run / after_run / before_remove` 这种模型对 Freely 的 worker worktree 生命周期有参考价值。

5. `SSH worker extension`
   - 对 Freely 后续 manager/worker 分布式执行有启发。
   - 但这属于扩展，不是当前自治开发应用的 P0。

## Misfit / Non-Adoption

本轮明确不建议把以下内容直接迁入 Freely：

1. 不把 Linear-first tracker model 当作 Freely 主入口。
2. 不把单一 `WORKFLOW.md` 升格成 Freely 的总治理入口。
3. 不把 Freely 简化成“issue runner + review/merge loop”。
4. 不因为 Symphony 有单 issue 状态机，就回退 Freely 现有的 pre-brainstorm / IBM / dev-loop 分层。
5. 不把“单 persistent comment”机械照搬成 Freely 唯一 continuity 载体；Freely 仍需保留按 loop 分层的文档落点。

## Freely-Centric Verdict

结论：Symphony 对 Freely 是“局部参考物”，不是目标系统模板。

它最有价值的部分，是如何把单 issue 自治执行做成一个可靠运行器：

- 任务隔离
- runtime orchestration
- retry/reconciliation
- workflow contract
- operator observability

但它没有覆盖 Freely 最关键的系统身份：

- 多来源问题发现
- pre-brainstorm 收敛
- issue-bound 文档层
- 恢复治理跨环回流
- 以应用内终端 / UI 为 day-1 主入口的自治开发应用

所以，对 Freely 来说最合理的态度是：

1. 借鉴 Symphony 的“执行器内核”写法。
2. 不放弃 Freely 已经形成的三层循环方法论。
3. 只在明确缺口上吸收它的局部机制，而不是把它当成架构蓝图。

## Recommended Next Route

如果后续要从这次研究 materialize issue，优先级应是：

1. 研究 Freely 是否需要一份更强的 runtime/orchestrator executable spec。
2. 研究 Freely 的 worktree / progress / recovery 是否需要更统一的 issue-level continuity artifact。
3. 将 SSH / remote worker 视为后续扩展，不抢当前自治开发应用主线。

若没有更明确缺口，这个 pre-brainstorm 可以停留在研究结论层，不必强行开大范围迁移 issue。
