---
analysis_id: PLUGIN-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# `@freely/dsh-freely` 插件应该长什么样

## 0. 目标与边界

目标：**Freely 保留除 agent harness 外的全部能力；agent harness 完全使用 DSH。**

这里的“全部能力”指：

- Manager / Worker / Reviewer 三个角色与它们的循环；
- B1/B2、SDD/TDD、scan、A2A/handoff、gates、worktree、PR/issue sync；
- 人插话、attention、收口、审计。

“使用 DSH 做 harness”指：

- DSH 负责 Session/Agent、模型、preset、工具、权限、subagent、usage、持久化；
- 不再走 ACP 子进程，不再维护 `run-acp-prompt.py` / `acp-bridge.py` 的 ACP 适配层。

**不采用**“DSH 拥有 Router/Ticket，Freely 只做 gates/TDD 工具”的治理插件形态——那会丢掉 Freely 的 Manager/A2A/loops，不是“全部能力”。

## 1. 两种插件形态，先分清

| 形态 | 谁拥有 loop | 保留 Freely 能力 | 丢失 |
| --- | --- | --- | --- |
| A. Freely-host 插件（本文推荐） | Freely | Manager/Worker/Reviewer、A2A、scan、gates、worktree、PR | DSH 的 Router/Ticket/Thread 编排 |
| B. DSH-host 治理插件 | DSH | gates、TDD、worktree、issue sync | Freely 的 Manager/Worker/Reviewer、A2A、scan、loops |

`@freely/dsh-freely` 如果目标是“除 harness 外全部释放”，必须是 **A**；B 是另一个产品。

## 2. 总体架构

```
DeepSeek Harness process (Cordis)
┌─────────────────────────────────────────────────────────────┐
│  @freely/dsh-freely plugin                                  │
│                                                             │
│  FreelyHost service                                         │
│    ├─ DshHarnessAdapter  ── uses agents/sessionController   │
│    ├─ FreelyBridgeServer ── Unix socket JSON-RPC            │
│    ├─ FreelyTools        ── freely_gate / worktree / tdd    │
│    ├─ FreelySkills       ── B1/B2/dev/test/review skills    │
│    └─ FreelyPanel        ── client plugin (optional)        │
│                                                             │
│  DSH services: agents, sessionController, sessionPersistence│
│  workspaceRegistry, permissionPresets, tools, systemPrompt, │
│  skills, webServer, llm, subprocess                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ Unix socket / JSON-RPC
┌──────────────────────────▼──────────────────────────────────┐
│  Freely runtime (Python, child process)                     │
│  Manager / Worker / Reviewer, A2A, scan, gates, worktree,   │
│  PR / issue sync, docs                                      │
│  replaces run-acp-prompt.py / acp-bridge.py with bridge RPC │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 为什么保留 Python runtime

Freely 的 Manager/scan/gates/A2A/worktree 是 20K 行 bash/Python，短期内重写成 TypeScript 不现实，也会引入大量行为回归。插件只做 **harness provider + bridge + panel**；Python runtime 继续拥有 loop。这样“全部非 harness 能力”原样保留，只替换 harness 调用点。

### 2.2 不加载 `dsh-superagent`

B2 只加载 `@freely/dsh-freely`，**不加载 `dsh-superagent`**。这样 DSH 只提供核心 harness services（agents/sessionController/tools/skills/...），不会同时出现 DSH Router/Ticket 与 Freely Manager/A2A 两套 loop。

### 2.3 Plugin 注入的服务

参考 `dsh-superagent` 的主插件：

```ts
export const inject = [
  'agents', 'sessionController', 'sessionPersistence',
  'workspaceRegistry', 'permissionPresets', 'tools',
  'systemPrompt', 'skills', 'webServer', 'llm', 'subprocess',
]
```

- `sessionController`：create/resolve/prompt/stop Session。
- `agents`：agent 事件、状态、usage。
- `tools`：注册 Freely 原生工具（可选；也可让 Worker 用 `bash` 调 `freely` CLI）。
- `skills` / `systemPrompt`：注入 Freely 角色定义与 workflow skill。
- `permissionPresets`：注册 `freely-manager` / `freely-worker` / `freely-reviewer` preset。
- `webServer`：bridge/health/panel endpoint。
- `subprocess`：启动/监督 Python runtime。

> 这些服务是 DSH 主插件实际注入的；第三方插件能否稳定拿到，需要 spike 验证。若不允许，退化为“Source + skill + CLI”，但那就不是 A 形态。

## 2.4 Spike 证据（2026-11-01）

已在本地 DSH 原型上做**静态插件契约 spike**，不是完整 runtime E2E：

- DSH 原型 `pnpm install --offline` + `pnpm typecheck` 通过。
- 最小插件 `research/ops/spike/dsh-plugin-contract.ts` 在 DSH 类型环境下编译通过：

```
pnpm exec tsc --ignoreConfig --noEmit --moduleResolution bundler --module esnext \
  --target es2022 --skipLibCheck --strict --types node spike-freely-plugin.ts
