# OpenAI / Entrix Agentic Engineering Principles Research

## Trigger

用户要求在专用 worktree 中研究 OpenAI 文章《工程技术：在智能体优先的世界中利用 Codex》：

- URL: https://openai.com/zh-Hans-CN/index/harness-engineering/
- publish_date: 2026-02-11
- research_date: 2026-03-19

目标不是复述宣传语，也不是追着 `harness` 这个名字跑，而是抽取对 Freely 作为自主循环运行器最有用的工程理念、判断结构与可落地机制。

## Naming Is Not The Point

这条研究的重点不是某个术语，而是背后的工程原则。无论外部把它叫：

- `harness engineering`
- `fitness`
- `guardrails`
- `change lifecycle`
- `anti-entropy`

Freely 真正要吸收的都是同一类东西：

1. 完成条件必须从人脑里的隐性经验，迁移成系统可执行的判断结构。
2. 自动化不是越多越好，而是要明确哪些判断交给机器、哪些升级更深验证、哪些保留人工复核。
3. agent 不是直接被 prompt 驱动到“写完为止”，而是运行在一个可观测、可约束、可恢复、可回写经验的工程系统里。
4. 熵增不会自己消失，必须有持续的反熵闭环。

## What Harness Actually Is

结合 OpenAI 原文、Entrix 文章和 Thoughtworks 对 `fitness functions` 的定义，`harness` 更准确地说不是某个工具箱，而是一层让 agent 能稳定交付的软件工程控制面。

它至少包含五种能力：

1. `intent encoding`
   - 人类目标、验收条件、架构约束、禁区和升级规则被写进仓库，并且 agent 可发现、可消费。

2. `executable evaluation`
   - 系统能用测试、lint、结构校验、契约校验、性能门槛、运行时观测等手段判断“这次改动距离目标还有多远”。

3. `risk-aware routing`
   - 不是所有改动都走同一套门。
   - 系统要能判断哪些只是低风险快验，哪些需要更深验证，哪些必须拉人进来。

4. `legible work environment`
   - agent 不只是拿到代码，还要拿到可启动的应用、可读的状态、可查询的日志/指标/trace、可导航的知识面。

5. `anti-entropy loop`
   - 经验会被回写成规则，规则会持续扫描偏差，偏差会触发清理或修复，而不是等到人类定期大扫除。

所以，`harness` 的本质不是“辅助 agent 的脚手架”这么浅。
它更像：

- 一个 `agent-readable engineering operating system`
- 一个 `change evaluation and control plane`
- 一个把隐性判断权转成可执行机制的环境层

如果 Freely 能吸收这些能力，它就不只是“有三层循环的 agent runner”，而可以更接近“面向应用开发的 harnessed agentic engineering runtime”。

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

3. Freely 的核心机会不只是“让 agent 写代码”，而是补齐一整套 agentic engineering substrate：
   - completion model
   - machine-readable feedback loops
   - executable invariants
   - anti-entropy loop

4. Freely 当前最值得对齐的不是 OpenAI 的吞吐量结论本身，而是其前提条件。
   - 如果没有严格边界、可执行 lint、可观察性和自修复回路，贸然提高自主度只会放大混乱。

5. Freely 要吸收的不是“OpenAI 的命名”，而是这层环境能力本身。
   - 只有当三层循环内都具备了目标编码、可执行评估、风险分流、环境可读和反熵闭环，Freely 才配称为有 `harness` 能力的 agentic engineering runtime。

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

结论：这些外部研究不是 Freely 的新北极星，也不是要原样照搬的方案包。

- 可保留：
  - “完成条件显式化 + 可执行 guardrails + 持续反熵”这个视角，用来检查 Freely 当前三层循环是否有足够的执行基座。
  - 将 feedback loops / enforcement / cleanup 视为自治开发的必要支撑层。
- 不应高估：
  - 术语本身
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

1. `completion substrate`
   - Freely 已有 route、branch、worktree、verification 等治理边界，但“某次变更为什么算完成、完成到什么层级、何时必须升级验证或人工复核”还没有统一判断结构。
   - 这正是外部文章反复在说、但不能只用术语代替设计的问题。

