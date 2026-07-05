# Brainstorm: freely-layered-architecture-and-tooling-topology

- brainstorm_id: `20260326-1810--freely-layered-architecture-and-tooling-topology`
- created_at: `2026-03-26`
- status: `active`
- related_signals:
  - 当前 `three-loop-capability-lifecycle` 能解释 loop / route / lifecycle，但不等于整套 Freely 产品/系统分层图。
  - 当前 `docs/system/workspace/tools.md` 已经定义 `codex`、`cc`、`cc-use-codex-cli`、`iflow` 等 AI tool/runtime 使用方式，但这些工具层还没有被放进一张更上位的体系拓扑图里。
  - 用户明确指出上一版方块图有两个错误：`chat` 不应和 `CLI shell / TUI shell / GUI app` 并列；AI tool usage layer 不能缺席，尤其 Freely 如何使用 `codex cli`、`claude code` 等是系统本体的一部分。

## Problem

Freely 现在缺一套更总览的高层 architecture/topology 表达，导致几个层面容易混在一起：

- loop/lifecycle 真源
- command family 与其暴露的语义
- 状态/观测语义
- host shell / form factor
- external AI tooling layer
- runtime/agent orchestration layer
- backend contract / adapter boundary
- evaluation harness + autonomy evals / acceptance

结果是：

- `three-loop-capability-lifecycle` 容易被误当成整栋系统地图
- `chat`、`start`、`init` 这些 command family 成员容易和 `CLI shell / TUI shell / GUI app` 这类 host shell 并列
- `status`、`live-status`、`fleet-status` 这种观测入口也容易被误放到和 `CLI shell / TUI shell / GUI app` 同一层
- `codex cli`、`Claude Code`、`codex MCP` 这种“Freely 如何借力外部 AI 工具”没有稳定层级归属
- `backend contract`、`adapter`、`control surface` 的边界虽然在局部 issue 中存在，但没被放回整张总图

## Desired Outcome

收敛一份更准确的 Freely 分层图，至少回答：

1. 哪些层是 Freely 产品本体
2. 哪些层是 Freely 借力外部 AI 的工具编排层
3. 哪些层是 eval / harness / evidence / replay 支撑层
4. `chat`、`start`、`init` 分别属于哪些 command family，以及这些 command family 如何映射到 host shells
5. `three-loop-capability-lifecycle` 应是这张图的一部分，还是只被它引用
6. `status` family 应属于哪一层，以及它与 `CLI shell / TUI shell / GUI app` 的关系是什么
7. `backend contract` / `adapter` / `host shell` 是否应被显式拆层，而不是继续口头区分

这轮预研的首个正式产物应优先落在：

- `docs/PROJECT_INTENT.md`
  - 表达 Freely 自身的高层产品/系统架构拓扑
- `docs/CONSTITUTION.md`
  - 冻结必须遵守的架构硬边界
- `docs/LAWS.md`
  - 补齐判定、验收与对齐规则
紧随其后的入口对齐：

- `AGENTS.md`
  - 不是架构真源本体
  - 只负责同步开发入口的判断顺序

然后再据此回头检查开发期文档与局部 issue 是否需要对齐；本轮不把这件事直接写进 `docs/system/workspace/**`。

## Tensions

- 不能为了画大图，把现有 `three-loop`、`tools.md`、agent/runtime/contracts 的边界打散。
- 不能把“交互入口”与“前端/终端载体”混成一层。
- 不能把“观测语义”与“宿主壳”混成一层；`status` 家族可能暴露在 CLI 中，但不因此等于 CLI 自身。
- 不能把外部 AI tool 当成 Freely 的外部杂项；按当前 dogfooding 方式，它们是 Freely architecture 中被明确编排的一层。
- 不能把 `ClientCommand` / `ServerEvent` / `Snapshot` 这种 backend contract 误当成某个前端壳的私有协议。
- 不能过早决定一定改 `three-loop`；更可能是新增一份更上位的 topology 文档，再让 `three-loop` 和 `tools.md` 各守其位。
- 不能把 Freely 自己的产品形态选择，直接误写成 Freely 对外可复用能力。
- 即使未来要沉淀“产品形态收敛方法”，也必须先抽象成独立能力，而不是把 Freely 当前的 `CLI-first` 选择直接推广成通用法则。

## Likely Landing Zones