```

- 编译验证了：`inject` 的服务名（`sessionController`/`workspaceRegistry` 等）存在；`resolveAgent`/`create({sessionId, workspaceId, agentPreset})` 可用；插件可以以 `name`/`inject`/`apply` 形态被 DSH 加载。
- DSH `Sessions.ensure` 的真实实现是：`sessionController.resolveAgent` → 未找到则 `workspaceRegistry.create` + `sessionController.create({agentPreset})` → `resolveAgent`；消息通过 `AgentDelivery.send`，不是 `session/new` 带 message。这与 Freely ACP 的丢消息 bug 不同。

仍未验证（属于 B2 实现验收，不是研究缺口）：

- DSH host 实际启动并加载第三方插件；
- Python runtime ↔ plugin bridge；
- 首次 session 收到 task+role prompt 的端到端；
- gate 阻断/usage 上报；
- 真实 issue 到 PR 无 ACP。

结论：**C-E 的研究问题（插件形态/服务注入是否可行）已关闭；运行/E2E 是 B2 实现验收。**

### 2.4.1 Runtime load spike（2026-11-01）

- 新建 DSH profile `freely-web-spike`，从 `web` 模板复制，安装本地 `@freely/dsh-freely-spike`。
- `dsh --profile freely-web-spike` 启动输出：
  `[freely-spike] loaded services sessionController=function workspaceRegistry=function`
- 证明确实：第三方插件被 DSH host 加载；`inject` 的 `sessionController/workspaceRegistry` 可用；web host 能启动。
- 反例：`headless` profile 缺这两个服务，插件停在 `pending (waiting for services...)`，不能假设所有 profile 都支持。
- 仍未验证：创建/提示 session、Python bridge、gate E2E、真实 issue→PR。见 `spike/dsh-runtime-load.log`。

## 3. Harness RPC

`FreelyBridgeServer` 暴露给 Python runtime：

| 方法 | 参数 | 返回 |
| --- | --- | --- |
| `harness/session.new` | `{role,cwd,preset,model,title}` | `{sessionId}` |
| `harness/session.prompt` | `{sessionId,text,requestId}` | `{stopReason,usage}` |
| `harness/session.resume` | `{sessionId}` | `{sessionId}` |
| `harness/session.interrupt` | `{sessionId}` | `{ok}` |
| `harness/session.status` | `{sessionId}` | `{state,model,usage}` |
| `harness/session.usage` | `{sessionId}` | `{input,output,cache?,reported}` |
| `harness/session.close` | `{sessionId}` | `{ok}` |

**不提供 `fork` 作为必需能力**：DSH 的 Session 模型以独立 session 为主；跨角色上下文用显式 **context pack** 传递，而不是依赖 provider 的 fork 缓存。若 DSH 以后提供 fork，可作为优化。

## 4. 角色与 Session 映射

| Freely 角色 | DSH Session | Preset | 工具边界 |
| --- | --- | --- | --- |
| Manager | 常驻 1 个 | `freely-manager` | 读 scan/docs、派工、收口；不写代码 |
| Worker | 每 issue 1 个 | `freely-worker` | read/write/edit/bash/jobs/skills；在 worktree |
| Reviewer | 每阶段/每 PR 1 个 | `freely-reviewer` | 只读代码/证据 + 跑测试/gate；不写代码 |

- `sessionId` 写入 Freely `agent_working`，A2A handoff 记录引用它。
- 同一角色跨轮次可 `session.prompt` 复用；换模型/换 preset 时新建 session + context pack。
- Reviewer 必须是独立 Session/preset，不能复用 Worker session。

### 4.1 角色级 harness/model 选择

插件形态下，UI 的“角色 tab”选的是 **DSH preset + model**，不是外部 ACP CLI：

- Manager：`freely-manager` preset + manager model。
- Worker：`freely-worker` preset + worker model。
- Reviewer：`freely-reviewer` preset + reviewer model。

配置真源是 DSH settings/KV；`.freely/harness.toml` 只做只读镜像/导出。不要复用 `agent-table.toml` 的 `{role}_slot`（那是外部 CLI 概念）。详见 `../harness/harness-selection.md` 与 `../harness/harness-strategy.md`。

## 5. 交接：从 task 行升级为 Handoff Envelope

`@freely/dsh-freely` 不应把 DSH Session 当 A2A task 行用。建议在 Freely 侧新增 append-only：

```
handoffs
  handoff_id, task_id, parent_handoff_id,
  from_role, to_role, from_agent, to_agent,
  intent, constraints, acceptance,
  artifacts, context_refs, session_id,
  expected_output, ownership, status, created_at

handoff_messages
  handoff_id, message_id, role, parts, created_at