2. `feedback substrate`
   - runtime/status/fleet-status/checkpoint 已存在，但还没有统一成对 agent 低成本可读的反馈面。
   - “项目当前发生了什么”仍然要靠分散文档和脚本输出拼接。

3. `enforcement substrate`
   - 一部分规则已经进入 hook 和 CLI。
   - 但仍有不少规则主要存在于文档和 prompt 注入，缺少统一 enforcement 编译面。

4. `cleanup substrate`
   - Freely 已意识到治理漂移、上下文漂移、checkpoint drift。
   - 但还未形成常驻的 doc/code gardening 后台循环。

5. `application-facing observability`
   - Freely 要做“自治开发应用”，最终不能只有 shell/runtime 自己看得懂。
   - 需要把 session/run/agent/governance/recovery 的事实态暴露给应用内 UI 和 agent 自己消费。

### 本次研究的真实产出方式

因此，本次研究最合理的输出，不是“导入 OpenAI 式工作流”，而是：

1. 用它检查 Freely 现有三层循环是否已经拥有足够的执行基座。
2. 用它逼出 Freely 自己的 completion model，而不是继续依赖隐性判断权。
3. 把缺口压缩成少数真正影响自治开发应用的 candidate。
4. 明确记录哪些部分不采用，避免后续反复讨论。

## Non-Adoption Decisions

以下内容在本轮明确判定为“不作为近期设计目标”：

1. 不以“全 agent 生成代码”作为 Freely 的近期成功标准。
2. 不以“更高 PR 吞吐量”作为 Freely 的近期优化目标。
3. 不把 OpenAI 的内部 team workflow 当作 Freely runtime 的直接蓝图。
4. 不因为 external validation 就重写三层循环、工作树治理或文档路由模型。

## Recommended Next Route

本 pre-brainstorm 当前建议维持在“研究收敛完成，但只提少数候选项”的状态：

1. 若需要继续推进，优先 materialize `Freely 的 completion model 与 change guardrails`，因为它最接近问题定义层。
2. 若近期目标是直接提高自治开发稳定性，则优先 materialize `支持 guardrail 决策的 machine-readable 状态接口`。
3. `doc-gardening / cleanup loop` 应保持候选状态，等待前两者更清晰后再决定是否提升。
4. 若没有新的明确缺口，这个 pre-brainstorm 可以停留在研究结论，不必强行进入 milestone。

## Three-Loop Absorption Map

如果把 `harness` 背后的能力放回 Freely，自然的吸收方式不是加第四层循环，而是给现有三层循环补控制面能力。

### A. outer loop / auto-loop 要补什么

outer loop 现在更像路由器和监督器，但要变成真正的 harness 控制面，还缺：

1. `change class + risk class`
   - 进入一轮执行前，先判断这是文档改动、实现改动、治理改动、恢复动作，风险半径多大。

2. `guardrail plan synthesis`
   - 基于风险等级自动决定这轮至少要经过哪些 gates：
   - 只跑文档一致性？
   - 还是要跑结构测试？
   - 还是要启动应用、跑 UI/E2E/perf smoke？

3. `escalation policy`
   - outer loop 要有明确的“何时必须人工复核/何时允许 agent 自动推进/何时必须回 pre-brainstorm”的规则。

4. `decision loop writeback`
   - 本轮哪些 guardrail 失效、哪些判断仍依赖隐性知识，必须回写成下一轮规则输入。

### B. doc loops / pre-brainstorm + IBM 要补什么

doc loops 现在已经负责收敛边界，但还没有把“完成条件”物化得足够强：

1. `acceptance as executable intent`
   - issue / brainstorm 不该只写自然语言目标，还要写最小验证门、升级条件、禁止绕过项。

2. `policy artifactization`
   - 规则不能只停留在 issue 说明里。
   - 哪些需要进入 LAWS、哪些需要进 skill、哪些需要进 CLI / lint / test，必须在文档环明确下游落点。

3. `risk decomposition`
   - doc-loop 需要把“这个需求的风险在哪里”提前拆开：
   - 边界风险
   - 架构风险
   - 运行时风险
   - 恢复风险
   - UI/体验风险

