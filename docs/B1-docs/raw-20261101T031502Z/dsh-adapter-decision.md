---
analysis_id: DSH-20261101T231000Z
phase_state: in_progress
topic: DSH adapter 还是 @freely/dsh-freely 插件
created_at: 2026-11-01
---

# DSH 集成：做 adapter 会阉割多少？反向插件是否更对

## 0. 先给结论

**不建议现在做“DSH 作为 Freely harness”的 adapter。** 它会把 DSH 最有价值的运行时能力全部旁路，只留下一个 Session 执行器；同时 Freely 还要承担双宿主的所有权冲突。

如果一定要进入 DSH 生态，正确方向是反向的：**把 Freely 做成 `@freely/dsh-freely` 插件**，让 DSH 继续拥有 Router/Ticket/Thread/Attention，Freely 只提供 SDD/TDD/gates/worktree/PR/issue-sync 这些交付治理能力。

两条路的本质区别：

- **DSH adapter**：Freely 拥有 loop，DSH 只当执行器 → 阉割 DSH。
- **DSH 插件**：DSH 拥有 loop，Freely 只当治理工具 → 阉割 Freely 的调度层，但保留差异能力。

## 1. 方案 A：DSH 作为 Freely harness

### 1.1 技术上要做什么

- Freely 侧新增 HarnessPort adapter，启动一个 DSH Session/Agent。
- 由于 DSH 没有 ACP 服务端，需要：
  - DSH 插件/桥进程，接收 prompt、开 Session、回事件/usage；或
  - Freely 侧 Node bridge，用 DSH SDK 起 Session，再暴露 JSON-RPC 给 Python runtime。
- 还要解决：谁拥有 Ticket？谁拥有 Thread？谁处理 follow-up？

### 1.2 会阉割 DSH 的什么

| DSH 能力 | 在 adapter 模式下 | 损失 |
| --- | --- | --- |
| Router（准入/批量决策/对外统一） | Freely Manager 取代 | **全丢** |
| Trigger/Source/Eval/Decision | Freely scan/Manager 取代 | **全丢** |
| Ticket/Assignment/Stage | Freely issue/worktree 取代 | **全丢** |
| Thread/Subscription 直通 | Freely 无事件总线 | **全丢** |
| Report/Attention/ownership/handback | Freely A2A 粗粒度取代 | **大部分丢** |
| Mandate/Policy 版本 | Freely 文档/门禁取代 | **全丢** |
| Watchdog/恢复 | Freely supervisor 取代 | **全丢** |
| 单写 Store/Effect 队列 | Freely docs/DB/平台多源取代 | **全丢** |
| Panel/IM/health | Freely CLI/chat 取代 | **大部分丢** |
| Session/模型执行 | 保留 | 保留 |

也就是说：**adapter 只保留了 DSH 的“Session 执行”这一层，丢掉了 DSH 之所以是 Super-agent 的 Router/事件/授权/交接/注意力。** 这不是“集成 DSH”，是“把 DSH 当 Claude Code 用”。

### 1.3 会得到什么

- DSH 的模型/preset/tool 生态（如果 Session 能独立跑）。
- 但 Freely 已经有 ACP 四家 CLI；DSH 的边际收益主要是“DSH 模型/工具”，不是“Super-agent 架构”。

### 1.4 成本

- 双宿主生命周期、版本锁定、Node/Python 桥、Session 事件映射。
- 所有权冲突：DSH 的 Router/Ticket 与 Freely Manager/issue 不能同时拥有。
- 能力探测/降级复杂：DSH 没有 ACP capability 契约。

## 2. 方案 B：`@freely/dsh-freely` 插件

### 2.1 角色反转

- DSH 继续拥有：Router、Trigger、Thread、Ticket、Mandate、Attention、Watchdog、Store、Panel。
- Freely 作为插件提供：
  - `freely_gate`：跑 governance/pretests/PR/merge gate。
  - `freely_worktree`：创建/回收 dev/test worktree。
  - `freely_tdd`：生成/校验 pre-tests、RED/GREEN 证据。
  - `freely_issue_sync`：GitHub/Gitee 双平台 issue/PR 同步。
  - `freely_spec`：B1/B2 模板与 SDD 文档校验。
- Freely 不再拥有 Manager/Worker/Reviewer/A2A/scan/three-loop；这些由 DSH 的 Router/Worker 取代。

### 2.2 保留/丢失的 Freely 能力

| Freely 能力 | 插件模式 | 说明 |
| --- | --- | --- |
| SDD/B1/B2 文档 | 保留 | 作为工具/模板/校验器 |
| TDD/pre-tests/RED-GREEN | 保留 | 作为 gate/tool |
| 独立 Reviewer | 部分保留 | 可作为 DSH 的一个 review tool/agent，但 DSH 没有内建 Reviewer 角色 |
| worktree/test lane | 保留 | 作为工具 |
| PR/merge/issue-sync | 保留 | 作为工具 |
| Manager/auto-loop | 丢失 | DSH Router 取代 |
| Worker/Reviewer A2A | 丢失 | DSH Ticket/Worker 取代 |
| scan/阶段路由 | 丢失 | DSH Trigger/Ticket 取代 |
| 多项目 fleet | 丢失/需重做 | DSH 单仓 |

