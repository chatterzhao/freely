# Brainstorm: freely-layered-architecture-and-tooling-topology

- brainstorm_id: `20260326-1810--freely-layered-architecture-and-tooling-topology`
- created_at: `2026-03-26`
- status: `active`
- related_signals:
  - 当前 `three-loop-capability-lifecycle` 能解释 loop / route / lifecycle，但不等于整套 Freely 产品/系统分层图。
  - 当前 `docs/system/workspace/tools.md` 已经定义 `codex`、`cc`、`cc-use-codex-cli`、`iflow` 等 AI tool/runtime 使用方式，但这些工具层还没有被放进一张更上位的体系拓扑图里。
  - 用户明确指出上一版方块图有两个错误：`chat` 不应和 `CLI/TUI/GUI` 并列；AI tool usage layer 不能缺席，尤其 Freely 如何使用 `codex cli`、`claude code` 等是系统本体的一部分。

## Problem

Freely 现在缺一份更总览的 architecture/topology 真源，导致几个层面容易混在一起：

- loop/lifecycle 真源
- 产品交互入口与操作语义
- 状态/观测语义
- 终端/界面载体
- 外部 AI tool orchestration layer
- runtime/agent orchestration layer
- backend contract / adapter boundary
- eval/harness/supporting substrate

结果是：

- `three-loop-capability-lifecycle` 容易被误当成整栋系统地图
- `chat`、`start`、`init` 这种交互入口会和 `CLI/TUI/GUI` 这种载体/表面形态并列
- `status`、`live-status`、`fleet-status` 这种观测入口也容易被误放到和 `CLI/TUI/GUI` 同一层
- `codex cli`、`Claude Code`、`codex MCP` 这种“Freely 如何借力外部 AI 工具”没有稳定层级归属
- `backend contract`、`adapter`、`control surface` 的边界虽然在局部 issue 中存在，但没被放回整张总图

## Desired Outcome

收敛一份更准确的 Freely 分层图，至少回答：

1. 哪些层是 Freely 产品本体
2. 哪些层是 Freely 借力外部 AI 的工具编排层
3. 哪些层是 eval / harness / evidence / replay 支撑层
4. `chat`、`start`、`tui`、`cli`、`gui` 到底分别属于“入口”、“交互模式”还是“表面载体”
5. `three-loop-capability-lifecycle` 应是这张图的一部分，还是只被它引用
6. `status` family 应属于哪一层，以及它与 `CLI/TUI/GUI` 的关系是什么
7. `backend contract` / `adapter` / `host shell` 是否应被显式拆层，而不是继续口头区分

## Tensions

- 不能为了画大图，把现有 `three-loop`、`tools.md`、agent/runtime/contracts 的边界打散。
- 不能把“交互入口”与“前端/终端载体”混成一层。
- 不能把“观测语义”与“宿主壳”混成一层；`status` 家族可能暴露在 CLI 中，但不因此等于 CLI 自身。
- 不能把外部 AI tool 当成 Freely 的外部杂项；按当前 dogfooding 方式，它们是 Freely architecture 中被明确编排的一层。
- 不能把 `ClientCommand` / `ServerEvent` / `Snapshot` 这种 backend contract 误当成某个前端壳的私有协议。
- 不能过早决定一定改 `three-loop`；更可能是新增一份更上位的 topology 文档，再让 `three-loop` 和 `tools.md` 各守其位。

## Likely Landing Zones

- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/tools.md`
- 新增一个更上位的 architecture/topology 真源，可能位于：
  - `docs/system/workspace/layered-architecture.md`
  - 或 `docs/system/architecture/freely-layered-topology.md`

## Working Hypothesis

目前更合理的方向不是“把所有内容都塞回 three-loop”，而是：

- 新增一份更上位的 layered architecture / topology 真源
- `three-loop-capability-lifecycle` 继续只负责 loop/lifecycle map
- `tools.md` 继续只负责外部 AI tool inventory / routing contract
- 新的 topology 文档负责把它们放进同一张楼层图里

这份拓扑真源至少要同时表达两件事：

1. 纵向分层：哪些能力在系统中承上启下
2. 横向正交：哪些概念不是“层”，而是跨层暴露到不同宿主壳的语义面

纵向上，当前最小可行分层更像：

1. operational substrate
2. harness / eval support
3. autonomy evals / acceptance plane
4. external AI tooling / execution provider layer
5. Freely runtime / orchestration layer
6. service / contract layer
7. host shell / product surface layer

横向上，至少有两组不该再被误画成纵向并列层的语义面：

- front-door interaction semantics
  - `init`
  - `start`
  - `chat`
  - control actions
- observability semantics
  - `baseline-status`
  - `live-status`
  - `fleet-status`
  - session / artifact / stream deep refs

也就是说：

- `chat` 不是 `CLI/TUI/GUI` 的 peer；它是 interaction semantic
- `status` family 也不是 `CLI/TUI/GUI` 的 peer；它是 observability semantic
- `CLI/TUI/GUI` 更像 host shell / form factor，承载这些语义面
- backend service contract 与 adapter taxonomy 也是独立层，不该被并入 `GUI` 或 `status`

## Proof Of Thoughtfulness

这次预研里，最重要的收敛不是“把方块重新摆一遍”，而是确认 Freely 当前至少有三类常被混淆但本质不同的东西：

1. vertical layer
   - 例如 external AI tooling、runtime orchestration、backend contract、host shell
2. semantic surface
   - 例如 `chat` submit、`status` family、human intervention、control actions
3. rendering / carrier
   - 例如 CLI、TUI、GUI、probe、未来其他 control surface

如果只画单轴楼层图，不额外标出 semantic surface，就会自然犯两个错误：

- 把 `chat` 和 `CLI/TUI/GUI` 并列
- 把 `status` family 和 `CLI/TUI/GUI` 并列

但项目现有真源已经部分证明它们不应这样站位：

- `auto-loop-orchestrator` 已明确 `freely` 是唯一 front-door command，`chat` 是 canonical high-level submit primitive，而未来 GUI 必须复用同一 backend contract。
- `cli-first-entrypoint-and-observability-surface-unification` 已明确 CLI status family 是未来 TUI/GUI 的 canonical backend interface，而不是和 TUI/GUI 同类的宿主壳。
- `backend-service-contract-and-adapter-taxonomy` 已明确 contract layer 与 adapter layer 分离，说明 UI/transport 也不是语义本体。
- `tools.md` 已明确 `codex`、`cc`、`cc-use-codex-cli` 是 Freely runtime 编排的外部 AI tool，而不是零散工具清单。
- `three-loop` 已明确 front-door flow 与 observability planes，但它的职责仍是 lifecycle / route / ownership，不是整栋楼的 architecture atlas。

因此这里真正缺的不是局部定义，而是一份统一总图，能把“层”和“跨层语义面”同时表达出来。

## Existing Truth And Drift Inventory

项目里已经有局部真源，但它们分散，且容易被过度延伸：

- `docs/system/workspace/three-loop-capability-lifecycle.md`
  - 已有：front-door、observability planes、loop ownership、worktree lifecycle
  - 漂移风险：容易被误当成 whole-system topology
- `docs/system/workspace/tools.md`
  - 已有：external AI tooling inventory / routing contract
  - 漂移风险：没有被放回总拓扑，读者容易把它当成 implementation appendix
- `docs/epics/workspace-routing-foundation/cli-first-entrypoint-and-observability-surface-unification/**`
  - 已有：`chat` submit primitive、status family backend interface、TUI/GUI render-layer direction
  - 漂移风险：结论停留在 issue 语境，没有沉淀成 architecture atlas
- `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/**`
  - 已有：contract vs adapter boundary
  - 漂移风险：停留在 control-surface 线，未进入全局产品拓扑

当前项目更像“有了多张局部正确的工程图”，但还没有“一张完整楼层图”。

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
4. external execution provider layer
   - `codex`
   - `cc`
   - `cc-use-codex-cli`
   - `iflow`
   - `kiro-cli`
   - MCP-assisted tool usage
5. Freely runtime / orchestration
   - `freely` runtime scripts
   - lead / manager / worker
   - three-loop routing
   - continuity / handoff / patrol / queue / recovery
6. service contract / adapter layer
   - `ClientCommand`
   - `ServerEvent`
   - `Snapshot`
   - `tauri_adapter`
   - `ws_adapter`
   - `local_process_adapter`
7. host shell / product surface
   - CLI shell
   - TUI shell
   - GUI / probe / future control surface

### Orthogonal semantic surfaces

这些不是 vertical peer layer，而是跨层暴露给 host shell 的语义面：

- boot semantics
  - `init`
  - `start`
- submit / intervention semantics
  - `chat`
  - future human intervention submit path
  - control actions such as pause / retry / resume
- observability semantics
  - `baseline-status`
  - `live-status`
  - `fleet-status`
  - session / stream / artifact deep refs

### Mapping back to current truth sources

| Current truth source | Best-fit place in topology | Why |
| --- | --- | --- |
| `three-loop-capability-lifecycle.md` | Freely runtime / orchestration | 它讲 loop、route、ownership、front-door flow、observability planes，但不等于 whole-system atlas |
| `tools.md` | external execution provider layer | 它定义 Freely 如何编排外部 AI tools，而不是 UI 或 lifecycle atlas |
| `cli-first-entrypoint-and-observability-surface-unification` | semantic surfaces + host shell relation | 它说明 `chat` submit primitive、status family backend interface、TUI/GUI render relation |
| `backend-service-contract-and-adapter-taxonomy` | service contract / adapter layer | 它冻结 contract vs adapter，而不是 front-door 或 tooling |
| frontend probe / control-surface issues | host shell / product surface | 它们是具体 render shell 与 interaction composition，不是 runtime 本体 |

### Current mismatch markers

- mismatch: repo 已经把 `chat` 写成 canonical submit primitive，但还没有在 architecture 总图里把它与 host shell 分离
- mismatch: repo 已经把 status family 写成 observability/backend interface，但还没有在 architecture 总图里把它与 CLI/TUI/GUI 分离
- mismatch: repo 已经把 external AI tools 写成正式 runtime 编排对象，但缺少一份总图说明它们处在 runtime 之下、宿主壳之外
- mismatch: repo 已经把 contract vs adapter 与 Tauri/WS 分离，但这条边界仍主要停留在 control-surface 线，没有回写到全局 architecture 层

## Open Questions

1. 最终文档应采用“单轴层级图 + 正交语义面注释”，还是直接采用“两轴拓扑图”？
2. `chat`、`start`、`init` 应归入统一 front-door semantic，还是区分 boot / submit / control 三类？
3. `CLI / TUI / GUI / probe` 应命名为 host shell、product surface，还是 shell + surface 分两层？
4. `codex cli`、`Claude Code`、`iflow`、`kiro-cli` 是“tooling layer”，还是“execution provider layer”更贴切？
5. `autonomy evals` 与 `harness` 应否分成两层，而不是合成一层？