4. `verification design`
   - 在进入 dev-loop 前，就应该定义好：
   - 基础门
   - 深验证门
   - 人工复核触发条件

### C. dev-loop 要补什么

dev-loop 已经最接近执行面，但还缺真正的 harness 落地能力：

1. `machine-readable worktree state`
   - 当前 worktree 的 dirty budget、测试状态、runtime 状态、失败类型、可恢复性，要能被统一读取。

2. `multi-depth validation`
   - 不能只有“测试过/没过”。
   - 需要区分 lint/unit/integration/runtime/ui/accessibility/perf/security 等层级。

3. `risk-triggered validation escalation`
   - 当改动触达高风险路径时，dev-loop 应自动升级验证深度，而不是仍走默认快路径。

4. `evidence packaging`
   - 变更完成时，输出的不只是代码 diff。
   - 还要有结构化证据包，说明跑了哪些 gates、跳过了哪些 gates、为什么可以 promotion。

5. `agent-visible observability`
   - 启动出来的 app、日志、指标、trace、错误分类必须足够低成本地暴露给 agent。

### D. cross-loop 常驻能力

这是 Freely 当前最缺、但也是最像真正 harness 的部分：

1. `golden-principles to enforcement compiler`
   - 把“我们喜欢怎样写/哪些模式禁止”从口头经验编译成 lint、hook、CLI guard、structure tests。

2. `background anti-entropy loop`
   - 周期性扫描文档漂移、模式退化、坏 helper、未收敛 issue、状态陈旧等，并产出小修复。

3. `shared evidence plane`
   - 同一条 issue 的 doc、dev、verification、recovery 证据要能被统一消费，而不是散在不同文件里靠人工拼接。

4. `completion ledger`
   - 每次变更为什么被判定为完成，应该留下统一 ledger，而不是只剩 PR/commit/test 输出。

## Minimal Capability Gaps For Freely

如果以“让 Freely 能被称为 harnessed agentic engineering runtime”作为目标，当前最小缺口不是再补一个大而全平台，而是先补下面五项：

1. `completion model`
   - 定义完成层级、升级规则、人工复核触发条件。

2. `guardrail planner`
   - 输入 issue/change/risk，输出本轮必须执行的 gates 与证据要求。

3. `machine-readable evidence interface`
   - 汇总 worktree/runtime/test/verification/recovery 状态，供 agent 决策。

4. `validation escalation engine`
   - 根据风险等级自动提升验证深度。

5. `anti-entropy background loop`
   - 把经验回写、漂移扫描和小步修复常态化。

## 2026-03-20 HelixVerify 增量证据

### 外部来源

- 标题：`Harness Engineering: 为 AI 搭建可持续迭代环境的实践`
- 链接：`https://mp.weixin.qq.com/s/xIWN6_X3UPbLXC3SUUdwrg`
- 读取日期：`2026-03-20`

### 新增观察

这篇文章和前两篇相比，新增价值不在“为什么要 harness”，而在“AI 如何把 harness 逐步自举出来”。

1. 它把 harness 讲成一个 `bootstrapping ladder`。
   - 不是先天完整存在。
   - 而是 AI 在人的引导下，一层层为自己搭环境：先有 `看` 的能力，再有 `量` 的能力，再有 `诊` 的能力，再有 `安全试错` 的能力，最后才有 `7x24 持续运行`。

2. 它把闭环拆成 5 个非常具体的模块：
   - 端到端测试：让 AI 能看懂系统
   - 标准化评测：让 AI 有统一尺子
   - badcase 自动诊断：让 AI 自己发现问题
   - TP 对抗验证：让 AI 的改动不破坏已有正确性
   - 阶梯式验证：让 AI 用最低成本试错

3. 它把 loop 基础设施和业务闭环明确分开。
   - 前 5 个模块回答“AI 能不能自己分析、修改、验证”
   - loop / supervisor 回答“谁来驱动 AI 持续跑下去、何时停下、何时继续、何时升级”

4. 它把 `实验记录` 变成连续迭代的核心 substrate。
   - benchmark 输出、detail 明细、实验目录、版本号、时间戳都被保留下来
   - 新 session 不是靠短期上下文记忆，而是靠实验记录继续推进

