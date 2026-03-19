# OpenAI Harness Engineering Research

## Trigger

用户要求在专用 worktree 中研究 OpenAI 文章《工程技术：在智能体优先的世界中利用 Codex》：

- URL: https://openai.com/zh-Hans-CN/index/harness-engineering/
- publish_date: 2026-02-11
- research_date: 2026-03-19

目标不是复述宣传语，而是抽取对 Freely 作为自主循环运行器最有用的工程结论。

## Observations

1. OpenAI 把“人写代码”替换成“人设计 harness，agent 执行代码”。
   - 人类主要负责定义目标、约束、反馈回路与环境。
   - 当 agent 失败时，首选修复环境、工具和文档，而不是人工下场写补丁。

2. 代码仓库被当成 agent 的 record system，而不是仅当源代码容器。
   - `AGENTS.md` 应该是目录，不应膨胀成百科全书。
   - 深层知识要进入可版本化、可交叉链接、可 lint 的 `docs/`。
   - 对 agent 不可见的知识等于不存在；Slack、口头约定、外部文档都需要入仓。

3. Agent-first 可读性比人类风格一致性更优先。
   - 代码、文档、schema、计划、评审历史都应对 agent 可导航。
   - 他们更偏好可预测、稳定、可组合、训练集中常见的“boring tech”。
   - 宁可重做小型透明能力，也不要依赖难以建模的黑箱行为。

4. 约束要编码成可执行不变量，而不是长篇 prompt。
   - 架构边界、依赖方向、命名约定、日志格式、文件大小、可靠性要求，都由 lint 和结构测试强制执行。
   - 规则错误信息本身也面向 agent 设计，直接给出修复线索。

5. 反馈回路必须 machine-readable。
   - 每次变更都跑独立 worktree 实例。
   - UI 通过 Chrome DevTools 协议可读、可控、可验证。
   - 日志、指标、trace 对 agent 可查询，形成本地临时 observability stack。
   - 这样 prompt 才能从“试试修一下”升级成“服务启动必须 <800ms”这类可验证约束。

6. 高吞吐量下，合并哲学会变化。
   - PR 周期极短，等待成本高于纠错成本。
   - 间歇性测试失败更适合自动重跑，而不是长期阻塞。
   - 这成立的前提不是“放松纪律”，而是前面已经把反馈回路和不变量做强。

7. 完全 agent 生成会产生熵，需要持续垃圾回收。
   - 漂移不会自己消失。
   - 需要把“黄金原则”编码进仓库，再用后台 agent 持续扫描、重构、清债。
   - 文档园艺与代码园艺都应制度化。

## Freely Implications

1. Freely 当前治理已经接近其“AGENTS.md 只做入口，真实知识进入 docs”方向，这条应继续强化，而不是回退到单大文件提示词。

2. Freely 的 worktree-first 纪律与文中“每次改动都在独立实例里运行并验证”高度一致，但目前还可以继续补强：
   - 将 UI/CLI/runtime 验证结果更系统地暴露给 agent。
   - 让每个 worktree 的状态、日志、trace、dirty budget 更容易被自动监督消费。

3. Freely 的核心机会不只是“让 agent 写代码”，而是补齐 harness engineering：
   - record system
   - machine-readable feedback loops
   - executable invariants
   - continuous cleanup

4. Freely 当前最值得对齐的不是 OpenAI 的吞吐量结论本身，而是其前提条件。
   - 如果没有严格边界、可执行 lint、可观察性和自修复回路，贸然提高自主度只会放大混乱。

## Fit Assessment Against Freely Goal

Freely 的目标不是“高吞吐生成代码”本身，而是“AI 在三层循环下持续自治开发应用”。按这个目标回看，OpenAI 这篇文章的可用性需要降噪处理：

### 直接同构、但不是新增信息

这些点与 Freely 现有设计高度一致，因此更多是外部印证，不应当作新的顶层方法论输入：

