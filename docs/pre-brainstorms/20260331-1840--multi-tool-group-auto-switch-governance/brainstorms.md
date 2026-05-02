# 预研头脑风暴：multi-tool-group-auto-switch-governance

## 背景

当前 Freely 的运行配置仍是单工具心智：

- `.freely/config.env` 只有单个 `AI_TOOL`
- `docs/system/workspace/scripts/runtime/ai-cli` 的 slot 真源主要围绕 `codex`
- `global-ai-account-watchdog-and-manager-bootstrap` 已把 `.ai-auth/<slot>`、slot probe、cooldown、watchdog 恢复做成 canonical contract，但作用域仍基本停留在“当前工具内部切 slot”

与此同时，`docs/system/workspace/tools.md` 已经承认 Freely 面向多个外部 AI 工具：

- `iflow`
- `codex`
- `kiro-cli`
- `cc`
- `cc-use-codex-cli`

而且它已经有工具优先级和适用场景的治理表达。

这形成了新的缺口：

1. 工具清单与优先级存在于能力真源里
2. runtime 实际配置仍只能固定在一个 `AI_TOOL`
3. watchdog 能处理同一工具下的部分 slot 不可用，但不能以统一 contract 做“同工具 slot 恢复 -> 跨工具 fallback -> 最终失败显式上报”

用户提出的新能力正是要把这条缺口正式化：

- 支持多个工具组配置
- `auto_switch_tool=true|false`
- `auto_switch_slot=true|false`
- 当前工具失败后，先在 `~/.ai-auth/{tool-name}-*` 中尝试同工具可用 slot
- 同工具都不可用时，再按工具优先级切换到下一个工具
- 全部失败后给出 canonical failure，而不是空转或假健康

同时这里还要冻结一个入口原则：

- 设计必须 `CLI first`
- 但未来若实现 UI，UI 也应只是这套配置真源的可视化编辑入口
- 用户仍可手工编辑配置文件
- 用户仍可通过 CLI 或 UI 做手工切换
- 若开启 `auto`，则 runtime/watchdog 按同一份配置自动恢复

## 现场事实

### 1. 当前配置面没有多工具组 contract

根项目 `.freely/config.env` 只配置了单个 `AI_TOOL="kiro-cli"`，没有：

- 工具组列表
- 跨工具优先级列表
- `auto_switch_tool`
- `auto_switch_slot`

### 2. 当前能力文档已经有“多工具清单 + 优先级”但不是 runtime config 真源

`docs/system/workspace/tools.md` 已定义多个可选工具及其优先级，但它的定位更接近：

- lead-agent 路由参考
- AI 自主选择依据

而不是 watchdog / runtime 可直接消费的配置合同。

### 3. 当前 slot 恢复 contract 仍偏 codex 专属

`runtime/ai-cli` 与现有 watchdog family 大量使用：

- `.ai-auth/<slot>`
- codex slot active file
- codex switch lock
- codex inventory / probe / sweep

这套 contract 目前没有被抽象成“工具无关的 tool -> slot family -> availability probe -> fallback orchestration”。

### 4. 真实现场已经证明“只盯单工具”不够

近期运行中至少同时暴露了两类现场：

- `kiro-cli` 月度请求上限/订阅校验失败，runtime 仍误记为 `ai_exit_rc_0`
- 既有 watchdog 恢复逻辑主要针对 codex slot 账本和 probe

这说明问题不是“配置写长一点”，而是 Freely 还没有把“工具级故障”和“slot 级故障”放在统一恢复状态机里。

## 问题定义

需要冻结的不是一个小参数，而是一条新的 availability orchestration contract：

1. Freely 如何声明“可选工具集合”和“工具优先级”
2. 工具切换与 slot 切换是否独立开关
3. 当前工具失败后，恢复状态机是否固定为：
   - 先同工具 slot sweep
   - 再跨工具 fallback
   - 最终显式失败
4. watchdog、runtime、manager 各自持有什么职责，避免三层都自己做 tool routing
5. 失败分类是否需要提升到“slot 级”和“tool 级”两层，而不是只有当前命令退出码

## 目标

1. 定义多工具组配置合同的最小真源
2. 定义 `auto_switch_slot` 与 `auto_switch_tool` 的语义边界
3. 冻结“同工具优先、跨工具兜底”的 canonical recovery order
4. 明确用户可见失败面，避免限额/认证/网络异常被误记成健康退出
5. 冻结 CLI / 配置文件 / UI 三种入口共享同一配置真源的 contract
6. 为后续 materialize 成 issue 提供稳定范围，而不是直接把设计塞进 runtime 脚本

