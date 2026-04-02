# 预研头脑风暴：acp-client-agent-protocol-runtime-adoption

## 背景

Freely 当前已经把 `codex`、`kiro-cli`、`iflow` 等外部 AI CLI 当作被编排的执行提供层；同时仓库里还存在 `cc` / `cc-use-codex-cli` 这类实验性当前实现：

- Freely runtime 负责启动、续接、fallback、auto/step 模式、approval policy、continuity 与 evidence writeback
- 外部工具负责具体的 agent 推进、repo 读写、会话内 reasoning 和 tool usage

在这个语境里，`Agent Client Protocol` 的含义应固定为：

- `Freely` = client / orchestrator
- `codex`、`kiro-cli`、`iflow` = 当前宪法已承诺工具面中的 code agent endpoints
- `cc` / `cc-use-codex-cli` = 当前仓库中的实验性实现 reality，可纳入比较，但不等于宪法已承诺工具面

因此这次预研不是研究“ACP 能否替代 Freely 的治理”，而是研究：

- ACP 是否适合作为 Freely 和外部 code agent 之间的统一接入层
- 它相对当前 launcher/profile-based 实现，在 token、会话、记忆、权限、多工具兼容与工程成本上各有什么利弊

## 已确认事实

### 1. Freely 当前强项不是 transport，而是自治治理

当前 canonical truth 已经覆盖：

- 三 loop 路由
- manager / worker 边界
- worktree / branch 生命周期
- explicit resume / fresh-with-handoff
- auto 模式下的免交互自动批准
- 多工具 fallback、slot、continuity、recovery、queue/freeze

这些都不只是“client 与 agent 怎么通信”，而是 Freely 自己的自治 control plane。

### 2. Freely 当前接入层是工具定制型，不是统一协议型

`tools.md` 与 runtime scripts 当前对不同工具维护各自 profile：

- `codex` 走显式 session id / thread 续接
- 实验性 `cc` 有顶层 Claude 会话，某些 profile 下再嵌 `codex-cli` MCP
- `kiro-cli` 仍偏向“当前目录最近会话”语义
- `iflow` 续接能力也弱于显式会话地址

这说明 Freely 现在的抽象强在治理面，但 agent 接入面是异构的。

### 3. ACP 的核心价值更接近“统一 agent 接口”

若 ACP 成立，它最直接解决的是：

- session 生命周期消息统一
- tool call / tool result / permission message 统一
- client 侧 spawn / supervise / stream / update 的结构化契约统一

它并不天然提供：

- Freely 的生命周期治理
- worktree / milestone / issue / recovery canonical truth
- 风险驱动的批准委员制度

### 4. Freely 的长期记忆本来就不应只压在 agent session 上

Freely 宪法和法律已经把 continuity 明确分层到：

- `candidate`
- `issue`
- `progress`
- `recovery`
- `milestones`

因此“记忆”在 Freely 里本来就不等于“agent 自己记住多少上下文”。

### 5. ACP 的默认 client 形象与 Freely 现状并不完全一致

从 ACP README 与 schema 看，它默认描述的是：

- client = code editor / interactive program
- agent = coding agent
- client 向 agent 暴露文件系统、terminal、permission prompt 等 callback

而 Freely 当前更像：

- client = autonomy runtime / supervisor
- 外部 agent 直接在项目/worktree 中运行
- 文件系统访问、cwd、sandbox、approval、resume target 很多是由 runtime 在 launch 前就决定，而不是等 agent 逐次回调 client

这不意味着 ACP 不能用于 Freely，但意味着：

- Freely 若采用 ACP，更像是“用 supervisor 扮演 ACP client”
- 需要明确哪些 editor-shaped capability 要保留，哪些需要 runtime-shaped adaptation

## 最小 Freely Adapter Contract

基于当前 `tools.md`、runtime launchers、continuity/recovery 真源，Freely 现在已经隐含了一组最小 adapter contract：

### 1. Tool identity and launch profile

- `tool`
- `model`
- `reasoning_effort`
- `mode=auto|step`
- `tool_capabilities`
- `tool_policy`

### 2. Execution environment

- `project_root`
- `cwd policy`
- `sandbox`
- `approval policy`
- project-scoped network/proxy inheritance

### 3. Session and continuity

- `launch_kind=fresh|resume|fresh_with_handoff`
- `tool_session_id`
- `tool_resume_target`
- `jsonl_path`
- `resume_streak`
- `route_only_handoff`
- `context_compacted`
- `context_ratio`

### 4. Nested or layered tool evidence

- top-level Claude session id/jsonl
- nested Codex MCP threadId/jsonl
- same-task continuation should preserve the correct inner/outer thread identity

### 5. Runtime observability and health

- current tool / current slot
- rate-limit and reset evidence
- execution-time network failure taxonomy
- cooldown / retry / switch reason

### 6. Governance-coupled launch metadata

- branch
- worktree_path
- role boundary
- dispatch metadata when delegated: `dispatch_priority` / `parallel_safe` / `write_scope`

## ACP Contract Mapping

下面不是逐字段穷举 schema，而是先看“Freely 要什么”与 “ACP 天然擅长什么”。