1. 三层循环中的外循环编排与路由。
   - `docs/PROJECT_INTENT.md` 已明确 `auto-loop -> context-source-skill -> pre/doc/dev-loop`。
   - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md` 已把这条主链写成正式能力。

2. 仓库作为 record system。
   - `AGENTS.md` 已被限定为入口文件。
   - 活跃知识源已明确收敛到 `CONSTITUTION / LAWS / PROJECT_INTENT / pre-brainstorms`。

3. worktree-first 执行纪律。
   - 宪法和法律已经把 feature worktree、主管/worker 分工、主工位只读等约束写死。

4. 将自治开发拆为文档收敛与实现执行，而不是直接把 chat 变成代码。
   - Freely 比文章更显式，已经把 pre-brainstorm、IBM、dev-loop 分层。

### 有增量价值的部分

真正有增量价值的，不是他们“也在做自治开发”，而是他们把自治开发的支撑层做得比理念更彻底：

1. 把反馈回路产品化、可查询化。
   - UI、日志、指标、trace 都直接对 agent 可读。
   - Freely 已开始做 runtime/status/checkpoint/fleet-status，但距离“完整 machine-readable harness”还有差距。

2. 把不变量编码成自动 enforcement。
   - Freely 已有宪法/法律/skills/hook，但仍有一部分规则停留在文档规范与 prompt 注入，而不是统一 CLI / lint / structure-test enforcement。

3. 把“AI 残渣清理”变成持续后台机制。
   - Freely 目前已有治理漂移意识，也有 pre-brainstorm reroute。
   - 但还没形成稳定的 doc-gardening / cleanup loop 作为控制面常驻能力。

### 对 Freely 当前阶段不应误用的部分

1. 不应过早追求他们的吞吐量/PR 节奏。
   - 他们强调的是等待成本高于纠错成本，但这是建立在超强反馈基础设施之上。
   - Freely 当前阶段更接近“建立自治开发控制面”，不是“把 merge 门尽量放松”。

2. 不应把“全 agent 生成代码”当作我们的近期验收标准。
   - Freely 当前要证明的是应用开发闭环能自治运行，而不是证明人类永不写代码。
   - 对 Freely 来说，先把自治 loop 稳定跑通，比追求纯度更重要。

3. 不应把 OpenAI 的 product team workflow 直接映射成 Freely 的 runtime 设计。
   - 他们描述的是一个已经有成熟内部基础设施的应用团队。
   - Freely 现在做的是“让任意项目也能具备这种自治开发能力”的通用运行器，因此控制面、恢复治理、worktree 生命周期会比他们更核心。

## Current Verdict

结论：这篇研究不是 Freely 的新北极星，也不是必须 materialize 的高优先方案包。

- 可保留：
  - “harness engineering”这个视角，用来检查 Freely 当前三层循环是否有足够的执行基座。
  - 将 feedback loops / enforcement / cleanup 视为自治开发的必要支撑层。
- 不应高估：
  - 吞吐量叙事
  - 全 agent 编码纯度
  - 直接照搬其团队工作流

因此，这次研究更适合作为一个“校准镜子”，不是新的路线替换。若后续没有发现明确缺口，就不应为了“研究出东西”而强行开更多 issue。

## Freely-Centric Synthesis

把外部文章放回 Freely 自己的目标后，可以更明确地得到下面这组判断。

### 我们真正要造的不是“agent coding workflow”，而是“自治开发应用的运行器”

Freely 的主目标并不是提升某个编码 agent 的个人产能，而是让一个应用项目能在三层循环下持续推进：

1. `auto-loop`
   - 负责发现输入、判定来源、路由下一跳、主管监督、恢复续接。
2. `doc-pre-brainstorm / doc-ibm`
   - 负责把模糊需求、边界外问题、issue 契约、验收口径收敛成机器可执行的项目文档。
3. `dev-loop`
   - 负责在正确 worktree 中实现、测试、回写执行态与恢复态。

因此，Freely 的关键问题不是“agent 会不会写代码”，而是：

- 是否能持续找到下一步该做什么；
- 是否能把边界不清的问题先收敛，而不是硬写；
- 是否能在实现中维持 worktree / checkpoint / recovery / supervision 纪律；
- 是否能在出错后续接，而不是会话死掉就停止。

### 现有设计已经覆盖的关键面

如果仅看“理念层”，Freely 其实已经比文章更贴近自治开发应用：

1. 已经有明确三层循环，不是单环 prompt engineering。
2. 已经有 discovery -> pre-brainstorm -> IBM -> dev -> verification -> recovery 的状态语义。
3. 已经把 worktree、分支纪律、主管/worker 分工写进宪法和法律。
4. 已经把 runtime / hook / skill / agent 分成不同层，不把所有控制逻辑塞进一个 prompt。
5. 已经把“边界外新问题 reroute 到 pre-brainstorm”当成正式治理，而不是临场判断。

这些都是 Freely 的核心资产，不需要因为外部文章而重写。

### 真正还缺、且会阻塞自治开发应用的面

当前最需要继续收敛的是执行基座，而不是 loop 定义本身：

1. `feedback substrate`
   - runtime/status/fleet-status/checkpoint 已存在，但还没有统一成对 agent 低成本可读的反馈面。
   - “项目当前发生了什么”仍然要靠分散文档和脚本输出拼接。

2. `enforcement substrate`
   - 一部分规则已经进入 hook 和 CLI。
   - 但仍有不少规则主要存在于文档和 prompt 注入，缺少统一 enforcement 编译面。

3. `cleanup substrate`
   - Freely 已意识到治理漂移、上下文漂移、checkpoint drift。
   - 但还未形成常驻的 doc/code gardening 后台循环。

4. `application-facing observability`
   - Freely 要做“自治开发应用”，最终不能只有 shell/runtime 自己看得懂。
   - 需要把 session/run/agent/governance/recovery 的事实态暴露给应用内 UI 和 agent 自己消费。

### 本次研究的真实产出方式

因此，本次研究最合理的输出，不是“导入 OpenAI 式工作流”，而是：

1. 用它检查 Freely 现有三层循环是否已经拥有足够的执行基座。
2. 把缺口压缩成少数真正影响自治开发应用的 candidate。
3. 明确记录哪些部分不采用，避免后续反复讨论。

## Non-Adoption Decisions

以下内容在本轮明确判定为“不作为近期设计目标”：

1. 不以“全 agent 生成代码”作为 Freely 的近期成功标准。
2. 不以“更高 PR 吞吐量”作为 Freely 的近期优化目标。
3. 不把 OpenAI 的内部 team workflow 当作 Freely runtime 的直接蓝图。
4. 不因为 external validation 就重写三层循环、工作树治理或文档路由模型。

## Recommended Next Route

本 pre-brainstorm 当前建议维持在“研究收敛完成，但只提少数候选项”的状态：

1. 若需要继续推进，优先 materialize `harness 分层与缺口图`，因为它最接近问题定义层。
2. 若近期目标是直接提高自治开发稳定性，则优先 materialize `统一 machine-readable 状态接口`。
3. `doc-gardening / cleanup loop` 应保持候选状态，等待前两者更清晰后再决定是否提升。
4. 若没有新的明确缺口，这个 pre-brainstorm 可以停留在研究结论，不必强行进入 milestone。

## Candidate Directions

- 把更多 runtime / governance / verification 信号转成 agent 可直接读取的结构化界面。
- 把“文档漂移”和“AI 残渣”治理从人工发现，升级成周期性后台扫描与自动修复提案。
- 强化 `AGENTS.md -> docs/*` 的渐进式披露地图，避免入口文件继续膨胀。
- 为 Freely 定义更明确的 harness 分层：任务入口、反馈采样、约束执行、垃圾回收。

## Source Notes

关键信息来自 OpenAI 原文中的这些段落：

- 从零仓库、全 agent 生成、1/10 时间、约百万行代码与约 1500 PR
- `AGENTS.md` 作为目录而不是百科全书
- worktree + DevTools + 本地可观测性栈 + LogQL/PromQL 查询
- 架构边界与 taste invariants 由自定义 lint / 结构测试强制执行
- 后台 doc-gardening / cleanup loop 处理漂移与技术债
