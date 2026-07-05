# 预研头脑风暴：runtime-websocket-permission-denied-recovery-governance

## 背景

2026-04-04 在 canonical root `develop` 完成 push 后，对 root runtime 的重新拉起与监督暴露出一条新的运行时缺口：

- `freely start --project /Users/zhaoyu/Downloads/code/my-freely/freely` 首轮报 `manager watchdog did not become ready`
- `freely ensure-manager --project ... --watch` 随后确认 watchdog 已 running
- runtime 持续生成新的 `prompt-20260404-153503.txt`、`prompt-20260404-153521.txt`、`prompt-20260404-153556.txt`、`prompt-20260404-153611.txt`
- 但没有生成新的 manager continuity，最新 continuity 仍停在 `.freely/run/manager-continuity-20260404-143843.md`
- 两条新的 human chat intake 已 durable 写入 `.freely/intake/20260404-153515-*` 与 `.freely/intake/20260404-153535-*`，也被带进新 prompt，但 `meta.env` 仍停留在 `STATUS="new"`

这说明当前失败已经不是“插话入口不可见”，而是“插话可见但 runtime 未能完成 claim/continuity/dispatch 消费”。

继续监督后又补了三条关键证据：

- `develop` 已实际 push 到 `origin/develop`，因此当前阻塞已不再是 protected-branch push gate
- 在清掉大量历史孤儿 `freely start` / `manager-watchdog` / `ensure-*` 进程后，root runtime 能重新拉起单个 manager supervisor，并继续生成新 prompt
- 最新 `.freely/run/prompt-20260404-153936.txt` 已带入新的人类插话 `20260404-153908-*`，但该 intake 的 `meta.env` 仍停在 `STATUS="new"` / `CLAIMED_BY=""`

这把现场进一步缩窄为：prompt assembly 已恢复，但 supervision truth 仍停在 claim / continuity materialization 之前。

## 已确认事实

### 1. 当前主症状是执行期 websocket 连接被拒，而不是 manager watchdog 完全缺失

最新运行日志显示：

- `.freely/logs/runtime-events.log` 持续出现 `execution_network_transient`、`ai_exit_rc_1`、`restart_storm_pause`
- `.freely/logs/cycle-20260404-153521.log` 明确记录：
  - `failed to connect to websocket: IO error: Operation not permitted (os error 1)`
  - URL: `wss://chatgpt.com/backend-api/codex/responses`

因此 `manager watchdog did not become ready` 更像启动窗口里观察到的表象；真实主故障是 manager AI 进程起不来或起后立刻掉线，导致控制面持续 churn。

### 2. 现有 runtime 已经能把 chat intake durable 注入 prompt，但不能把它们消费进 continuity

当前现场同时满足：

- `.freely/intake/.../message.txt` 存在，说明 `freely chat` durable intake 入口正常
- `prompt-20260404-153503.txt`、`prompt-20260404-153521.txt`、`prompt-20260404-153556.txt`、`prompt-20260404-153611.txt` 都能看到这两条新 intake
- 但对应 `meta.env` 仍是：
  - `STATUS="new"`
  - `CLAIMED_BY=""`
  - `ABSORPTION_TARGET=""`
- 且没有新的 manager continuity 落盘

结论：当前链路不是 intake durability 缺失，而是 manager runtime 无法完成 consume/claim/absorb 回写。

### 2A. 最新证据显示“新插话可见于 prompt，但仍未被 claim”

继续监督后又确认：

- `.freely/intake/20260404-153908-supervisor-interruption-canonica/message.txt` 已被 durable 写入
- 同一条消息已出现在 `.freely/run/prompt-20260404-153936.txt`
- 但 `.freely/intake/20260404-153908-supervisor-interruption-canonica/meta.env` 仍是：
  - `STATUS="new"`
  - `CLAIMED_BY=""`
  - `ABSORPTION_TARGET=""`
- 最新 manager continuity 仍停在 `.freely/run/manager-continuity-20260404-143843.md`

因此当前 contract gap 已能精确表达为：

1. intake durability 正常
2. prompt assembly 正常
3. manager continuity / intake claim writeback 未收敛

### 3. 这不是 GitHub issue 自动化功能已经存在但没被正确调用

现有证据仍支持：

- GitHub issue create/sync 相关能力目前只停留在 `docs/B1-docs/raw-20260403T110000Z/*`
- 当前没有已 materialize 的 runnable `scan/create/sync/close` 能力面

因此这轮监督里不能把“没有自动创建 GitHub issue”误判成 runtime 消费错误；真实情况是该能力本来就还在预研。

### 4. 现有 completed owner 只能提供边界，不能直接吸收本次现象