| Freely concern | Current Freely truth | ACP fit | Gap / risk |
| --- | --- | --- | --- |
| tool identity | `AI_TOOL`, profile-specific launcher | strong | low |
| session create/load/list | per-tool implementation | strong | weak tools still stay weak |
| streaming updates | cycle log + tool-specific parsing | strong | requires bridge if tool has no native ACP |
| tool call events | tool-specific evidence, especially nested `cc-use-codex-cli` | strong | nested-agent shape may not map cleanly |
| permission request/response | tool-specific flags plus runtime policy | medium-strong | ACP normalizes prompts, not approval governance |
| file system operations | mostly direct process-level repo access | medium | ACP assumes client callbacks; Freely often pre-grants environment |
| terminal operations | external process/PTY owned by runtime | medium-strong | needs careful ownership split |
| cwd/sandbox/approval prebinding | launcher arguments and policy prompt | weak-medium | ACP does not automatically model Freely's exact prelaunch contract |
| long-term memory | canonical artifacts | weak | ACP is not a project memory system |
| recovery truth | progress/recovery/runtime state | weak | remains Freely-owned |
| manager/worker governance | continuity + lane metadata | weak | remains Freely-owned |
| risk-aware approval council | not yet materialized, but Freely-owned future direction | weak | out of ACP scope |

## Formal Mapping Matrix

这张表的目标不是把 schema 全抄一遍，而是冻结一版“Freely 当前最小 adapter contract”与 ACP 的对应关系。

| Freely current field | Current owner | Current carrier | ACP equivalent | Gap | Keep in Freely or move to adapter |
| --- | --- | --- | --- | --- | --- |
| `tool` | runtime | config + launch args | agent identity / initialized capabilities | low | adapter |
| `model` | runtime | config + launch args | session config or agent-specific option | medium | split: adapter transport, Freely policy |
| `reasoning_effort` | runtime | launch args | session config or agent-specific option | medium | split |
| `mode=auto|step` | runtime | config + launcher behavior | session mode or config option | medium | split |
| `tool_capabilities` | runtime | config + tool profile | capability negotiation | low | adapter |
| `tool_policy` | runtime | config + system prompt injection | extension/config, not first-class governance | medium | Freely |
| `project_root` | runtime | launch cwd | file-system / workspace context | medium | split |
| `cwd_mode` | runtime | launcher contract | no exact first-class equivalent | medium-high | Freely |
| `sandbox` | runtime | launcher contract | tool permission / execution policy only indirectly | high | Freely |
| `approval_policy` | runtime | launcher contract | permission requests / responses | high | split: ACP carries messages, Freely owns policy |
| `launch_kind=fresh|resume|fresh_with_handoff` | runtime | session state + launch path | `new_session` / `load_session` only partially | high | Freely |
| `tool_session_id` | runtime | session state | session id | low | adapter |
| `tool_resume_target` | runtime | session state | load-session target | medium | split |
| `jsonl_path` | runtime | local evidence extraction | none | high | Freely |
| `cycle_log` / `debug_log` | runtime | runtime artifacts | none | high | Freely |
| `context_compacted` / `context_ratio` | runtime | parsed evidence | none standardized | high | Freely |
| rate-limit reset evidence | runtime | parsed evidence | none standardized | high | Freely |
| `branch` / `worktree_path` | runtime + governance | continuity artifacts | could ride in metadata/extensions | medium-high | Freely |
| `resume_hint` | runtime + continuity | progress/recovery/handoff | none exact | high | Freely |
| top-level Claude session id | runtime | session state | session id | low | adapter |
| nested Codex MCP thread id | runtime | derived evidence | tool-call related metadata only indirectly | high | Freely |
| file read/write | external agent or runtime bridge | direct workspace access today | ACP fs callbacks | medium-high | optional adapter experiment |
| terminal execution | runtime | PTY/process supervision | ACP terminal APIs | medium | optional adapter experiment |
| tool call updates | tool-specific parsing | logs/jsonl/debug | ACP `tool_call` / `tool_call_update` | low-medium | adapter |
| streaming message chunks | tool-specific parsing | logs/jsonl | ACP `session/update` chunks | low-medium | adapter |
| delegated lane metadata `dispatch_priority/parallel_safe/write_scope` | manager/runtime | continuity + worker prompts | none exact | high | Freely |
| milestone / issue / progress / recovery truth | governance loops | canonical artifacts | none | high | Freely |

### Matrix Reading

从这张矩阵可以得到三个直接判断：

1. ACP 最有价值的吸收面是：
   - session lifecycle
   - update streaming
   - tool call reporting
   - permission message transport
   - optional terminal / file callbacks

2. Freely 绝不能下放给 ACP 的面是：
   - lifecycle truth
   - recovery truth
   - fresh-with-handoff
   - token/rate-limit/context rotation
   - manager/worker dispatch
   - risk-aware governance

3. 最危险的误判是：
   - 以为 ACP 能替代现有 runtime continuity/recovery/control plane
   - 实际上它更像“统一 agent message bus”，不是 Freely 自治内核

## 字段级判断

### 1. ACP 明显适配的字段族

- `initialize` / capability negotiation
- `new_session` / `load_session` / `session/list`
- `session/update`
- `session/cancel`
- mode/config updates
- tool call / tool call update
- permission request / response
- terminal and file callbacks

这些字段族非常适合收束 Freely 当前分散的“会话消息与工具事件”。

### 2. 需要 Freely 保留在上层的字段族

- milestone / issue / progress / recovery truth
- branch / worktree lifecycle judgement
- resume vs fresh-with-handoff policy
- token warn/rotate thresholds
- cross-tool fallback and slot strategy
- dispatch queue / frozen queue / write-scope conflict resolution
- future risk-aware approval planner / committee sizing

这些即使采用 ACP，也仍然是 Freely 自己的控制面。

### 3. ACP 与 Freely 当前形态最可能冲突的点

#### A. File system ownership

ACP 很自然的模式是：

- agent 想读/写文件
- client 提供 `fs.read` / `fs.write` callback

Freely 当前更自然的模式是：

- runtime 直接把 agent 启在 project/worktree 里
- agent 直接对仓库工作区操作