```

规则：

- 每次交接一条 handoff，不覆盖旧行。
- 消息 append-only；task state 只由显式 transition 改。
- Reviewer verdict 作为 artifact/message 追加，不覆盖 Worker 的 summary。
- `ownership` 决定后续消息归谁；handback 显式转移。
- 跨 harness/跨 model 时，prompt = 角色定义 + handoff envelope + context pack（PRD/pre-tests/artifacts/上一轮 verdict）。
- 同一 DSH host 内也走 envelope，不依赖“session 里应该还记得”。

## 6. 工具、skill、gate 怎么落地

### 6.1 原生工具（优先）

注册：

- `freely_gate`：跑 governance/pretests/PR/merge gate，返回 exit code + 输出。
- `freely_worktree`：创建/回收 dev/test worktree。
- `freely_tdd`：生成/校验 pre-tests、RED/GREEN 证据。
- `freely_issue_sync`：双平台 issue/PR 同步。
- `freely_status`：scan/agent/task 状态。

### 6.2 skill/prompt

- 把 `docs/system/workspace/skills/freely-*` 注册为 DSH skills。
- 把 `agents/manager-agent.md`、`worker-agent.md`、`reviewer-agent.md` 作为角色 prompt 段。
- `systemPrompt` 注册稳定前缀；动态 scan/attention 放尾部（沿用 Freely 的 STABLE/SEMI/DYNAMIC 排序）。

### 6.3 Gate

- Worker/Reviewer 通过 `bash` 或原生 `freely_gate` 调 CLI；exit code 必须能阻断。
- Plugin 不复制 gate 逻辑；gate 的唯一真源仍在 Freely scripts。

## 7. Panel 与 Source（可选）

- **Panel**：DSH client plugin 增加 “Freely” 侧栏：项目、issue、角色、handoff、gate、attention；数据来自 bridge。
- **Source**：初期保留 Freely scan（GitHub/Gitee/chat）；不要让 DSH Source 和 Freely scan 同时 intake，否则重复。后续若要 DSH 统一入口，必须把 issue-sync/ownership 一起迁，不能只迁 Source。

## 8. 迁移阶段

| 阶段 | 内容 | 验收 |
| --- | --- | --- |
| P0 | 插件骨架 + bridge + Manager session（只读 scan） | DSH 内 Manager 能读 scan 并 a2a-exit |
| P1 | Worker session + worktree + tools + handoff envelope v1 | 一个 issue 从派工到 commit，消息不丢 |
| P2 | Reviewer session + verdict + gates | fail→Worker 修复；pass→PR |
| P3 | Panel + 真实 issue E2E | 人能看见 attention/gate/角色 |
| P4 | Source 统一/多项目 | 不与 Freely scan 重复 intake |

## 9. 验收标准

1. 一个真实 issue，从 Manager 派工到 PR，全程不经过 ACP。
2. 首次 `session.new` 后，Worker/Reviewer 能收到完整 task message + 角色定义（针对当前 bug）。
3. 跨角色 handoff 有 append-only envelope；Reviewer verdict 不覆盖 Worker summary。
4. Worker session 死亡后，fail 反馈能重投并被新 session 收到。
5. gate exit code 能阻断 Worker/Reviewer 的下一步。
6. usage/cache 至少能区分 reported/estimated。
7. DSH Router/Ticket 明确禁用；不出现双 ownership。

## 10. 风险

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| DSH 服务 API 非公开/不稳定 | 插件无法注入 session/tools | spike 先验证；不行退 Source+CLI，但那不是 A 形态 |
| Python runtime 子进程生命周期 | 重启/退出泄漏 | plugin `ctx.effect` 管理；健康检查 |
| DSH Session 无 fork | 跨角色上下文丢失 | 显式 context pack；不依赖隐式 session |
| DSH 单仓 | 多项目丢失 | 一项目一 host；多项目另做 |
| 禁用 DSH Router/Ticket | DSH panel/既有能力不可用 | Freely panel 补；明确边界 |
| Reviewer 独立性 | 复用 Worker preset 会污染 | 独立 preset/工具白名单 |
| 双入口 | DSH Source + Freely scan 重复 | 初期只保留 Freely scan |

## 11. 结论

`@freely/dsh-freely` 应该是 **Freely-host 插件**：DSH 提供 Session/Agent/模型/工具，Freely 保留 Manager/Worker/Reviewer/A2A/scan/gates/worktree/PR。它不是 ACP adapter，也不是“DSH 拥有 loop、Freely 只做工具”的治理插件。

先做 P0/P1 spike，验证三件事：

1. 插件能否稳定注入 `sessionController/tools/skills`；
2. 首次 `session.new` 能否可靠收到 task message + role prompt；
3. handoff envelope 能否让 Reviewer/Worker 在不 fork 的情况下拿到足够上下文。

这三件事不过，就不应继续全量插件化。