结论：**插件模式保留 Freely 的“交付治理差异”，丢掉“调度差异”。** 这比 adapter 模式保留的东西更值钱，因为 Freely 的差异化本来就在 SDD/TDD/gates，而不是“又一个 Router”。

### 2.3 成本

- 需要 DSH 插件 API/Cordis bundle 开发；版本跟随 DSH。
- Freely 的 gate 要适配 DSH 的 Ticket/Workspace 模型。
- Freely 不能再声称“完整 three-loop”；在 DSH 内它是治理插件，不是项目所有者。
- 多项目/跨仓仍受 DSH 单仓限制。

### 2.4 插件 API 的现实：DSH 不是通用“工具插件”宿主

读 `docs/007-architecture.md` 和 `docs/008-cookbook.md` 后要修正一个预期：

- DSH 的插件入口主要是 **Source 插件**（`SourceKind` + `SourceContext` + `orchestrator` service），负责把外部消息变成 Trigger。
- 主 Session 的工具集是 `src/app/tools/main.ts` 内建的 14 个工具；没有看到“第三方插件任意注册工具”的公开接口。
- 因此 `@freely/dsh-freely` 最现实的形态不是“把 gates 注册成 DSH tools”，而是：
  1. **Source 插件**：把 Freely 的 issue/PR/CI/文档事件变成 DSH Trigger；
  2. **skill/prompt**：告诉 DSH Worker 用 `freely` CLI 跑 B1/B2、gate、worktree、TDD；
  3. **bash 调用**：DSH Worker 本来就有 `bash` 工具，可以直接执行 `freely ...`，用 exit code 卡门禁。
- 这能保留 DSH 的 Router/Ticket/Thread/Attention，也能让 Freely 的 gate/worktree/TDD 以 CLI 形式落地；但“Freely 作为一等工具”做不到，除非改 DSH core。

这进一步说明：**插件路线的可行形态是“Source + skill + CLI”，不是“Freely 全套能力原样插件化”。** 如果目标是“Freely 能力全部落地”，插件路线也会阉割掉 Freely 的 Manager/A2A/three-loop；只是它保留的是 DSH 的运行时，而不是把 DSH 阉割成执行器。

## 3. 方案 C：不做 DSH 集成

- 保持 ACP 四家 CLI；DSH 只作为“另一个可参考的架构”，不进入代码。
- 成本最低；不丢失 Freely 的 loop 所有权。
- 代价：放弃 DSH 生态/模型/preset 的边际收益。

## 4. 判定矩阵

| 目标 | A: DSH adapter | B: Freely 插件 | C: 不做 |
| --- | --- | --- | --- |
| 用 DSH 模型/Session | 可以 | 可以（DSH 内） | 不可以 |
| 保留 Super-agent 运行时 | **丢大部分** | 保留 | N/A |
| 保留 Freely 交付治理 | 保留 | 保留 | 保留 |
| 保留 Freely 调度/three-loop | 保留 | **丢** | 保留 |
| 双宿主冲突 | 高 | 中 | 无 |
| 工程成本 | 高 | 中高 | 低 |
| 战略价值 | 低（把 DSH 当 CLI） | 高（Freely 治理进入 DSH） | 中 |

## 5. 建议

1. **现在不做方案 A。** 它不是“DSH 集成”，是把 DSH 阉割成执行器；投入大、战略价值低。
2. **如果要做 DSH，先做方案 B 的 spike**：`@freely/dsh-freely` 只暴露 3 个工具（gate、worktree、tdd），在 DSH 内跑一个真实 Ticket，测量：
   - DSH 的 Router/Ticket/Attention 是否真的能承接 Freely 的交付语义；
   - Freely 的 gate 是否能独立于 Manager/three-loop 工作；
   - 哪些 Freely 能力必须依赖 A2A/scan，无法插件化。
3. **方案 C 是默认**：除非 DSH 生态有明确用户/模型收益，否则不值得为它维护双宿主。
4. 如果 spike 证明 DSH 的 Router/Ticket 不能承接 Freely 的 B1/B2/TDD，那么答案不是“写 adapter”，而是“不集成”。

## 6. 何时重新评估

**方案 A（DSH 作为 harness）只在以下条件同时满足时重开：**

1. DSH 暴露稳定的 Session API（开/发/停/usage/stopReason），或提供 ACP 服务端；
2. DSH 明确允许 Freely 拥有 Router/Ticket，不要求双写；
3. 有真实用户需求“必须用 DSH 模型/preset”，而不是“架构看起来更强”；
4. 能接受 DSH 的 Router/Thread/Mandate 被旁路。

**方案 B（插件）的 spike 验收：**

1. 在 DSH 内跑一个真实 Ticket，从 issue 到 PR；
2. 用 `freely` CLI 卡住至少一个 gate（证明 exit code 能阻断）；
3. DSH 的 Thread/Attention 能承接 Freely 的阶段消息；
4. 测量“Freely 能力落地比例”和“DSH 上下文成本”，再决定是否产品化。

没有这组证据，不做全量插件，更不做 adapter。

## 7. 未解

- DSH 插件 API 是否能暴露同步工具调用（gate 需要阻塞等待）？
- DSH Ticket 能否承载 B1/B2 两级文档，还是需要外挂 docs？
- DSH 的 Worker 能否跑 test-pre-merge 这种环境隔离？
- 插件模式下 Reviewer 的独立性如何保证？
- 双平台 issue/PR sync 在 DSH 单仓模型下是否仍成立？