这意味着若采用 ACP，需要二选一：

1. 保持 ACP 的 callback 语义，让 Freely 真正托管 fs operations
2. 做 Freely-specific bridge，把“工作区直接访问”包装成 ACP agent 内部能力

第二种更贴近当前实现，但 ACP 收益会打折。

#### B. Permission ownership

ACP 默认支持 agent 在 tool call 前向 client 请求 permission。

Freely 当前更偏向：

- `auto` 模式在 launch 前就设定好预批准边界
- agent 不应再回头问一个必须在环的人类

因此若采用 ACP：

- permission broker 必须是 Freely runtime
- 且它要支持 machine policy 自动批准，而不是简单转发 prompt

#### C. Nested agent shape

`cc-use-codex-cli` 说明 Freely 已经存在“外层 agent + 内层 capability agent”的双层证据模型。

ACP 若只假设“一个 client 对一个 agent”的平面结构，会遇到两个问题：

- Claude 会话和 Codex thread 谁是 canonical session
- 内层 tool call/thread evidence 如何作为上层 session 的一部分稳定暴露

这需要专门建模，不宜先乐观假设天然兼容。

## Detailed Contract Expansion

上面的“最小 Freely Adapter Contract”是总览。这里把每一层展开成更接近 runtime 当前真实消费面的细化版本，避免后续 materialization 时把 launch/session/continuity/policy 混成一层。

### 1. Launch surface

最小字段：

- `tool`
- `model`
- `mode` (`auto` / `step`)
- `reasoning_effort`
- `tool_capabilities`
- `tool_policy`
- `launch_kind` (`fresh` / `resume` / `fresh_with_handoff`)

补充 capability 字段：

- `codex_capability_model`
- `codex_capability_sandbox`
- `codex_capability_approval_policy`
- `codex_capability_cwd_mode`

含义：

- Freely 不只是“启动某个 agent”
- 它还要同时把 mode、reasoning、工具能力 profile 和 capability-level policy 一起带进去

### 2. Session surface

最小字段：

- `tool_session_id`
- `tool_resume_target`
- `claude_session_id`（仅部分工具）
- `launch_resume_target`

当前事实：

- `codex` 已有 explicit session-addressed resume
- `cc` 有顶层 Claude session id
- 某些 profile 还会存在内层 `codex` thread / session

### 3. Continuity surface

最小字段：

- `tool`
- `session_id`
- `jsonl_path`
- `branch`
- `worktree_path`
- `resume_hint`
- `cycle_log_path`
- `fresh_with_handoff` reason

当前事实：

- `jsonl_path` 在 Freely 里已经是正式 continuity 证据，而不是纯调试细节
- `fresh_with_handoff` 不是错误状态，而是正常轮换模式
- continuity 真相跨 `candidate / issue / progress / recovery`

### 4. Permission / execution policy surface

最小字段：

- `mode`
- `approval_policy`
- `sandbox`
- `cwd_mode`

当前事实：

- Freely 已有免交互 `auto`
- 某些工具 profile 会固定注入 `approval-policy=never`
- `cwd=project-root`、`sandbox=workspace-write` 已是 capability policy 的一部分

### 5. Tool-use / nested capability surface

最小字段：

- `tool_capabilities`
- `tool_policy`
- 是否启用 nested capability（例如 `codex-cli`）
- nested tool 的 session/jsonl evidence（若存在）

当前事实：

- `cc-use-codex-cli` 说明 Freely 已经不只是“调一个 agent”
- 它还要表达 agent 内嵌 capability 的策略与证据模型

### 6. Update / observability surface

最小字段：

- `last_tool_session_id`
- `last_tool_jsonl_path`
- `last_claude_jsonl_path`
- `last_codex_mcp_jsonl_path`
- `context_ratio`
- `context_compacted`
- rate-limit usage / reset 时间
- process exit / recovery signals

当前事实：

- Freely 当前没有统一的跨工具 message bus
- 它更像“runtime variables + cycle log + tool-specific jsonl extractors + status surfaces”
- 这正是 ACP 可能真正改善的地方：把 update / event 从“每工具自解码”收敛到统一 schema

## 对比：ACP 与现有实现

### 1. Token

现有实现的优势：

- Freely 已经把 continuity 外置到 canonical artifacts，而不是全靠会话上下文记忆
- `warn / rotate / fresh-with-handoff` 已形成 token 治理能力
- 对高价值任务可以直接给工具最小 prompt，不需要通用协议包装层

现有实现的劣势：

- 每个工具都要单独注入 prompt policy、approval policy、cwd policy、resume 说明
- 多工具之间的 message 语义不统一，容易产生重复 prompt 包装和 adapter glue
- 当 Freely 想让不同 agent 暴露一致的 session/tool/permission 信息时，要做重复映射

ACP 的优势：

- 若各 agent 都能说同一种 session/update/tool-call 语言，client 端 wrapper 可以收敛
- streaming update、permission、tool-use 等事件可以统一建模，减少“每个工具一套 parser”
- 长远看有机会减少 tool-specific prompt glue 带来的额外 token 和实现噪音

ACP 的劣势：

- ACP 本身不会减少模型推理 token；它主要减少的是接入层和重复包装
- 如果底层 agent 仍需要大量 system prompt 才能遵守 Freely 治理，ACP 不会自动节省这部分 token
- 若为了适配 ACP 又增加 bridge/translation 层，短期 token 与实现复杂度都可能上升

判断：

- ACP 可能降低“接入噪音 token”，但不会直接解决“任务本身的上下文成本”
- Freely 当前 token 治理的主收益仍来自 continuity artifacts 与 rotation，而不是 transport 选择