5. 它证明了 `safe iteration` 不是抽象原则，而是具体机制组合：
   - badcase 诊断避免瞎猜
   - TP 对抗验证避免优化一个指标破坏另一个指标
   - 阶梯式验证让失败尽早暴露，降低试错成本

6. 它强化了一个对 Freely 很关键的判断：
   - harness 不只是“评估变更是否完成”
   - 还是“帮助 agent 自举出更强执行环境”的机制

### 对 Freely 的新增意义

这篇文章让 Freely 的能力缺口更具体了。

1. Freely 不只缺 `completion model`，还缺 `bootstrap path`。
   - 要让 agent 从“会改代码”逐步进化到“能自举闭环”，系统必须支持能力分阶段长出来，而不是假设所有 substrate 一开始就齐全。

2. Freely 需要补一层 `see + measure substrate`。
   - 现在 Freely 更擅长治理和路由。
   - 但如果 agent 不能低成本地看系统、量化结果、拿到 detail 级证据，它就只能停留在“改代码 + 看粗粒度测试结果”。

3. Freely 需要把 `safe iteration guardrails` 独立成正式能力。
   - 对抗验证
   - 分阶段验证
   - 失败快速暴露
   - 这些不应只是某个 issue 临时手法，而应成为通用执行模式。

4. Freely 需要更强的 `experiment ledger / evidence lineage`。
   - 当前有 progress / recovery / docs，但还缺一层更统一的实验与验证记录面，能跨 session、跨 loop、跨 worktree 被继续消费。

5. outer loop 的 supervisor 角色需要更正式地支持“持续驱动 + 审查 + 升级”。
   - 这篇文章证明，单纯 loop 还不够。
   - 外层仍需要一个更高阶的判断者来决定是否继续、是否升级、是否需要人类介入。

### 对三层循环的补强指向

#### outer loop

- 增加 `bootstrap stage awareness`
- 增加 `loop continuation policy`
- 增加 `supervisor review / escalation`

#### doc loops

- 在 issue / IBM 中显式写出：
  - 当前能力阶段
  - 当前缺的是 `看`、`量`、`诊`、`安全验证` 还是 `持续运行`
- 把验证设计从“是否有测试”提升为“是否具备闭环下一层能力”

#### dev-loop

- 增加标准化 benchmark / detail 输出面
- 增加对抗验证与阶梯式验证
- 增加实验目录和结果 lineage，供下一轮 session 继续消费

### 对当前候选的影响

1. `C-20260319-0402-01`
   - 不只要定义 completion model，还要覆盖 bootstrap ladder：agent 是如何逐层长出闭环能力的。

2. `C-20260319-0402-02`
   - 不只要输出状态摘要，还要输出 benchmark/detail/experiment lineage 这类可续接证据。

3. `C-20260320-01`
   - 需要把阶梯式验证和对抗验证纳入 planner 的 guardrails，而不只是做风险分流。

### 更新后的判断

OpenAI 原文给了总纲，Entrix 文章细化了完成条件和 guardrails，这篇 HelixVerify 文章则补上了第三块关键拼图：

- `harness` 不是静态环境
- 它还是一条 `self-bootstrapping path`

对 Freely 来说，这意味着我们不仅要回答“什么叫完成”，还要回答：

1. agent 当前处在闭环能力的哪个阶段？
2. 下一步该补的是哪一个 substrate？
3. 新补的 substrate 如何被后续 session 和 loop 持续消费？

## Candidate Directions

- 为 Freely 定义更明确的 completion model：什么叫完成、完成到什么层级、何时升级验证或人工复核。
- 把更多 runtime / governance / verification 信号转成 agent 可直接读取的结构化界面。
- 把“文档漂移”和“AI 残渣”治理从人工发现，升级成周期性后台扫描与自动修复提案。
- 强化 `AGENTS.md -> docs/*` 的渐进式披露地图，避免入口文件继续膨胀。

## Source Notes

关键信息来自 OpenAI 原文中的这些段落：

- 从零仓库、全 agent 生成、1/10 时间、约百万行代码与约 1500 PR
- `AGENTS.md` 作为目录而不是百科全书
- worktree + DevTools + 本地可观测性栈 + LogQL/PromQL 查询
- 架构边界与 taste invariants 由自定义 lint / 结构测试强制执行
- 后台 doc-gardening / cleanup loop 处理漂移与技术债