## 非目标

1. 本轮不直接实现新的 runtime/ai-cli/watchdog
2. 本轮不承诺所有工具都立刻具备统一 probe 能力
3. 本轮不解决每个工具的全部登录/认证细节
4. 本轮不把 AI 自主任务选工具和 watchdog 恢复切工具混成同一件事

## 关键边界

### 1. “工具选择”至少分两层

- 语义路由层：AI 根据任务阶段决定偏向哪类工具
- 可用性恢复层：当前工具/slot 失败后，runtime/watchdog 如何自动恢复

这两层可以共享优先级真源，但不能混成单一隐式逻辑。

### 1.5 配置入口可以多样，但真源只能有一个

这条能力需要同时支持：

- 手工编辑配置文件
- CLI 命令读写配置
- 未来 UI 读写配置
- 手工切换当前工具或 slot
- 自动模式下由 watchdog/runtime 代替用户切换

但这些都不能各自维护一套状态。更稳的 contract 应该是：

- 配置文件是 canonical persisted truth
- CLI 是一等入口
- UI 如果未来出现，应只是同一配置的展示/编辑面
- 自动恢复只消费同一份 persisted truth，而不是旁路写临时状态

### 2. slot 优先于 tool 还是 tool 优先于 slot，必须可配置但不能模糊

若 `auto_switch_slot=true`：

- 当前工具失败后，应先尝试当前工具名下的 slot family
- 只有当前工具 slot family 全部不可用，且 `auto_switch_tool=true`，才允许跨工具

若 `auto_switch_slot=false`：

- 当前工具失败后不得在本工具内隐式切账号/slot

若 `auto_switch_tool=false`：

- 当前工具 slot family 全部不可用后，应直接失败并显式告知

### 3. `.ai-auth` 目录命名需要工具维度真相

用户给出的 `~/.ai-auth/{tool-name}-xx` 很接近可落地 contract，但仍需冻结：

- tool family 的 canonical 命名
- active slot 指针是全局一个，还是每个工具一个
- cooldown/availability ledger 是全局表，还是按工具分区

### 4. 不是所有工具都已经有足够强的 canonical continuity / probe contract

例如：

- `codex` 已有较强 slot / resume / probe 真源
- `kiro-cli` 当前 continuity contract 较弱，而且刚暴露月度限额误分类问题
- `iflow` / `cc` / `cc-use-codex-cli` 的 account/profile/probe 能力未必与 codex 等价

因此不能假设“多工具 fallback”只是把 codex 的 slot 逻辑复制一份。

### 5. 跨工具 fallback 必须冻结 continuity contract，不能隐式降级

当前工具真源已经区分了不同 continuity 强度：

- `codex`：explicit session-addressed resume
- `cc` / `cc-use-codex-cli`：Claude 外层 session + Codex 内层 thread 的双层证据
- `kiro-cli`：当前目录最近会话，weak-contract
- `iflow`：当前 continuity contract 弱于 `codex` / `cc`

因此跨工具切换时必须先回答：

- 什么时候允许跨 continuity class fallback
- 什么时候必须强制 `fresh_with_handoff`
- 哪些证据必须跟随 handoff 落盘
- 哪些工具切换只允许用于“保持自治继续运行”，但不允许冒充“原会话 resume”

更稳的初步 contract 应该是：

1. 同一 continuity class 内的切换，才允许尝试保留 resume 语义
2. 一旦跨到更弱 continuity class，默认强制 `fresh_with_handoff`
3. runtime 必须把“跨工具导致 continuity 降级”显式写成 handoff / state，而不是静默发生

### 6. 多工具恢复必须继承 watchdog 的控制面不变量

现有 codex watchdog 之所以安全，不只是因为能切 slot，而是因为它冻结了以下不变量：

- probe-first truth
- sweep / reprobe 期间 no-launch gate
- serialized switch / lock
- 恢复成功后先写结构化 handoff，再拉起 manager

多工具版本如果不继承这些不变量，就会出现：

- runtime 和 watchdog 同时改 active tool / slot
- 半切换状态被新的 AI launch 消费
- project runtime 把 tool switch 误判成 attachable / healthy

因此这条能力的最小 contract 至少还要定义：