### 2. 会话

现有实现的优势：

- 对 `codex`，Freely 已经有 explicit session-addressed resume 真相
- 对 `cc-use-codex-cli`，Freely 已经管理双层 session evidence
- runtime 对不同工具的“能否 resume、值不值得 resume”已有本地治理

现有实现的劣势：

- 各工具的 session 语义并不一致
- `kiro-cli` / `iflow` 的 continuity contract 比 `codex` 弱
- manager 在跨工具监督时要理解多套会话模型

ACP 的优势：

- 可以把“session/update/interrupt/permission/tool-call”统一成结构化 client-side model
- Freely 更容易做 generic session supervisor，而不是每个工具单独处理
- 更有利于未来新增 agent，而不用每次从零定义会话桥

ACP 的劣势：

- 若底层工具本身没有稳定 ACP endpoint，Freely 仍要维护 bridge，弱工具不会因为包了一层 ACP 就变成强 continuity tool
- ACP 只能统一外部表现，不能自动弥补底层工具本身缺乏 explicit resume target 的事实

判断：

- ACP 能显著改善“会话模型异构”问题
- 但不会神奇修复弱工具的真实续接能力

### 3. 记忆 / Continuity

现有实现的优势：

- Freely 的长程记忆是 canonical artifacts，不依赖单个 agent session
- `progress / recovery / issue / candidate` 天然支持 fresh process re-entry
- 这和 AI 自治高度一致，比“把记忆塞进 agent 内部状态”更稳

现有实现的劣势：

- agent 层的 session memory 仍然是工具自定义契约
- 跨工具切换时，session memory 只能依赖 handoff，而不能共享统一 session schema

ACP 的优势：

- 可以统一“短期会话态”的事件与结构
- 更容易让 Freely 在不同 agent 前保持统一的 session envelope

ACP 的劣势：

- ACP 不是长期记忆系统，不等于 project memory
- 它不能替代 `candidate / issue / progress / recovery` 这些 Freely 真源

判断：

- Freely 的“长期记忆”已经比 ACP 更适合作为自治真相面
- ACP 只可能补齐“短期会话记忆的统一表达”

### 4. 权限 / 自动批准

现有实现的优势：

- Freely 已经明确支持 `mode=auto`
- 对 `codex` / `cc` 已有 non-interactive auto-approve 映射
- Freely 的目标是“人不在环中必须”，这和当前 runtime 方向一致

现有实现的劣势：

- 当前批准策略更多是工具 profile 级配置，还不是 risk-aware control plane
- 不同工具的 permission 模型差异仍大

ACP 的优势：

- 能统一 permission prompt / permission response 的消息面
- 对 client 侧做自动批准 broker 更友好

ACP 的劣势：

- ACP 常见设计默认仍保留 permission prompt 语义；如果 Freely 要免交互，仍需自己在 client 侧决定何时自动批准、何时升级审议
- 也就是说，ACP 统一的是“权限消息”，不是“批准制度”

判断：

- ACP 可改善权限交互的一致性
- 但 Freely 最缺的仍是 risk-aware approval planner，而不是 permission transport

### 5. 多 agent / 多工具编排

现有实现的优势：

- Freely 已经有 `dispatch_priority`、`parallel_safe`、`write_scope`
- 已有 manager continuity、queue、frozen queue、launch gating
- 这些都直接服务多 lane 自治调度

现有实现的劣势：

- 不同工具的 runtime adapter 成本高
- 如果未来新增更多 code agent，维护成本会继续增加

ACP 的优势：

- 适合作为统一 agent adapter boundary
- 可以降低新增 agent 的接入成本
- 更适合把 Freely 抽成真正的 “client/orchestrator over many code agents”

ACP 的劣势：

- 只有在多个工具都能稳定暴露 ACP 能力时，收益才真正出现
- 若多数工具都要 Freely 自己写桥接器，短期只是在自建另一层复杂度

## ACP 对上述 contract 的可能价值与不匹配

### 1. 对齐得比较好的部分

- `launch session`
- `session update`
- `permission request / response`
- `tool call / tool result`
- client 侧统一 supervise / stream / interrupt

这些都和 Freely 当前的 adapter 疼点相符。

### 2. 只部分对齐的部分

- `reasoning_effort`
- tool-specific capability profile
- nested capability policy，例如 `cc-use-codex-cli`
- `fresh_with_handoff`
- rate-limit / context-ratio 这类 runtime-owned rotation signal

这些更像 Freely 自己为了自治运行补出来的字段，不一定在 ACP 里天然一等存在。

### 3. 基本不该下沉到 ACP 的部分

- milestone / issue / progress / recovery 真相
- branch / worktree 生命周期
- manager / worker dispatch metadata
- `dispatch_priority`
- `parallel_safe`
- `write_scope`
- risk-aware approval council

这些是 Freely 自己的 orchestration 和治理层，不应因为引入 ACP 而降到通信协议里。

## 统一结论

### 1. ACP 在 Freely 中的正确位置

ACP 在 Freely 里的正确位置应明确冻结为：

- `agent communication plane`
- `optional adapter layer`

而不是：

- Freely 的治理平面
- Freely 的 recovery/control-plane 替代品
- 所有工具必须统一迁移到的唯一接入方式

### 2. 推荐架构应是双轨 adapter，不是一刀切替换

更稳定的结论不是“把当前实现重写成 ACP”，而是：

- `direct` 保持一等路径
- `acp` 作为可选路径并行存在
- 每个工具按能力、稳定性、证据强度自行选择 adapter mode

推荐的抽象应更接近：

- `adapter=direct`
- `adapter=acp`
- `adapter=prefer_acp_fallback_direct`