- 第一落点：
  - `docs/PROJECT_INTENT.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
- 紧随其后的入口对齐：
  - `AGENTS.md`（开发入口同步，不是并列架构真源）
- 开发期承接：
  - `docs/B1-docs/raw-`
  - 后续若需要更大范围的 repo 对齐，再进入 `docs/epics/`
- 暂不把这轮讨论直接落到 `docs/system/workspace/**`

## Working Hypothesis

目前更合理的方向不是“把所有内容都塞回 three-loop”，而是：

- 先在开发文档中收敛 Freely 自身的产品/系统架构拓扑
- 首先回写 `PROJECT_INTENT / CONSTITUTION / LAWS`
- 再同步更新 `AGENTS.md`，让开发入口能按新的分类顺序思考
- `three-loop-capability-lifecycle` 继续只负责 loop/lifecycle map
- `tools.md` 继续只负责外部 AI tool inventory / routing contract
- 之后再检查 repo 里哪些局部文档或 issue 需要对齐到新的架构表达

这套高层架构表达至少要同时表达两件事：

1. 纵向分层：哪些能力在系统中承上启下
2. 横向正交：哪些概念不是“层”，而是跨层暴露到不同宿主壳的语义面

纵向上，当前最小可行分层更像：

1. operational substrate
2. harness / eval support
3. autonomy evals / acceptance plane
4. external AI tooling layer
5. Freely runtime / orchestration layer
6. service contract layer
7. adapter layer
8. host shell / form factor layer

横向上，至少有三组不该再被误画成纵向并列层的语义面：

- boot / control command family
  - `init`
  - `start`
- submit / intervention command family
  - `chat`
  - control actions
- observability semantics
  - `baseline-status`
  - `live-status`
  - `fleet-status`
  - session / artifact / stream deep refs

也就是说：

- `chat` 不是 `CLI shell / TUI shell / GUI app` 的 peer；它是 submit / intervention command family 的一部分
- `status` family 也不是 `CLI shell / TUI shell / GUI app` 的 peer；它是 observability semantic
- `CLI shell / TUI shell / GUI app` 更像 host shell / form factor，承载这些 command family 与语义面
- backend service contract 与 adapter taxonomy 也是独立层，不该被并入 `GUI` 或 `status`

这里还要额外守住一个边界：

- 当前讨论的是 Freely 自身的产品/系统架构
- 不是在定义“所有未来应用都应采用 `core + CLI + TUI + GUI`”
- 若未来真要形成通用能力，它应是类似“product-shape architecture method / skill”这类更抽象的方法能力
- 而那条能力必须允许 `CLI-first`、`GUI-first`、`GUI-only`、`API-first` 等不同产品形态，而不是复制 Freely 自己的壳组合

## Proof Of Thoughtfulness

这次预研里，最重要的收敛不是“把方块重新摆一遍”，而是确认 Freely 当前至少有三类常被混淆但本质不同的东西：

1. vertical layer
   - 例如 external AI tooling、runtime orchestration、service contract、adapter、host shell
2. semantic surface
   - 例如 `chat` submit、`status` family、human intervention、control actions
3. host shell / form factor
   - 例如 CLI shell、TUI shell、GUI app、probe surfaces、未来其他 control surfaces

如果只画单轴楼层图，不额外标出 semantic surface，就会自然犯两个错误：

- 把 `chat` 和 `CLI shell / TUI shell / GUI app` 并列
- 把 `status` family 和 `CLI shell / TUI shell / GUI app` 并列

但项目现有真源已经部分证明它们不应这样站位：

- `auto-loop-orchestrator` 已明确 `freely` 是唯一 front-door command，`chat` 是 canonical high-level submit primitive，而未来 GUI 必须复用同一 backend contract。
- `cli-first-entrypoint-and-observability-surface-unification` 已明确 CLI status family 是未来 TUI/GUI 的 canonical backend interface，而不是和 TUI/GUI 同类的宿主壳。
- `backend-service-contract-and-adapter-taxonomy` 已明确 contract layer 与 adapter layer 分离，说明 UI/transport 也不是语义本体。
- `tools.md` 已明确 `codex`、`cc`、`cc-use-codex-cli` 是 Freely runtime 编排的 external AI tooling，而不是零散工具清单。
- `three-loop` 已明确 front-door flow 与 observability planes，但它的职责仍是 lifecycle / route / ownership，不是整栋楼的 architecture atlas。

因此这里真正缺的不是局部定义，而是一份统一总图，能把“层”和“跨层语义面”同时表达出来。

同时也要承认，这份总图首先只回答“Freely 自己是什么”。它还没有自动回答“Freely 以后帮别人做产品时应该怎么选产品形态”。后者如果要进入能力目录，需要单独收敛、单独命名、单独验收。

## Existing Truth And Drift Inventory

项目里已经有局部真源，但它们分散，且容易被过度延伸：

- `docs/system/workspace/three-loop-capability-lifecycle.md`
  - 已有：front-door、observability planes、loop ownership、worktree lifecycle
  - 漂移风险：容易被误当成 whole-system topology
- `docs/system/workspace/tools.md`
  - 已有：external AI tooling inventory / routing contract
  - 漂移风险：没有被放回总拓扑，读者容易把它当成 implementation appendix
- `docs/PROJECT_INTENT.md`
  - 已有：高层 loop 结构、来源与路由总述
  - 漂移风险：缺一张明确区分 host shell、semantic surface、tooling layer 的 Freely 产品架构图
- `docs/CONSTITUTION.md`
  - 已有：技术栈、终端架构、CLI-first 等硬边界
  - 漂移风险：已有硬边界还没被放回一份更完整的 Freely 产品拓扑叙事里
- `docs/LAWS.md`
  - 已有：判定规则、验收证据、架构治理进入 pre-brainstorm 的流程
  - 漂移风险：尚未对“新的产品架构表达形成后，哪些文档必须跟随对齐”给出清晰操作口径
- `AGENTS.md`
  - 已有：开发 Freely 时区分“开发目录”和“能力目录”的入口指引
  - 漂移风险：当前还没有把“先判断是 Freely 自身产品架构，还是可复用能力”写成更清晰的首跳思考顺序
- `docs/B2-docs/human/cli-first-entrypoint-and-observability-surface-unification/**`
  - 已有：`chat` submit primitive、status family backend interface、TUI/GUI render-layer direction
  - 漂移风险：结论停留在 issue 语境，没有沉淀成 architecture atlas
- `docs/B2-docs/runtime/control-surface/**`
  - 已有：contract vs adapter boundary
  - 漂移风险：停留在 control-surface 线，未进入全局产品拓扑

当前项目更像“有了多张局部正确的工程图”，但还没有“一张完整楼层图”；而这张楼层图首先应属于 Freely 自身架构的高层开发文档，而不是先写成能力目录。

另一个明确的非目标是：不把这次预研偷换成“泛化一套所有项目都应遵守的产品形态能力”。如果未来真出现那类需求，也应该是另一条独立 pre-brainstorm。

## Provisional Topology Draft

注意：这不是最终 frozen 命名，只是当前证据下最稳的一版草图。

### Vertical stack

1. operational substrate
   - git / branch / worktree
   - filesystem / prompts / jsonl / logs / session-state
   - process control / watchdog / shell runtime
2. evaluation harness
   - test runners
   - replay scripts
   - evidence collection
   - environment setup
3. autonomy evals / acceptance
   - integration acceptance
   - real-environment dogfooding
   - e2e runtime replay
   - verification / regression expectations
4. external AI tooling layer
   - `codex`
   - `cc`
   - `cc-use-codex-cli`
   - `iflow`
   - `kiro-cli`
   - tool integrations such as MCP-assisted tool usage
5. Freely runtime / orchestration
   - `freely` runtime scripts
   - lead / manager / worker
   - three-loop routing
   - continuity / handoff / patrol / queue / recovery
6. service contract layer
   - `ClientCommand`
   - `ServerEvent`
   - `Snapshot`
7. adapter layer
   - `tauri_adapter`
   - `ws_adapter`
   - `local_process_adapter`
8. host shell / form factor layer
   - CLI shell
   - TUI shell
   - GUI app
  - probe surfaces / future control surfaces

### Orthogonal semantic surfaces

这些不是 vertical peer layer，而是跨层暴露给 host shell 的 command family 与语义面：

- boot / control command family
  - `init`
  - `start`
- submit / intervention command family
  - `chat`
  - future human intervention submit path
  - control actions such as pause / retry / resume
- observability semantics
  - `baseline-status`
  - `live-status`
  - `fleet-status`
  - session / stream / artifact deep refs

## Proposed First-Doc Responsibility Split

为避免一边收敛架构、一边又把职责混回去，当前建议的首轮文档分工是：

- `docs/PROJECT_INTENT.md`
  - 承接 Freely 自身产品/系统架构的高层拓扑表达
  - 解释 `core`、external AI tooling、runtime/orchestration、service contract、host shell、semantic surfaces 的相互关系
  - 给出整张高层图，以及为什么这样分层
- `docs/CONSTITUTION.md`
  - 只冻结硬边界
  - 例如强制技术栈、CLI-first、终端/PTy 规则、哪些语义必须通过同一 backend contract 暴露
  - 不负责承载整张产品架构叙事
- `docs/LAWS.md`
  - 承接判定规则、验收口径、对齐要求
  - 明确当产品架构表达更新后，哪些开发期文档必须跟随检查和对齐
  - 明确开发过程中发现新讨论时，何时视为 Freely 自身产品架构，何时视为可复用能力发现
- `AGENTS.md`
  - 只承接“开发 Freely 时怎么先判断、怎么首跳路由”
  - 不定义架构本体，只把上述分类顺序变成入口指引

如果这个四分法成立，后续 materialize 就不再是“先改一批文档试试看”，而是一个边界已冻结的架构收敛 issue。

### Mapping back to current truth sources

| Current truth source | Best-fit place in topology | Why |
| --- | --- | --- |
| `three-loop-capability-lifecycle.md` | Freely runtime / orchestration | 它讲 loop、route、ownership、front-door flow、observability planes，但不等于 whole-system atlas |
| `tools.md` | external AI tooling layer | 它定义 Freely 如何编排 external AI tooling，而不是 UI 或 lifecycle atlas |
| `PROJECT_INTENT.md` | Freely product/system high-level topology | 它最适合先承接 Freely 自身产品/系统架构总图 |
| `CONSTITUTION.md` | hard architecture constraints | 它应冻结技术栈、CLI-first、终端边界等硬约束 |
| `LAWS.md` | alignment and acceptance rules | 它应定义新架构表达形成后，哪些文档和验收口径必须同步对齐 |
| `AGENTS.md` | development-entry routing guard | 它不定义架构本体，但应指导开发 Freely 时先判断这类讨论属于产品架构、开发治理还是可复用能力 |
| `cli-first-entrypoint-and-observability-surface-unification` | command family + host shell relation | 它说明 `chat` submit primitive、status family backend interface、TUI/GUI render relation |
| `backend-service-contract-and-adapter-taxonomy` | service contract layer + adapter layer | 它冻结 contract vs adapter，而不是 front-door 或 tooling |
| frontend probe / control-surface issues | host shell / form factor layer | 它们是具体 render shell 与 interaction composition，不是 runtime 本体 |

### Current mismatch markers

- mismatch: repo 已经把 `chat` 写成 canonical submit primitive，但还没有在 architecture 总图里把它与 host shell 分离
- mismatch: repo 已经把 status family 写成 observability/backend interface，但还没有在 architecture 总图里把它与 CLI shell / TUI shell / GUI app 分离
- mismatch: repo 已经把 external AI tools 写成正式 runtime 编排对象，但缺少一份总图说明它们处在 runtime 之下、宿主壳之外
- mismatch: repo 已经把 contract vs adapter 与 Tauri/WS 分离，但这条边界仍主要停留在 control-surface 线，没有回写到全局 architecture 层
- mismatch: `PROJECT_INTENT / CONSTITUTION / LAWS` 各自已有局部正确内容，但还没有统一表达“Freely 自身产品架构先落这三份高层开发文档，再要求其他文档跟随对齐”
- mismatch: `AGENTS.md` 已经要求开发中判断“是否应沉淀为能力”，但还缺一层更明确的前置分流，避免把 Freely 自身产品架构过早推向能力目录
- mismatch: 当前讨论已经触到“产品形态抽象方法”这个潜在能力方向，但这仍只是旁路发现，不能和 Freely 自身产品架构收敛混成同一条 scope

## Open Questions

1. 最终文档应采用“单轴层级图 + 正交语义面注释”，还是直接采用“两轴拓扑图”？
2. `chat`、`start`、`init` 应归入统一 front-door semantic，还是区分 boot / submit / control 三类？
3. `CLI shell / TUI shell / GUI app / probe surfaces` 应命名为 host shell / form factor，还是 shell + surface 分两层？
4. `codex cli`、`Claude Code`、`iflow`、`kiro-cli` 是否统一收敛到 `external AI tooling layer`，并把 execution-provider abstraction 仅作为层内路由语义？
5. `autonomy evals` 与 `harness` 应否分成两层，而不是合成一层？
6. 新架构表达形成后，repo 对齐范围应止于 `PROJECT_INTENT / CONSTITUTION / LAWS / AGENTS.md`，还是要继续 sweep 到相关 epic / issue / system 引用文档？
7. “产品形态抽象方法”是否值得另开独立 pre-brainstorm，而不是继续绑在这条 Freely 自身架构线上？
