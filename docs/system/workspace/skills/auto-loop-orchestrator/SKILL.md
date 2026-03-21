---
name: auto-loop-orchestrator
description: 编排 A:auto-loop(ADD)，从启动外部 AI CLI 工具到首跳 lead-agent、上下文判定，再接入 pre-brainstorm/doc-loop/dev-loop，并回到发现阶段。当 AI 运行自主持续交付循环时使用。
---

# skill:auto-loop-orchestrator

## 首段闭环主链
`sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> doc-pre-brainstorm-execution | doc-ibm-execution | dev-loop-execution`

约束：
- Freely 当前编排的是外部 AI CLI 工具，而不是自研 AI CLI runtime。
- `lead-agent` 是角色定义，建议落点：`docs/system/workspace/agents/lead-agent.md`。
- `manager-agent` 与 `worker-agent` 是显式角色定义，建议落点：
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
- `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`dev-loop-execution` 是 skills。
- skill 名称表达职责，不用 loop 前缀表达归属。
- `docs/system/workspace/` 是能力真源；`bin/`、`.githooks/` 等是运行时落点。
- `sh` / `ps1` 的定义源应位于 `docs/system/workspace/scripts/`。
- hook 的定义源应位于 `docs/system/workspace/hooks/`，根目录 `.githooks/` 作为安装产物。
- 三层循环下各能力的归宿、owner 边界和生命周期细节以 `docs/system/workspace/three-loop-capability-lifecycle.md` 为准；本 skill 只定义 auto-loop 编排步骤。

## 工作流
1. 先执行固定前置门禁：`skill:constitution-guard` -> `skill:laws-enforcer`。
2. `system/workspace/scripts` 中定义的 `sh` / `ps1` 启动外部 AI CLI 工具，并进入 `lead-agent`。
3. `lead-agent` 调用 `skill:context-source-skill`，基于当前来源、milestone、工具清单与上下文做 usable issue 判定，并组装下一跳提示词。
4. 根据 `context-source-skill` 的结果分流：
   - 无稳定 issue 边界 -> `skill:doc-pre-brainstorm-execution`
   - issue-bound brainstorm / mapping / governance -> `skill:doc-ibm-execution`
   - ready issue / in-progress -> `skill:dev-loop-execution`
5. 各 loop skill 在环内完成自己的工作，并把状态、阻塞、完成或恢复上下文回流给 `auto-loop`；不要求下游 skill 直接“调用 auto-loop 的某个子 skill”。
6. `system/workspace/hooks` 中定义的 hook 规则按安装流程投影到根目录 `.githooks/` 运行时位置。
7. 当状态跨环迁移时，按 `docs/LAWS.md` 第 2C 章同步更新候选项 / milestone / issue / progress / recovery / session evidence。
8. 重复循环直到停止条件。

## 主管模式

当当前会话承担项目级监督职责时：

0. 这是 `auto-loop` 的项目负责人姿态，不是新的并列 loop。
1. 先读取项目级工位视图，而不是直接把自己降级成单工位执行者。
2. 基于 worktree 的 `dirty/checkpoint/runtime/phase/issue` 信息决定：
   - 哪些工位继续 dev-loop
   - 哪些工位只做 doc-loop
   - 哪些工位冻结等待上游
   - 哪些工位进入 review / integration / cleanup
3. 在可并行且写入范围不冲突的任务上，使用 subagent 提高效率。
4. 主管会话自己的职责是排班、监督、合并节奏和恢复决策；不要把这部分完全外包给 subagent。
5. 会话轮换前先写 continuity，至少包含项目级工位快照和下一轮监督优先级。
6. 若主管运行在 `develop` / `main` / `pre-test-merge`，它是只读管理工位；真实 doc-loop / dev-loop 必须在 feature worktree 的 worker 会话中执行。
7. 若控制面出现 `expected running but down` 的工位告警，优先处理 supervision / recovery / freeze 判定，再继续普通路由。
8. 若异常 owner 属于目标工位 `runtime`，主管只输出结构化恢复目标，不自行处理切号、等待或重启。
9. 主管同时处理两类 source：
   - `event source`：interruption / review finding / test failure / runtime anomaly / worker-discovered gap
   - `standing source`：`PROJECT_INTENT` / milestones / issue / progress / recovery / fleet
10. 对 `event source`，主管及时 notice；对 `standing source`，主管周期扫描，并在必要时生成 derived problem signal。
11. 主管被 runtime 重新激活后，不得只确认“进程活着”；必须先做一轮 patrol：
   - `live-status`
   - `fleet-status`
   - milestone / issue / progress / recovery
   - 主动寻找没有 worker 在推进的点位与已完成但未收口的 worktree
12. 主管的核心职责不是“分流插话”，而是对任意 signal 决定 restart point：
   - `pre-brainstorm`
   - `candidate / milestone intake`
   - `IBM`
   - `dev`
   - `review`
   - `verification`
   - `progress / recovery`
   - `runtime supervision / cleanup`
13. 对 `human interruption`，runtime interruption dispatcher 可先做 durable 接住与及时 notice，但不替代主主管完成完整路由。
14. 主管不把 raw signal 直接广播给所有 worker；只把加工后的 handoff 分发给目标 ownership。

## 角色组织

Freely 的角色组织遵循四层：

1. `runtime`
   - 硬编码角色拓扑与分支保护
   - 负责账号切换、等待重检、进程重启等 AI 不可用时的恢复动作
2. `agents`
   - `manager-agent` 负责编排
   - `worker-agent` 负责执行
3. `skills`
   - 提供 doc-loop / dev-loop / supervision / recovery 等可复用动作
4. `hooks`
   - 提供提交、提升、合并前的最后门禁

不要把上述四层全部硬塞到同一个 prompt 或单一 skill 中。

## pre-brainstorms 触发
当任一条件成立时，经 `context-source-skill` 判定后进入 `doc-pre-brainstorm-execution`：
- 问题来源已发现，但 `epic/story/milestone` 尚未收敛。
- 验收边界不清，无法直接进入 `dev-loop`。
- 需要跨工具或子代理进行分歧收敛。

最小产物：
- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- 会话证据（jsonl）在 `candidates.md` 的 `session_refs` 留痕，并在后续 issue / progress / recovery 中继续传播。

## 完成
- 发现、路由和闭环状态保持可追溯。
