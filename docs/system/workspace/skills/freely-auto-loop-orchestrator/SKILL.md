---
name: freely-auto-loop-orchestrator
description: >- 编排 AI 自主持续交付循环。从启动外部 AI CLI 工具到首跳 lead-agent、
  上下文判定、进入 doc-loop/dev-loop，再回到发现阶段。

  Use when: AI 运行自主持续交付循环，或需要编排多 agent 协作。
  触发词："auto-loop"、"自主循环"、"持续交付"、"编排 agent"。
---

# skill:freely-auto-loop-orchestrator

## 首段闭环主链
`sh/ps1 -> external AI CLI tool -> lead-agent -> freely-context-source-skill -> freely-doc-B1_IBM-execution | freely-doc-B2_IBM-execution | freely-dev-loop-execution | manager-owned verification / cleanup route`

约束：
- Freely 当前编排的是外部 AI CLI 工具，而不是自研 AI CLI runtime。
- `lead-agent` 是角色定义，建议落点：`docs/system/workspace/agents/lead-agent.md`。
- `manager-agent` 与 `worker-agent` 是显式角色定义，建议落点：
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/agents/worker-agent.md`
- `freely-context-source-skill`、`freely-doc-B1_IBM-execution`、`freely-doc-B2_IBM-execution`、`freely-dev-loop-execution` 是 skills。
- skill 名称表达职责，不用 loop 前缀表达归属。
- `docs/system/workspace/` 是能力真源；`bin/`、`.githooks/` 等是运行时落点。
- `sh` / `ps1` 的定义源应位于 `docs/system/workspace/scripts/`。
- hook 的定义源应位于 `docs/system/workspace/hooks/`，根目录 `.githooks/` 作为安装产物。
- 三个 loop 下各能力的归宿、owner 边界和生命周期细节以 `docs/system/workspace/three-loop-capability-lifecycle.md` 为准；本 skill 只定义 auto-loop 编排步骤。
- `docs/system/workspace/three-loop-capability-lifecycle.md` 同时是 whole-app lifecycle / logic 的唯一细节真源；本 skill 不平行维护 three-loop 的细节地图、route map 或 terminal semantics。
- 若本 skill 的 routing、restart point、completion / verification / cleanup / recovery judgement 语义变化，必须先同步检查该真源，再更新本 skill。

## 工作流
1. 先执行固定前置门禁：`skill:freely-constitution-guard` -> `skill:freely-laws-enforcer`。
2. `system/workspace/scripts` 中定义的 `sh` / `ps1` 启动外部 AI CLI 工具，并进入 `lead-agent`。
3. manager / patrol 轮次先把 standing/event source 扫描成 machine-readable `manager-task-source-scan-latest.json`，作为本轮路由的结构化输入。
4. `lead-agent` 调用 `skill:freely-context-source-skill`，基于当前来源、scan json、milestone、工具清单与上下文做 usable issue 判定，并组装下一跳提示词。
5. 根据 `freely-context-source-skill` 的结果分流：
   - 无稳定 issue 边界 -> `skill:freely-doc-B1_IBM-execution`
   - issue-bound brainstorm / mapping / governance -> `skill:freely-doc-B2_IBM-execution`
   - ready issue / in-progress -> `skill:freely-dev-loop-execution`
   - `completion_verification` / `cleanup_governance` -> 留在 `auto-loop` 侧做 manager-owned judgement / handoff，必要时委派 worker 或 `skill:freely-worktree-maintenance-governance`
6. 各 loop skill 在环内完成自己的工作，并把状态、阻塞、完成或恢复上下文回流给 `auto-loop`；不要求下游 skill 直接“调用 auto-loop 的某个子 skill”。
7. `system/workspace/hooks` 中定义的 hook 规则按安装流程投影到根目录 `.githooks/` 运行时位置。
8. 当状态跨环迁移时，按 `docs/LAWS.md` 第 2C 章同步更新候选项 / milestone / issue / progress / recovery / session evidence。
9. scan json 是 idle/replan step，而不是 every-cycle step：至少在首次启动缺少 scan、manager idle 且有新 intake、或 manager continuity 在无 active worker 的情况下前进后重生成；若 active worker 正在稳定推进，不要为 broad patrol 每轮重扫。

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
6. 若主管运行在 `develop` / `main` / `test-pre-merge-*`，它是只读管理工位；真实 doc-loop / dev-loop 必须在 feature worktree 的 worker 会话中执行。
7. 若控制面出现 `expected running but down` 的工位告警，优先处理 supervision / recovery / freeze 判定，再继续普通路由。
8. 若异常 owner 属于目标工位 `runtime`，主管只输出结构化恢复目标，不自行处理切号、等待或重启。
9. 主管同时处理两类 source：
   - `event source`：interruption / review finding / test failure / runtime anomaly / worker-discovered gap
  - `standing source`：external issue / milestones / issue / progress / recovery / interruption backlog / pre-brainstorm lifecycle / fleet
10. 对 `event source`，主管及时 notice；对 `standing source`，主管周期扫描，并在必要时生成 derived problem signal。
   - 推荐统一脚本入口：`freely task-source-scan --project <project> --json`
   - 该 JSON 是 standing-source inventory，不替代 canonical issue / progress / milestone / source closeout 真相
11. 因此 `auto-loop` 对主管而言至少有两类入口：
   - `event-driven`
   - `patrol-driven`
   两者都要回到统一的 manager restart-point routing，而不是形成两套并列流程。
12. 主管被 runtime 重新激活后，不得只确认“进程活着”；必须先做一轮 patrol：
   - `live-status`
   - `fleet-status`
  - external issue / milestone / issue / progress / recovery
   - 主动寻找没有 worker 在推进的点位与已完成但未收口的 worktree
13. 主管的核心职责不是“分流插话”，而是对任意 signal 决定 restart point：
   - `pre-brainstorm`
   - `candidate / milestone intake`
   - `IBM`
   - `dev`
   - `review`
   - `verification`
   - `progress / recovery`
   - `runtime supervision / cleanup`
14. verification / writeback / cleanup 不是第四层 loop；它们要么属于 worker 在 `doc-loop` / `dev-loop` 中产出的证据，要么属于主管在 `auto-loop` 中做出的治理判断与收口委派。
15. worker 在 `doc-loop` / `dev-loop` 中只能把事项推进到“到达下一门”的状态：
   - 文档边界已收敛
   - 实现与局部测试已完成
   - verification evidence 已写回
   但“是否完成、是否通过验证、是否进入 cleanup / retirement”必须由 `auto-loop` 基于 canonical evidence 裁决。
16. 若 runtime watchdog 发现短时间内反复启动 AI 工具进程、异常重启次数、或短窗口进程总数异常增长，这不是 worker 自行回流；主管必须把它视为 `event-driven` dead-loop suspicion signal，先判断是正常恢复、prompt/continuity 漂移，还是需要 freeze / kill / restart / reroute。
17. 对 `human interruption`，runtime interruption dispatcher 可先做 durable 接住与及时 notice，但不替代主主管完成完整路由。
18. 人类插话默认是 advisory signal：
  - 不自带调度权
  - 不默认打断当前 lane
  - 主管先判断它与当前主线是兼容、纠偏、阻塞、冲突，还是只是建议
  - 再决定 direct answer、queue、freeze、analysis delegation 或 execution delegation
19. 主管不把 raw signal 直接广播给所有 worker；只把加工后的 handoff 分发给目标 ownership。
20. 当 standing source 的重点问题是 sequencing / queue drift / state maintenance，而不是业务边界本身时，主管应优先委派 `skill:freely-milestone-planning-state-maintenance`，而不是让业务 worker 顺手补 milestone。
21. 对 worker 工位的 `human interruption`：
  - `freely chat` 先完成 durable intake 与 interruption classification
  - 若结果已收敛成当前工位的 worker-owned `continuation` / `verification` handoff，且当前 worker runtime 因 `operator_stop` 停止
  - runtime 应重激活该 worker 主循环，而不是让 delegated intake 悬空
22. 对 manager continuation handoff：
  - interruption resolution 生成 `handoff://continuation` 只是第一步
  - runtime 还必须留下 generated-vs-consumed evidence
  - 若后续命中 `fresh_with_handoff`、`auth_failure` 或其他 failure boundary，不能把 handoff 是否已消费变成不可见状态