## 2026-03-20 Entrix 增量证据

### 外部来源

- 标题：`Entrix 开源了：我们如何用反熵机制治理 Vibe Coding`
- 链接：`https://mp.weixin.qq.com/s/hvdNDXUJdzxAZMDnk-F0pA`
- 读取日期：`2026-03-20`

### 新增观察

这篇文章提供的增量，不是再次证明“harness engineering 很重要”，而是把完成条件漂移问题拆成了更细的判断结构：

1. 它把问题重心从“agent 写得快”转到“变更何时算完成、何时可信”。
   - 局部绿灯、覆盖率和接口 200 不是完成条件本身。
   - 当 agent 参与交付时，真正需要显式化的是判断权，而不是只补更多自动化步骤。

2. 它把反熵治理拆成变更生命周期里的五段守护层：
   - `Policy Setup`
   - `Quality Gates`
   - `Risk Routing`
   - `Deep Validation`
   - `Decision Loop`

3. 它强调 `fitness` 不是 SDLC 里的单一步骤，而是贯穿变更生命周期的 guardrail。
   - 越靠左的检查越适合自动阻断。
   - 越靠右的判断越依赖语义、上下文和风险半径，因此更适合升级人工 review 或更深验证。

4. 它把 `risk routing` 说得比 OpenAI 原文更具体。
   - 不是只有 lint / test / observability。
   - 还包括高风险目录、diff 扩张、graph review context、以及何时升级到人工复核。

5. 它把 `deep validation` 单独提成一层。
   - API parity
   - 安全扫描
   - shell / UI 的 E2E、Accessibility、Visual Regression、performance smoke
   - 这说明 machine-readable feedback 还不够，Freely 还需要“按风险升级验证深度”的分层能力。

### 对 Freely 的新增意义

这篇文章把本 pre-brainstorm 里的 `feedback loops / invariants / cleanup` 三件事，进一步压实成“完成条件显式化 + 变更生命周期 guardrails”问题：

1. Freely 不只需要一份静态能力分层图。
   - 还需要回答不同层的 guardrail 在 change lifecycle 的哪个阶段触发。

2. Freely 现有候选 `统一 machine-readable 状态接口` 仍然成立，但边界应更具体。
   - 不只是把状态暴露出来。
   - 还要能支持 risk-aware routing：什么改动只需基础门、什么改动要升级到更深验证、什么改动要人工复核。

3. `doc-gardening / cleanup loop` 依旧重要，但它更像决策闭环的右侧能力。
   - 没有前面的 policy / gates / risk routing / deep validation，单独做 cleanup 容易变成“清理动作很多，完成条件仍然模糊”。

4. Freely 还缺一层更明确的 `change completion model`。
   - 当前治理更强于 branch/worktree/route discipline。
   - 但对“某次变更算不算被充分证明”还缺一套统一结构，尤其是风险分流和验证升级机制。

### 对当前候选的影响

1. `C-20260319-0402-01` 需要把“harness 分层图”从静态能力盘点，收束为 `policy -> gates -> risk routing -> deep validation -> decision loop` 的 change-lifecycle 视图。
2. `C-20260319-0402-02` 需要把“统一状态接口”扩展为“支持风险分流与验证升级决策的 machine-readable 接口”，而不只是状态摘要。
3. `C-20260319-0402-03` 继续维持 `needs_research`。
   - 这篇文章证明 cleanup 属于体系的一部分。
   - 但它不是当前最先 materialize 的入口，仍应排在 lifecycle guardrails 和 risk-aware feedback 之后。

### 更新后的判断

OpenAI 原文更像“自治开发基座的总纲”，Entrix 文章则更像“变更完成条件、判断分层与反熵闭环的细化补丁”。

因此，这条 pre-brainstorm 的合理收束方向不是继续泛泛讨论某个名词，而是更明确地回答两个问题：

1. Freely 的 change lifecycle guardrails 应如何分层？
2. 哪些 machine-readable 信号足以支持 risk routing、deep validation 和 decision loop？