其中第三种最符合 Freely 的现实约束：

- 支持 ACP 且质量足够好，就优先走 ACP
- 不支持 ACP，或支持得不好，就退回直连

### 3. 新增工具的统一判断规则

未来新增工具时，不应先问“它是不是 ACP 工具”，而应先问：

- 它是否满足 Freely 的最小 adapter contract
- 它走 `direct` 还是 `acp`，哪条路径总复杂度更低
- 它的 session / permission / update / continuity 哪条路径更稳定

因此新增工具的 canonical policy 应是：

- 原生 ACP 好用：优先 `acp`
- ACP 缺失或太弱：走 `direct`
- ACP 可用但不完全可信：`prefer_acp_fallback_direct`

### 4. 对现有工具的结论

现有工具不应被要求“一次性迁移到 ACP”。

更合理的策略是：

- 当前已经成熟、证据链稳定、治理清楚的直连路径继续保留
- 只有当某个工具的 ACP 路径明确减少 adapter 复杂度，才值得单独迁移
- `cc-use-codex-cli` 这类 nested profile 不适合作为第一批迁移对象

### 5. 对本次预研的当前判定

基于目前收集到的 contract、映射矩阵、收益/成本，当前最稳的判断是：

- `reject full rewrite`
- `keep ACP as optional adapter research`
- `preserve direct as first-class`
- `allow per-tool adapter selection`
- `only consider a narrow prototype after per-tool fit is concrete`

## 初步判断

### A. 不应把 ACP 当成 Freely 的治理替代品

Freely 的真正核心是：

- autonomy loop
- lifecycle truth
- recovery
- worktree governance
- risk routing

这些不属于 ACP 的主职责。

### B. ACP 值得被视为可选的 agent adapter layer

更合理的位置是：

- Freely governance/runtime 在上层不变
- ACP 落在 `external AI tooling layer` 和 `service contract / adapter layer`
- 用来统一 Freely 与外部 code agent 的通信语义
- `direct` 路径继续保留为并行一等路径

### C. 是否现在就采用，关键看“接入异构成本”是否已高到值得付桥接成本

如果当前主要压力是：

- 多工具 profile 越来越多
- session / permission / tool-use 桥接代码持续膨胀
- 新 agent 接入成本越来越高

那么 ACP 价值会上升。

如果当前主要压力仍是：

- risk-aware approval
- validation escalation
- committee-style autonomous review
- 更强的 continuity / recovery / governance planner

那么 ACP 不是第一优先级。

### D. 对 Freely 当前阶段的建议

第一阶段不做“全量 ACP 化”，而做 bounded research：

1. 先定义 Freely 期望的最小 `agent adapter contract`
2. 用这个 contract 对照 ACP schema，判断：
   - 哪些字段已匹配
   - 哪些字段 ACP 不够
   - 哪些字段是 Freely 独有治理，必须留在上层
3. 只有当至少一个外部 agent 能稳定接成 ACP endpoint 时，再考虑做 prototype bridge
4. 即使后续进入 prototype，也不要求现有工具统一迁移；按 tool 逐个判断 `direct / acp / prefer_acp_fallback_direct`

### E. 更具体的 adoption strategy

若继续推进，建议严格分三步：

1. `contract freeze`
   - 先冻结 Freely 最小 adapter contract
   - 不碰 runtime 主路径
2. `single-agent bridge prototype`
   - 只选一个最适合的工具做桥接原型
   - 候选优先级应是：原生 ACP 支持最好、session 语义最清晰、嵌套最少
3. `go/no-go judgement`
   - 比较 bridge 后是否真的减少 adapter 复杂度
   - 若只是把复杂度从 launcher 挪到 bridge，则不进入主路径

### F. Prototype Candidate Heuristic

如果后续真的要做 prototype，优先级应这样排：

1. 首选“单层 session、没有 nested capability、resume 语义最清晰”的 agent
2. 避免第一刀就选 `cc-use-codex-cli`
3. 避免第一刀就要求 ACP 承担 `fresh_with_handoff`
4. 避免第一刀就把 file system ownership 全量改成 ACP callback

按这个标准，最像 prototype 候选的是：

- 一个原生 ACP agent
- 或一个没有双层会话的单层 code agent bridge

最不适合做第一刀的是：

- `cc-use-codex-cli`
- 任何必须依赖 Freely 现有 nested evidence extraction 才能保持 truth 的 profile

### G. 整体预研收口建议

这条预研现在已经足够统一到以下收口面：

1. 保持在 `pre-brainstorm`
2. 不进入“ACP 全量 adoption”方向
3. 只允许进入“窄 ACP prototype”方向
4. prototype 的前提必须是某个具体工具满足：
   - ACP 路径真实存在
   - adapter 复杂度确实下降
   - 不破坏 Freely continuity / recovery truth
   - 不要求同时重写 direct path

## Prototype Acceptance Direction

如果这条预研后续 materialize 成一个窄 prototype owner，issue-level 验收标准应优先冻结为“adapter mode 可配置且两条路径都能工作”，而不是先追求全工具统一迁移。

### 1. 已存在直连工具的验收

至少选择一个当前已经走 `direct` 的工具：

- 在工具配置中显式看到 adapter mode
- 可以从 `direct` 切到 `acp`
- 配置切换后能够完成最小可验证任务
- status / continuity / recovery 证据仍然可见
- 若 `acp` 路径失败，可退回 `direct` 并恢复工作

最小通过标准：

- “原来能直连的工具”在打开 ACP 配置后，确实能经 ACP 路径工作
- 切换前后不破坏现有 direct path

### 2. 新增工具的验收

至少选择一个新增工具：