23. `freely` 是唯一正式 front-door command：
  - `chat` 是 canonical high-level submit primitive
  - `tui` 只是交互壳，必须复用同一 post-submit runtime chain
  - 未来 GUI 也应复用同一 backend contract，而不是另造提交语义
24. 当项目级 patrol 已经把某条线稳定判成 `retire-only`、`retire-now` 或 `continue-dev` 时，主管下一步必须进入 concrete execution routing：
  - `retire-only / retire-now` -> cleanup / retirement worker
  - `continue-dev` -> verification / dev continuation worker
  - 只有在关键事实缺失、上游依赖不明或 blocker 未冻结时，才允许继续 manager-only patrol
25. standing-source completeness 至少覆盖 interruption、external issue、milestone、progress 与 pre-brainstorm：
  - external issue 要区分 raw source intake 与已消费后的 external drift / closeout drift，不得把所有 open issue 都当 fresh intake
  - interruption 要检查是否已分类、吸收、写回
  - progress 要优先读取，确认是否已有主动记录
  - pre-brainstorm 要检查 candidate / milestone 同步、`next_action` 与 `revisit_trigger`
  - 发现 drift 时默认补账、核实、重排与委派，而不是把项目级不确定性默认退回给人类插话者
  - `task-source-scan` 更适合在 startup patrol、closeout 后 truth 发生变化、或 worker capacity 有空位时运行；不要在所有 worker lane 都忙且没有新 truth 时机械重扫
26. 当主管已经生成更新的一轮 manager continuity 和 worker prompt set 时，runtime 必须以后者为最新 truth：
  - latest continuity generated
  - latest prompt set generated
  - latest continuity / prompt set consumed
  主管 watchdog 不得仅因为 supervisor 已在运行就停留在旧 continuity；要持续把最新一轮监督结果推进成 worker launch / reentry。
27. manager handoff 中的每个 worker prompt 都必须同时满足两层契约：
  - continuity 中显式引用 worker prompt 绝对路径
  - worker prompt 本体携带 machine-readable `Worktree:` / `Branch:` header
  否则 manager 虽然完成了排班判断，runtime 仍可能无法把 handoff 推进成真实 worker launch。

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
当任一条件成立时，经 `freely-context-source-skill` 判定后进入 `freely-doc-B1_IBM-execution`：
- 问题来源已发现，但 `epic/story/milestone` 尚未收敛。
- 验收边界不清，无法直接进入 `dev-loop`。
- 需要跨工具或子代理进行分歧收敛。

最小产物：
- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- 会话证据（jsonl）在 `candidates.md` 的 `session_refs` 留痕，并在后续 issue / progress / recovery 中继续传播。

## 完成
- 发现、路由和闭环状态保持可追溯。
