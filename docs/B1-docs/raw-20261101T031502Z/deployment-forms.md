---
analysis_id: DEPLOY-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 两种部署形态：Freely 主应用 vs Freely 作为 DSH 插件

## 0. 一句话

- **形态 A（Freely 主应用）**：Freely 拥有 loop，agent harness 是可插拔基座（ACP CLI/slot）。UI/CLI/TUI 按角色选 harness，写 `.freely/agent-table.toml`。
- **形态 B（Freely 作为 `@freely/dsh-freely` 插件）**：Freely 仍拥有 loop，DSH 是 harness。UI/CLI 按角色选 DSH preset/model，写 DSH settings；`.freely/harness.toml` 只是镜像。

两者**共用同一个 Freely core**（Manager/Worker/Reviewer、SDD/TDD、handoff、gates、worktree、PR），差别只在 **HarnessProvider + 角色配置 + UI 选项**。不要做成两个产品。

## 1. 对比表

| 维度 | A: Freely 主应用 | B: Freely 作为 DSH 插件 |
| --- | --- | --- |
| 进程 | Freely runtime（bash/Python） | DSH 进程 + Freely Python runtime 子进程 |
| loop owner | Freely | Freely |
| agent harness | 外部 ACP CLI（Claude/Codex/OpenCode/Cline） | DSH Session/Agent |
| 角色选择对象 | tool + slot（+ adapter） | DSH preset + model |
| 配置真源 | `.freely/agent-table.toml` | DSH settings/KV；`.freely/harness.toml` 镜像 |
| 外部 CLI | 直接支持 | 不直接支持；除非 DSH 通过 ACP gateway 接 backend |
| DSH Router/Ticket | 不使用 | 不使用（不加载 dsh-superagent） |
| 多项目 | 全局 projects.tsv + 多 runtime | DSH 单仓/单 host；多项目需多 host |
| UI | Freely UI/TUI/CLI | DSH panel + Freely bridge |
| 当前代码 | 已存在（ACP bridge） | 需新建插件/bridge |
| 主要成本 | ACP 适配、跨 harness 上下文 | DSH 服务 API、插件生命周期、单仓 |
| 主要收益 | 多 harness、可移植、现有能力 | DSH 模型/tools/session、原生 UI |

## 2. 形态 A：Freely 主应用 + 可插拔 harness

### 2.1 结构

```
Freely runtime (bash/Python)
  Manager/Worker/Reviewer
  scan/B1/B2/TDD/gates/worktree/PR
        │ HarnessPort
  ACP adapter (Claude/Codex/OpenCode/Cline)
        │
  external CLI sessions
```

### 2.2 角色级选择

- `.freely/agent-table.toml` 的 `manager_slot/worker_slot/reviewer_slot` 已经是角色级真源。
- UI 选 `tool + slot`；写 `{role}_slot`。
- adapter 目前全局 `acp`；短期强制三角色都用 ACP；混合 adapter 需新增 `{role}_adapter`。
- model/effort 目前多在 slot 的 CLI 配置里；角色级 model 是后续能力。

### 2.3 优点

- 保留现有全部 Freely 能力，迁移成本最低。
- 真正“换 harness”：Claude/Codex/OpenCode/Cline 可混用。
- 同一角色可换 slot（账号/凭据/profile），不只是一张 CLI 列表。
- 跨项目、worktree、PR/issue sync 都已存在。

### 2.4 代价

- ACP 能力差异大：fork native/degraded、usage/cache 不稳定。
- 跨 harness 上下文只能靠 prompt/context pack，不能依赖 session fork。
- 外部 CLI 版本/登录/二进制问题由 Freely 承担。
- UI 候选必须过滤“无 ACP adapter”的 CLI，不能照搬截图整张列表。

## 3. 形态 B：Freely 作为 `@freely/dsh-freely` 插件

### 3.1 结构

```
DSH process
  @freely/dsh-freely
    FreelyHost + DshHarnessAdapter + bridge
        │
  DSH Session/Agent (Manager/Worker/Reviewer presets)
        │
  Freely Python runtime (loop, scan, gates, worktree, PR)
```

### 3.2 角色级选择

- UI 选 `DSH preset + model`（Manager/Worker/Reviewer 分开）。
- 写 DSH settings/KV；`.freely/harness.toml` 只读镜像/导出。
- 不要复用 `{role}_slot`：DSH 没有外部 CLI slot；slot 是形态 A 的概念。
- 不加载 `dsh-superagent`，避免 DSH Router/Ticket 与 Freely Manager/A2A 双 loop。

### 3.3 优点

- DSH 原生 Session/Agent/tools/skills/model/usage，少一层 ACP。
- 三角色可以共用 DSH host，但保持独立 session/preset。
- Freely 的 SDD/TDD/gates/worktree/PR 全部保留。
- 可利用 DSH 的模型路由、preset、panel、subagent。

### 3.4 代价

- DSH 单仓/单 host；多项目要多个 host。
- 依赖 DSH 插件服务 API 稳定性；需要 spike。
- 外部 CLI 列表不再适用；只能用 DSH backend（除非 DSH 自己接 ACP gateway）。
- DSH Router/Ticket 不用，DSH panel 的既有语义要重做/映射。
- 插件生命周期、Python 子进程、配置双源要治理。

## 4. 共用的 core 与差异层

```
Freely core（共用）
  Manager/Worker/Reviewer
  handoff envelope
  B1/B2/SDD/TDD
  gates/worktree/PR/issue sync

HarnessProvider（差异层）
  A: AcpHarnessProvider
  B: DshHarnessProvider

RoleConfig（差异层）
  A: agent-table {role}_slot + adapter
  B: DSH settings {role}_preset/model
```

只要 HarnessProvider 接口一致，UI/CLI/TUI 就可以共用“角色 tab + 候选列表 + 应用”的交互；候选内容由 provider 决定：

- A 的 `list` 返回 ACP tool/slot/health。
- B 的 `list` 返回 DSH preset/model/health。

## 5. 统一接口（建议）

```
HarnessProvider
  listCandidates(role) -> Candidate[]
  probe(candidate) -> Health
  createSession(role, candidate, cwd) -> Session
  prompt(session, envelope) -> Result
  resume(session) -> Session
  usage(session) -> Usage
  stop(session) -> void

RoleHarnessConfig
  role, harness_id, profile/slot/preset, model, adapter
```

UI 不直接写 TOML；调用 `harness set` 后端。后端按部署形态写不同真源。

## 6. 选型建议

- **如果 Freely 的产品目标是“项目所有者 + 多 harness 可插拔”**：A 是主形态，继续把 ACP/HarnessPort 做稳；UI 先做角色级 slot 选择。
- **如果目标是把 Freely 能力带进 DSH 生态**：B 是独立形态，先做 P0/P1 spike；不要为了 B 牺牲 A 的 core。
- **不要同时做两套 loop**：B 里禁用 DSH Router/Ticket；A 里不加载 DSH plugin。
- **不要共用一套配置字段**：A 写 agent-table；B 写 DSH settings。用 `RoleHarnessConfig` 做适配层，不强行统一文件格式。

## 7. 未解

- A 是否值得支持 `{role}_adapter`（混合 acp/direct），还是永远全 ACP？
- B 的配置权威在 DSH settings 还是 `.freely/harness.toml`？建议 DSH 权威。
- B 是否需要 DSH panel 才能接受？CLI 先行的最小形态是什么？
- 两者是否共享同一个 `harness` CLI，还是 B 只暴露 DSH 命令？
- 角色级 model/effort 在 A 里放哪里（agent-table vs slot）？