- 工具注册时可声明 `adapter=direct` 或 `adapter=acp`
- 若工具支持两种路径，可进一步支持 `prefer_acp_fallback_direct`
- 配置成 `direct` 时能工作
- 配置成 `acp` 时也能工作

最小通过标准：

- “新增工具不是被迫 ACP-only”
- “新增工具也不是被迫 direct-only”
- Freely 能按配置选择接入方式并成功执行最小任务

### 3. 统一行为验收

无论走 `direct` 还是 `acp`，至少应保持以下统一结果：

- 能进入同一套 tool selection / launch 流程
- 能写回同一套 continuity / session evidence
- 能进入同一套 recovery 判断
- 不要求上层治理逻辑因 adapter 不同而分叉成两套 lifecycle

### 4. 明确不作为本阶段验收的内容

首个 prototype 不要求：

- 所有现有工具都支持 ACP
- `cc-use-codex-cli` 这类 nested profile 先完成迁移
- ACP 替代 Freely 的 direct path
- ACP 接管 Freely 的 governance / recovery / planner truth

### 5. Prototype Issue-Level Acceptance Checklist

若这条预研继续 materialize 成 prototype owner，建议把 issue-level 验收单明确冻结为以下 checklist：

- 至少一个现有 `direct` 工具支持在配置中切换到 `acp`
- 切到 `acp` 后可完成一个最小可验证任务
- 切回 `direct` 后原路径不回归
- 至少一个新增工具支持在配置中声明 `adapter=direct` 或 `adapter=acp`
- 若工具两种路径都可用，可进一步支持 `adapter=prefer_acp_fallback_direct`
- 无论走 `direct` 还是 `acp`，都写回同一套 continuity / recovery 证据面
- adapter 差异不会迫使上层治理分裂成两套 runtime 逻辑

若以上 checklist 不能满足，则说明 ACP prototype issue 还不应进入实现。

### 6. Prototype Preconditions

即使只做窄 prototype，也要先承认一个现实前提：

- 当前 runtime 主要仍按 `tool -> launcher case` 直接分派
- 还没有独立成型的 `adapter axis`

因此 prototype 的最小前置条件不是“先把所有工具都 ACP 化”，而是：

- 至少抽出一层可配置的 adapter contract
- 让 `direct` 与 `acp` 成为同一工具选择面下的两种接入方式
- 不要求为此重写整个 runtime，但必须承认这不是零成本 bridge

## Prototype Target Ranking

当前更值得评审的不是“ACP 好不好”，而是“第一刀原型该打在哪个工具上”。

### 1. Ranking Heuristic

优先级判断建议固定为：

- 原生 ACP 支持越明确越优先
- session / resume 语义越单层越优先
- 与 Freely 当前 continuity 证据面冲突越少越优先
- 不要求 nested capability 映射的越优先
- 能同时验证“已有工具切到 ACP”或“新增工具按配置选 direct/acp”的越优先

### 2. Current-Repo Tool Candidates

这组候选属于“仓库内当前已有实现现实”，更适合做第一批 prototype target：

1. `Kiro CLI`
   - 适合作为“现有异构 CLI 走 ACP”候选
   - 价值在于验证 ACP 是否真的比当前较弱 resume 语义更整洁
2. `Codex CLI`
   - 可用于验证 ACP 对成熟 CLI 的接线收益
   - 但 Freely 当前已对其直连更熟，若只得到“又多一层 adapter”则收益未必大
3. `cc-use-codex-cli`
   - 当前不适合做第一刀
   - nested capability、内外层会话与证据写回都更复杂

### 3. Future-Tool Speculative Candidate Pool

这组候选属于“外部生态里值得观察的未来新增工具”，当前只能作为 speculative pool，不应误读成 repo 内已冻结实现对象：

1. `OpenCode`
   - 适合作为“新增工具走 ACP”候选
   - 价值在于验证新工具是否能以 `adapter=acp` 低成本接入
   - 若其直连路径也容易做，可顺带验证“新增工具 direct/acp 二选一”
2. `Roo Code`
   - 适合作为“未来 editor-hosted agent”候选
   - 价值在于验证 ACP 是否让新增 agent 比直连更容易接入

### 4. What First Prototype Should Prove

首个 prototype 最该证明的不是“ACP 很先进”，而是：

- 一个已存在 direct 工具确实可以通过配置切到 ACP 并工作
- 一个新增工具确实可以按配置选择 `direct` 或 `acp`
- Freely 不需要为 ACP 另起一套 continuity / recovery / governance 栈
- adapter 复杂度真实下降，而不是从 launcher 挪到 bridge

## Prototype Implementation Guidance

如果后续要把这条预研 materialize 成 issue，建议实现顺序固定为：

### 1. Phase 1: Extract Adapter Axis

- 先在 runtime 里把 `tool` 与 `adapter` 两个维度分开
- 不要求立刻让所有工具支持 `acp`
- 先让已有 `direct` path 继续原样可用

最小目标：

- 单个工具配置里可以表达 `adapter=direct`
- runtime 内部不再把“工具名”和“接入方式”完全写死成同一个维度

### 2. Phase 2: Add One ACP Path

- 只为一个最合适的 prototype target 增加 `adapter=acp`
- 复用同一套 tool selection / continuity / recovery 流程
- 不另起第二套 ACP-only lifecycle

最小目标：

- 至少一个现有或新增工具能通过 `acp` 跑通最小任务
- 出现失败时可以明确 fallback 或报出 adapter-specific reason

### 3. Phase 3: Validate Dual-Path Behavior

- 验证 `direct`
- 验证 `acp`
- 若工具支持两者，再验证 `prefer_acp_fallback_direct`