- tool switch lock 是否全局唯一
- tool-level sweep / reprobe 期间是否阻塞所有 AI launch
- active identity 是 `tool + slot` 二元组，而不是仅 slot 或仅 tool
- 跨工具恢复成功后 handoff 至少包含：失败类别、原 tool/slot、新 tool/slot、continuity 降级与否

### 7. 配置真源不只是一份文件，还涉及 project config 与 global profile config 的分层

当前已存在两类配置面：

- project runtime config：`.freely/config.env`
- global AI profile config：`~/.config/freely/ai-cli-profiles.yaml`

因此“CLI first，但可 UI/手工编辑”不能只表达成“入口多样”。还必须冻结：

- 哪些字段属于 project-local truth
- 哪些字段属于 global profile truth
- project-local 是否只引用 global profile group / tool group 名称
- CLI / UI / 手工编辑命中冲突时的优先级与写入序列化

更稳的初步方向是：

1. 账号/profile 清单继续由 global profile config 承载
2. project config 只声明当前项目允许的 tool group、优先级、自动开关和当前 active pointer
3. CLI / UI 都通过同一写路径更新 persisted truth，而不是各自绕过
4. runtime/watchdog 只消费 persisted truth，不旁路写第二套配置

## 初步方向

### 方向 A：在配置面显式引入 tool group

候选配置能力至少应覆盖：

- 当前首选工具
- 工具优先级顺序
- 每个工具的 slot family
- `auto_switch_tool`
- `auto_switch_slot`
- 手工模式与自动模式的切换开关
- 当前 active tool / active slot 的 persisted pointer

是否仍放在 `.env` 里，还是改成结构化文件，需要专门判断；因为一旦有分组、优先级、per-tool 属性、active pointer 与多入口写入，纯平铺 env 的可维护性会迅速下降。

### 方向 B：恢复状态机分两跳

对当前工具故障：

1. 先归类故障是：
   - slot-local
   - tool-local
   - host/network-global
2. 若可做同工具 slot 恢复，则先 sweep 当前工具 slot
3. 若当前工具 exhausted 且允许跨工具，则按优先级找下一个 tool family
4. 所有 tool family exhausted 时，记录 canonical unavailable failure，并向用户暴露

补充冻结：

- `host/network-global` 默认禁止跨工具 fallback；因为它更像共享基础设施故障，而不是某个 tool family 不可用
- `slot-local` 默认允许先做同工具 slot sweep
- `tool-local` 是否允许跨工具，要按 failure allow/deny matrix 明确列出
- 一切跨工具 fallback 都必须经过 no-launch gate 与结构化 handoff

### 方向 C：watchdog 负责恢复，manager 负责解释和监督

更稳的职责划分应接近：

- runtime：捕获当前失败并上报结构化失败原因
- watchdog/control plane：做 slot/tool availability recovery
- manager：在 continuity/live-status 中解释当前全局不可用状态，而不是亲自发明切换策略

## 需要继续冻结的问题

1. 这条能力应吸收到既有 `global-ai-account-watchdog-and-manager-bootstrap`，还是需要 materialize 成新的 issue family
2. 多工具组配置应继续走 `.freely/config.env`，还是升级成单独结构化配置文件
3. `tools.md` 中的 AI 路由优先级，是否应成为 watchdog 可消费的 canonical truth，还是另建 runtime 专用真源
4. 哪些失败允许跨工具 fallback：
   - rate limit
   - auth failure
   - payment/subscription failure
   - oauth unreachable
   - proxy/network unavailable
5. 跨工具 fallback 时是否允许改变 continuity contract 强度，例如从 explicit-session 工具退化到 weak-contract 工具
6. CLI / UI / 手工编辑配置文件三种入口如何避免并发写冲突与状态漂移
7. project-local config 与 global `ai-cli-profiles.yaml` 的字段归属和 precedence 如何冻结

## 生命周期判断

这条线不像现有 codex-slot watchdog issue 的简单 continuation，更像新的 capability family：

- 它新增了配置面
- 新增了 tool-level recovery state machine
- 新增了 per-tool slot family contract
- 新增了跨工具优先级和失败语义

因此当前更稳的判断是：

1. 先保持在 pre-brainstorm
2. 不直接吸收到既有 codex-scoped watchdog issue
3. 待配置真源、职责分层、失败分类冻结后，再决定是否 materialize 成新的 milestone-owned issue
