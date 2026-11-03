---
b1_id: B1-20261101T140415Z
phase_state: completed
source_raw: raw-20261101T140415Z
source_url: https://github.com/chatterzhao/freely/issues/4117
produced_candidate: C-20261101T140415Z-A, C-20261101T140415Z-B
created_at: 2026-11-02
---

# B1_IBM: 交接运行时可靠性（Super-agent 研究收口）

> 研究包入口：[`research/super-agent/README.md`](research/super-agent/README.md)。
> 前序对账：[`predecessor-reconciliation.md`](predecessor-reconciliation.md)。
> 运行层图：[`research/architecture/freely-runtime-architecture.html`](research/architecture/freely-runtime-architecture.html)、[`research/architecture/super-agent-handoff-loop.html`](research/architecture/super-agent-handoff-loop.html)。

## 1. Input

- raw issue：`raw-20261101T140415Z`（GitHub #4117 / Gitee IKS3MM）。
- 原文：DeepSeek 产品部《Super-agent 设计探索》，2026-10-31；本地归档 `research/super-agent/source.html` + 15 图。
- 原型：`deepseek-ai/dsh-superagent-prototype` @ `6337fc8`；文档 `000-008` + `src/` 已逐条核对。
- Freely 侧：`CONSTITUTION`、`LAWS`、`PROJECT_INTENT`、`docs/system/workspace/{agents,scripts,skills}`、develop `ceaa8c1f2`。
- 前序：`raw-20261101T031502Z` 六条 candidate 与 B2 交付（见对账文档）。

## 2. Problem

第一轮研究把“交接”当成领域模型问题（`Subscription`/`handback`），产出了 `handoff_store` 三张表；但 develop 上 `HandoffStore` 零生产调用，交接仍然靠 `a2a-exit --summary` + `watchdog_sse` 的一次性 `session/prompt`。所以真正的问题不是“模型不够干净”，而是：

> **一次交接在运行时没有信封、没有队列、没有 owner；两个实现缺陷还会让路由线程直接抛异常并丢事件。**

表现：交接时好时坏；日志只有一行 `SSE error`；同一 raw 的消息可能落到不同席位；接收方必须重新查库才能知道发生了什么。

## 3. Boundary

- 只修“交接能不能可靠到达”，不改 A2A 状态机语义（`submitted/working/input-required/completed/failed/canceled` 保持）。
- 不引入 `Ticket/Assignment` 全量领域模型；不重命名 `worker_NN`；不做面板。
- 不在本 candidate 实现持久 outbox（留给 C-B），但修复必须让 outbox 将来能挂在这条链上。
- 研究文档与图作为 B1 证据随分支提交，不单独设 candidate。

## 4. Discovery

### 4.1 两轮研究的缺口

第一轮来源是二手报道、原型只做静态阅读（decision note 自述），所以它只能得到概念级结论；本轮补了原文与原型代码，才发现“文章主张 / 原型实现 / Freely 现状”三层长期被混用。详见对账文档。

### 4.2 交接链的三个结构性缺口

1. **载荷**：`a2a-exit` 只有 `--summary/--next/--evidence` 三个自由字符串；`process_ai_reply` 用正则抓 JSON block；`STATE_ALIASES` 堆了几十个同义词。接收方拿到的是“一段话”，不是“一件事”。
2. **传输**：`a2a_task prompt` 只写库，投递依赖活跃 SSE；`/tasks/stream` 是内存 `asyncio.Queue`，断线不重放；`_handle_message_delivery` 失败只打日志。没有 outbox、没有 receipt、没有“投递未达”状态。
3. **身份**：`agent_next_free(role, pool)` 从 `worker_01..10` 选任意空闲席位；席位跨任务复用。`worker_NN` 实际绑定的是 `agent-table.toml` 的凭证槽，不是 raw issue。

### 4.3 两个可复现的实现缺陷（P0）

- `agent_working._do_new` 的函数签名没有 `message`，函数体却调用 `_prompt_after_connect(..., message)`；同函数 `sys` 也未在模块级导入。由 `3e82cfee4` 引入，develop 现存。触发面：**跨工具交接 / resume 失败 / 无 manager 会话**。
- 后果链：`_handle_sse_event` 无 `try/except` → 异常上抛 → `watchdog_run` 记 `SSE error` 后重连（1s→30s 退避）→ 期间 SSE 不重放 → 交接静默丢失。
- 上游还有：`_check_agent_liveness` 用 `pgrep -f <session_id>` 判活，误标 DEAD 后清空 session 绑定；下一次交接找不到会话 → 走 `_do_new` → 命中上面的异常。两个缺陷串联，解释了“时好时坏”。

### 4.4 Super-agent 可借鉴的部分（只取运行时件）

- `worker_report` / `worker_attention`：固定信封，原始 Trigger 转发，单问题原样转发。
- `delivery` / `relay` / `notice` / `reply`：持久 effect 队列，顺序 + 退避 + 健康项 + `Later`（无 slot 不算失败）。
- `Ticket` 自持 `workerSessionId`，`Assignment` 只是绑定；handback 一次，`queued:false` 表示别人还持有。
- 不借鉴：存算分离、外部 LLM Watchdog、投机执行、完整 Mandate、A2A。

## 5. Options

| 选项 | 内容 | 代价 | 能解决什么 |
|---|---|---|---|
| **A（选中）** | 修 `_do_new` 未定义变量 + 把 liveness 换成 `session/ping`；补回归测试 | 小；两个文件 + 测试 | 消除“随机丢交接”的最大来源；让后续协议有可用的底座 |
| B | A + 交接信封 + 持久 outbox + owner 绑定 | 中；新增表/队列/消费循环，跨 3-4 个模块 | 完整解决载荷/传输/身份；但改动面大，需独立 B2 |
| C | 重做 `Ticket/Assignment` 领域模型 | 大；迁移 A2A 表与全部调用方 | 架构最干净；超出本 raw，且会破坏现有 A2A 兼容 |

## 6. Decision

- **先做 A**（`C-20261101T140415Z-A`，promoted）：两个缺陷是 B 的前置条件——不修掉，跨工具交接必抛，B 的端到端测试无法稳定跑。
- **B 单独立项**（`C-20261101T140415Z-B`，`needs_research`）：需要先在 B2 里定信封字段、outbox 状态机与 owner 规则，不在本轮实现。
- **C 不做**：与 `LAWS` 的兼容性要求冲突，收益不足以抵消迁移风险。

## 6.1 Scope 变更说明

raw 原文写“不实现 runtime 变更；研究完成后按 ADR 另开实现 issue”。B1 在核对 develop 代码时发现两个可复现缺陷（`_do_new` 未定义变量、`pgrep` 误判），按用户 2026-11-02 的指示（“做好一个可用的 freely”），将 `C-A` 收敛为最小运行时修复；`C-B` 仍只做研究，不实现。此变更在此显式记录，避免被读成偏离 raw。

## 7. 风险

- 修 `_do_new` 会改变“新建会话后是否立即收到首条消息”的行为；必须有测试证明 worker/reviewer 两种角色都能收到首条 handoff。
- 把 `pgrep` 换成 `session/ping` 会改变“DEAD”判定口径；必须保留 fail-closed：ping 失败时不发明会话，只标记需要恢复。
- 本 raw 的研究结论依赖原型 `6337fc8`；原型是 research prototype，不能把“原型有”当成“文章已证明”。