最小目标：

- adapter 切换不会破坏 continuity / recovery evidence
- runtime/status 不会因为 adapter 不同而分叉成两套真相面

### 4. Phase 4: Judge Go/No-Go

- 若 ACP 只是把复杂度从 launcher 挪到 bridge，则停在 optional research
- 若 ACP 真实降低新增工具接入成本，再考虑扩大采用面

## 收益清单

### 1. 新工具接入成本下降

这是 ACP 最直接、也最现实的收益。

如果未来 Freely 要继续接更多 code agent，例如：

- `OpenCode`
- `Roo Code` 或其他 VS Code / editor-side agent
- 新的 CLI-native coding agent
- 新的 IDE-hosted coding agent

那么当前做法通常需要逐个补：

- launcher 参数
- session / resume 语义
- permission 模型
- tool-call 解析
- 日志/流式输出解析
- continuity 证据桥接

若这些工具能直接说 ACP，Freely 就更接近：

- 复用同一套 client connection
- 复用同一套 session lifecycle
- 复用同一套 tool call / permission / streaming update 解析

这会显著降低“每来一个新 agent 就重新造半套 adapter”的成本。

### 2. 多工具接入更可组合

当前 Freely 已经能管多个工具，但组合方式仍偏工具特化。

若 ACP 落成 adapter 层：

- Freely 更容易把“新增工具”看成 registry / capability 扩展，而不是 launcher 特例
- 更容易按 capability 选 agent，而不是按手写 profile 选 agent
- 更容易在一个统一 schema 下比较 agent 的 session/list/load/tool support

### 3. 会话消息面统一

对 Freely 来说，这会减少两类复杂度：

- 不同工具各自的 update / progress / tool-use parsing
- 不同工具各自的 permission / interrupt / session state 处理

这对 runtime、status、debug、observability 都有长期收益。

### 4. 统一权限消息面，便于后续自动批准 broker

ACP 不会自动给出 Freely 需要的批准制度，但它会把 permission message 统一出来。

这意味着未来若 Freely 要做：

- risk-aware approval planner
- autonomous approval council
- 按危险度决定几个 subagent 复核

那么 ACP 至少能提供一个更整齐的“权限事件入口”。

### 5. 更容易把 Freely 做成真正的 agent orchestrator

现在 Freely 已经在做这件事，但 adapter 层还不够统一。

若 ACP 适配成功，Freely 的定位会更清晰：

- Freely = autonomy runtime / governance orchestrator
- external tools = ACP agents or ACP-bridged agents

这有利于未来把外部 agent 的接入从“经验型脚本支持”升级成“正式能力面”。

### 6. 更容易接有 UI 的宿主型工具

这里的收益不是“控制 UI”，而是：

- 若某个有 UI 的工具本身能作为 ACP agent 暴露
- Freely 就不必去模拟操作它的界面
- 而是把它当作标准 agent endpoint 接进来

这对 IDE-hosted agent 特别重要，因为它避免 Freely 走脆弱的 GUI automation 路线。

### 7. 降低 vendor lock-in

如果 Freely 和外部 agent 的边界更标准化：

- runtime 对某个单一工具的绑死程度会下降
- 替换或增加新 agent 的成本更可控
- 未来 agent 生态变化时，Freely 更容易继续演进

## 成本与劣势

### 1. 不能替代 Freely 当前最有价值的治理层

这是最大的边界。

ACP 即使接入成功，也不能替代：

- three-loop routing
- milestone / issue / progress / recovery truth
- worktree / branch governance
- fresh-with-handoff
- context/rate-limit rotation
- dispatch_priority / parallel_safe / write_scope

所以 ACP 不是“用了就能显著简化 Freely 整体架构”，它只能简化其中一层。

### 2. Bridge 成本可能很高

现实里很多工具并不会原生说 ACP。

那就意味着 Freely 要自己维护 bridge，把每个工具的：

- session
- permission
- streaming output
- tool call
- file/terminal semantics

翻译成 ACP。

如果 bridge 只是把当前复杂度从 launcher 挪到 adapter，收益会被吞掉。

### 3. 弱工具不会因为包一层 ACP 就自动变强

例如某个工具本来就没有：

- explicit resume target
- 稳定 session list/load
- 明确 tool-call event
- 可追踪证据路径

那 ACP bridge 最多只是统一外观，不能补真实能力。

### 4. `cc-use-codex-cli` 这类嵌套 agent 形态很难优雅映射

Freely 当前已经有：

- 外层 Claude session
- 内层 Codex thread
- 两层 jsonl / debug / tool evidence

这类 profile 不是“单 client 对单 agent”的简单形状。

若 ACP 建模不够细，容易出现：

- canonical session 到底算谁
- nested tool evidence 怎么保留
- continuation 应该接续哪一层

这些问题如果没先冻结，会让 ACP 方案反而更混乱。

### 5. File system / terminal ownership 需要重新切边界

ACP 倾向于：

- agent 通过 client callback 读写文件、申请 terminal

Freely 当前更倾向于：

- runtime 直接把 agent 放到 worktree 环境里执行

一旦改成 ACP，就要重判：

- fs 操作由谁托管
- terminal 由谁拥有
- sandbox 与 cwd 谁说了算

这不是免费迁移。

### 6. Token 和性能收益可能没有直觉上那么大

ACP 最大收益是统一接口，不是减少模型推理量。

所以它不一定会明显降低：

- 单次任务 token
- agent 真正的 reasoning 开销
- 长任务的上下文负担

尤其如果 Freely 还要保留大量治理 prompt，短期几乎不一定省 token。

### 7. 会引入新的调试层

当前问题多半还在：