- `global-ai-account-watchdog-and-manager-bootstrap` 已完成，主要收敛 slot sweep / manager bootstrap / account recovery contract
- `watchdog-restart-storm-and-process-churn-governance` 已完成，主要提供 churn signal 与低频观察面
- `runtime-network-failure-taxonomy-and-bounded-recovery-governance` 已完成，主要收敛 execution-time network taxonomy 与 bounded retry/cooldown

但当前现场仍暴露出一个新的组合性问题：

- execution-time websocket failure 仍会把 system 带进 prompt-only churn
- manager prompt 可以持续刷新
- 但 intake claim / continuity / dispatch 产物没有 materialize

这已经超出“只是把网络故障分桶”本身，更接近“runtime 在 network-local failure 下如何保持监督闭环与 intake absorption truth”的 follow-on governance。

### 5. 最新证据还叠加了 slot-switch 和进程容量层

本轮继续监督时新增观察到：

- `.freely/logs/cycle-20260404-153936.log` 首行就是：
  - `[WARN] codex slot switch is already in progress (owner_pid=97028); waiting before codex launch`
- root 仓库一度存在约 600+ repo-owned runtime 相关进程，包含历史 `freely start`、`manager-watchdog`、`ensure-manager --watch`、`ensure-interruption-dispatch --watch`
- 这些孤儿进程会把现场推到 `fork: Resource temporarily unavailable`，并放大 prompt-only churn

这说明当前 follow-on 不能只看“websocket permission denied”字符串，还要判断：

- slot-switch busy 是否应进入同一 bounded blocked state
- orphan process storm 是否属于同一 runtime-owned recovery family
- intake/continuity blocked truth 应由哪一层统一 materialize

## 初步边界判断

更窄且可执行的问题定义应是：

1. 当 manager AI 因 websocket / permission-denied 类执行期网络故障无法建立会话时
2. runtime 是否应该继续不断刷新 prompt
3. 还是应进入一个更强的 bounded hold / circuit-open 状态
4. 并把 pending intake 显式标记为 `blocked_by_runtime_network_failure`、`awaiting_recovery` 或同类 truth
5. 避免出现“intake 永远是 new，但 prompt 一直重发”的假活跃状态

## 候选方向

### 方向 A：把 websocket permission-denied 归入现有 execution-time network taxonomy 的新证据族

优点：
- 和 `execution_network_transient` / `execution_network_persistent` 属于同一失败面
- 不需要新造“网络故障”大类

风险：
- 仅靠 taxonomy 扩词典，不一定能收住 intake/continuity 消费缺失
- 可能继续把真正的 supervision truth gap 藏在“网络错误分类已存在”后面

### 方向 B：新增一个 runtime-owned follow-on，专门收口 `prompt-only churn without continuity/intake claim`

优点：
- 问题边界直接对准当前 dogfood 现象
- 能把 intake absorption truth、manager continuity materialization、network-local hold 三者一起看

风险：
- 需要谨慎避免和已完成的 restart-storm / network-taxonomy issue 重复

## 当前判断

倾向方向 B。

原因：当前要修的不是“再多识别一种网络错误字符串”，而是：

- network-local failure 已经被观察到
- restart storm signal 也已经观察到
- 但系统仍没有把 supervisor truth 从“不断重发 prompt”收束到“明确 blocked、保留 pending intake、等待恢复”

这更像 supervision contract 的 follow-on，而不是单纯 taxonomy 增补。

补充判断：

- `global-ai-account-watchdog-and-manager-bootstrap` 与 `watchdog-restart-storm-and-process-churn-governance` 都已 completed，只能提供边界，不能直接作为这轮新现象的 owner
- 当前 `1545` lane 继续保持 pre-brainstorm 是合理的，因为还没完全冻结 websocket permission denied、slot-switch busy、resource exhaustion 三者是否共享一个 recovery owner

## 下一步研究问题

1. `Operation not permitted` 应被归到 `execution_network_transient`、`execution_network_persistent`，还是新的不可恢复本地边界类 reason？
2. 当 manager runtime 无法消费 intake 时，`meta.env` 应如何表达 blocked truth，避免永远停在 `new`？
3. prompt 重发与 continuity 缺失之间，哪个是真正的 bounded stop 条件？
4. 现有 restart-storm pause 之后，为什么仍会继续生成新 prompt 而没有新的 continuity？
5. 这条能力应吸收到哪一个新的 lifecycle：
   - runtime network follow-on
   - manager supervision / intake absorption follow-on
   - 还是一个更窄的 manager continuity materialization regression
6. `slot switch already in progress` 与 websocket `Operation not permitted` 是否应共享同一个 blocked-intake / blocked-continuity truth surface？
7. 清掉历史孤儿 runtime 进程后，为什么 prompt 仍能前进而 claim/continuity 不前进？