- launcher 参数
- session evidence
- runtime state

若引入 ACP，会多一层：

- ACP transport
- ACP bridge
- ACP capability negotiation
- ACP message translation

如果 observability 没同步补齐，排障会更难。

### 8. 可能把当前“可脚本化直连”的简单路径变复杂

Freely 现在的一个优势是：

- 对 CLI-native tool 可以直接启动
- 行为简单，可脚本化，可本地验证

ACP 若引入过早，可能把本来直接能跑的路径，变成先过一层 protocol runtime。

对原生 CLI 工具来说，这未必总是净收益。

## 收益与成本的总结判断

### 适合采用 ACP 的信号

- 新增 agent 的速度越来越快
- 每个 agent 的 adapter 代码都在重复 session/permission/update 逻辑
- 至少有一批目标工具能原生说 ACP，或 bridge 成本足够低
- Freely 想把自己正式定位成“统一 agent orchestrator”

### 暂不值得重投入 ACP 的信号

- 当前主要瓶颈仍是治理，不是接入
- 绝大多数目标工具都需要自建 bridge
- 最常用路径仍是 CLI-native direct launch
- ACP 不能减少当前最痛的 recovery / continuity / governance 复杂度

### E. 下一步研究应缩成字段级 mapping，而不是继续抽象讨论

最有价值的下一跳是补一张矩阵：

- Freely current field
- current owner
- current carrier (`env` / `log` / `jsonl` / artifact)
- ACP equivalent
- gap
- keep in Freely or move to adapter

没有这张表，就无法判断 ACP 是“能省真实 adapter 成本”，还是“只是换一层名词”。

## 初始字段映射草表

下表先只做第一版粗映射，目标不是宣称已经完全兼容，而是冻结“哪里像、哪里不像”。

| Freely current field / behavior | 当前载体 | ACP 近似面 | 初步判断 |
| --- | --- | --- | --- |
| `tool` / `model` | runtime config / launcher args | `initialize` + agent identity + session setup inputs | 可映射，但 agent identity 与 model 选择未必总由 ACP 同一层负责 |
| `mode=auto/step` | runtime config | session mode / session config option | 可映射；Freely 的 `auto` 仍需额外本地自动批准策略 |
| `reasoning_effort` | runtime config / launcher args | session config option 或 agent-specific option | 可能映射，但更像 agent-specific 扩展 |
| `launch_kind=fresh/resume/fresh_with_handoff` | runtime decision | `session/new` / `session/load` | `fresh`/`resume` 易映射；`fresh_with_handoff` 属于 Freely 特有 continuity 策略 |
| `tool_session_id` / `claude_session_id` | runtime state | `sessionId` | 强映射 |
| `tool_resume_target` | runtime state | `session/load` input | 强映射 |
| `jsonl_path` | runtime state / continuity evidence | 无直接一等字段 | ACP 不覆盖本地证据文件路径；应继续留在 Freely |
| `session/prompt` 等价 prompt turn | prompt file + launcher stdin | `session/prompt` | 强映射 |
| tool progress / streamed output | cycle log + tool-specific parser | `session/update` | ACP 明显更优，适合替代异构日志解析 |
| permission ask / allow / reject | tool-specific CLI flags + local policy | `session/request_permission` | ACP 更统一，但“是否免交互自动批准”仍归 Freely |
| `approval_policy` | tool capability policy | permission options / session mode / config | 只能部分映射；Freely 仍需本地批准制度 |
| `sandbox` / `cwd_mode` / project root | capability policy | session lifecycle `cwd`，以及新增 additional workspace roots | 有映射空间；Freely 当前 `cwd + sandbox` 边界更工程化 |
| `tool_capabilities` / `tool_policy` | runtime config | agent capabilities + config + extensibility `_meta` | 可部分映射，但 Freely 的 profile 粒度更高 |
| `cc-use-codex-cli` nested capability | top-level tool profile | MCP-over-ACP / nested tool channel | ACP 有潜力，但需要 bridge；不是现成等价 |
| `context_ratio` / `context_compacted` | jsonl extraction | 无直接一等字段 | 继续留在 Freely runtime |
| rate-limit usage / reset time | jsonl extraction / runtime state | 无直接一等字段 | 继续留在 Freely runtime |
| `dispatch_priority` / `parallel_safe` / `write_scope` | manager continuity / worker prompts | 无直接等价 | 明确属于 Freely orchestration，不下沉到 ACP |
| `candidate/issue/progress/recovery` continuity | canonical artifacts | 无直接等价 | 明确属于 Freely 长期记忆与治理层 |

### 由这张表得到的第一结论

ACP 最有价值的吸收面是：

- `session/new`
- `session/load`
- `session/prompt`
- `session/update`
- `session/request_permission`
- session mode / config
- MCP-over-ACP 或类似 nested capability channel

Freely 必须继续自持的面是：

- `fresh_with_handoff`
- `jsonl_path` / cycle log / evidence extraction
- context / token / rate-limit rotation
- risk-aware approval
- dispatch / lane orchestration
- canonical lifecycle artifacts

因此，如果 Freely 未来采用 ACP，最合理的姿势不是“替换 runtime”，而是：

- 用 ACP 收敛 agent communication plane
- 保留 Freely 自己的 continuity / governance / orchestration plane

## 建议下一跳

- 先把这条研究保持在 pre-brainstorm，不直接 materialize 为 IBM issue
- 继续收敛一张“Freely adapter contract vs ACP contract”字段表
- 再决定 ACP 是否只做可选 adapter，还是值得进入 runtime 主路径

## 关联真源

- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/system/workspace/skills/recovery-subagent-governance/SKILL.md`
