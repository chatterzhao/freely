---
analysis_id: HARNESS-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# Harness 策略：可插拔基座、角色选择、DSH 集成边界

## 0. 结论

- **Freely 主应用**：harness 是外部 ACP CLI；角色选 tool + slot；写 `.freely/agent-table.toml`；这是当前主形态。
- **Freely 作为 `@freely/dsh-freely` 插件**：harness 是 DSH；角色选 DSH preset + model；写 DSH settings；Freely 保留 loop；这是可选形态 B2。
- **不做 DSH-as-harness adapter**：那会把 DSH 的 Router/Thread/Mandate 阉割成执行器，战略价值低。
- 两者共用 Freely core，只替换 HarnessProvider + 角色配置。

## 1. HarnessPort 最小接口

| 方法/字段 | 作用 | 缺失时 |
| --- | --- | --- |
| `probe()` | binary/version/协议/能力 | fail-closed 或降级 |
| `capabilities()` | session/fork/resume/stream/interrupt/tools/skills/usage/cache/subagent/mcp | native/degraded/unknown/unsupported |
| `start()` | 新建 session | 不能派工 |
| `prompt()` | 发送 prompt，返回 stopReason/usage | 不能执行 |
| `resume()` | 恢复 session | 上下文丢失 |
| `fork()` | 从父 session 派生 | 冷启动/上下文丢失 |
| `interrupt()` | 中止当前 turn | 只能杀进程 |
| `usage()` | input/output/cache | 只能估算 |
| `close()` | 结束 session | 资源泄漏 |

能力不是布尔：`fork` 至少 native/degraded/unsupported/unknown；`usage` 至少 reported/estimated/absent。布尔会把“尝试后降级”误报成“支持”。

## 1.1 HarnessPort 可实现接口

```python
from typing import Literal, Protocol
from dataclasses import dataclass

Cap = Literal["native", "degraded", "unsupported", "unknown"]

@dataclass(frozen=True)
class Capabilities:
    session: Cap
    fork: Cap
    resume: Cap
    stream: Cap
    interrupt: Cap
    tools: Cap
    skills: Cap
    usage: Cap          # reported/estimated/absent
    cache: Cap          # reported/estimated/absent
    mcp: Cap
    subagent: Cap

@dataclass(frozen=True)
class Health:
    ok: bool
    binary: str | None
    version: str | None
    acp: bool
    error: str | None

class HarnessPort(Protocol):
    id: str
    def probe(self) -> Health: ...
    def capabilities(self) -> Capabilities: ...
    def start(self, role: str, cwd: str, tools: list[str], skills: list[str]) -> "Session": ...
    def prompt(self, session: "Session", text: str, *, manifest: dict | None = None) -> "TurnResult": ...
    def resume(self, session_id: str) -> "Session": ...
    def fork(self, session_id: str) -> "Session": ...
    def interrupt(self, session: "Session") -> None: ...
    def usage(self, session: "Session") -> "Usage": ...
    def close(self, session: "Session") -> None: ...
```

约束：

- `fork=degraded` 表示允许尝试，失败后 new；调用方要知道“不是原生”。
- `usage/cache=absent` 时返回 null，不返回 0。
- `probe` 必须可单独调用；UI 列表不启动 session。
- `prompt` 返回 stopReason、usage、session_id；错误不吞。

## 1.2 RoleHarnessConfig

归一化视图（不是新配置文件）：

```json
{
  "role": "manager",
  "tool": "claude",
  "slot": "claude-apikey-ds-flash-auto",
  "adapter": "acp",
  "model": null,
  "preset": null,
  "source": "agent-table",
  "capabilities": {"fork": "native", "resume": "native", "usage": "reported"},
  "health": {"ok": true, "acp": true}
}
```

映射：

- Freely 主应用：`role` + `{role}_slot` + 全局 `AGENT_AI_TOOL_ADAPTER`；tool 从 slot 前缀推断；model 目前未知。
- DSH 插件：`role` + `{role}_preset` + `{role}_model`；source=DSH settings。
- 写回：主应用只改 `{role}_slot`；插件只改 DSH settings；`.freely/harness.toml` 只镜像。
- 不把 `adapter` 写进 agent-table，直到支持 `{role}_adapter`。

## 1.3 Per-role probe

`freely harness status --role reviewer --json` 输出：

```json
{
  "role": "reviewer",
  "slot": "cline-account-ds-flash-free-auto",
  "tool": "cline",
  "health": {"ok": true, "binary": "...", "acp": true, "version": "..."},
  "capabilities": {"session": "native", "fork": "degraded", "resume": "native", "usage": "absent"},
  "requirements": {"fork": "optional", "usage": "optional"},
  "satisfied": true,
  "degraded": ["fork"],
  "reason": "fork degraded: fallback to new + context pack"
}
```

- `requirements` 由角色决定：Manager 要 resume/skills；Worker 要 tools/skills；Reviewer 要 fork/resume + 只读。
- `satisfied=false` 时 `set` 拒绝；`degraded` 允许但显式提示。
- `--strict` 把 degraded 也当失败；`--allow-degraded` 才允许。

## 1.4 统一 harness JSON 契约

```
GET  /harness/roles
GET  /harness/candidates?role=worker
POST /harness/apply  {role, tool, slot, model?}
POST /harness/validate {role, tool, slot}
```

返回：

```json
{
  "ok": true,
  "diff": {"worker_slot": ["old", "new"]},
  "requires_restart": ["worker"],
  "audit_id": "...",
  "error": null
}
```

- UI/CLI/TUI 都调这个 contract；不各自写 TOML。
- `apply` 前 validate；失败不落盘；写前备份/写后重读。
- 运行中的 session 不重启；返回 `requires_restart`。

## 2. 四家 ACP CLI 的事实

| 能力 | Claude | Codex | OpenCode | Cline |
| --- | --- | --- | --- | --- |
| session/new | 是 | 是 | 是 | 是 |
| resume | 是 | 是 | 是 | 是 |
| fork | native | degraded（尝试后 new） | native | degraded（尝试后 new） |
| usage | 部分 | 部分 | 部分 | 少 |
| cache 字段 | provider 依赖 | provider 依赖 | provider 依赖 | provider 依赖 |
| MCP | 自身配置 | 自身配置 | 自身配置 | 自身配置 |

`harness-status` 已按 registry + 代码事实输出 native/degraded，不是手写布尔。

## 3. 角色级选择

当前 `agent-table.toml` 已经是角色级真源：

```toml
manager_slot  = "claude-apikey-ds-flash-auto"
worker_slot   = "opencode-apikey-ds-flash-auto"
reviewer_slot = "cline-account-ds-flash-free-auto"
```

- Manager：resume/usage/skills；不需要 fork。
- Worker：fork/resume、tools、skills、usage；可降级 new。
- Reviewer：fork/resume、只读+测试/gate；独立 preset，不复用 Worker。

`AGENT_AI_TOOL_ADAPTER` 目前全局 `acp`；短期强制全角色 ACP。混合 adapter 需要 `{role}_adapter`，当前不支持。

## 4. 两种部署形态

| 维度 | A: Freely 主应用 | B2: Freely 作为 DSH 插件 |
| --- | --- | --- |
| 进程 | Freely runtime（bash/Python） | DSH 进程 + Freely Python 子进程 |
| loop owner | Freely | Freely |
| harness | 外部 ACP CLI | DSH Session/Agent |
| 角色选择 | tool + slot | DSH preset + model |
| 配置真源 | `.freely/agent-table.toml` | DSH settings/KV；`.freely/harness.toml` 镜像 |
| 外部 CLI | 直接支持 | 不直接支持（除非 DSH 接 ACP gateway） |
| 多项目 | projects.tsv + 多 runtime | 单仓/单 host；多项目多 host |
| 当前代码 | 已有 ACP bridge | 需新建插件/bridge |

### A 的优缺点

- 优点：保留全部 Freely 能力；真正换 harness；slot 可换账号/profile；多项目/worktree/PR 已有。
- 代价：ACP 差异大；跨 harness 上下文只能 context pack；CLI 版本/登录由 Freely 承担；UI 必须过滤非 ACP CLI。

### B2 的优缺点

- 优点：DSH 原生 session/tools/skills/model/usage；少一层 ACP；三角色可共用 host 但独立 session。
- 代价：DSH 单仓/单 host；依赖插件服务 API；外部 CLI 列表不适用；DSH Router/Ticket 不用；Python 子进程生命周期。

## 5. DSH 集成的四种方案

| 方案 | 谁拥有 loop | 结果 |
| --- | --- | --- |
| A: DSH-as-harness adapter | Freely | DSH 的 Router/Thread/Mandate 被旁路，只剩 Session 执行器；**不做** |
| B1: DSH-host 治理插件 | DSH | Freely 只提供 gates/worktree/TDD/issue；丢掉 Manager/A2A/loops；不是“全部能力” |
| B2: Freely-host 插件 | Freely | Freely 保留 Manager/Worker/Reviewer/A2A/scan/gates；DSH 只做 harness；**推荐用于全部能力** |
| C: 不做 | Freely | 保持 ACP 四家；成本最低 |

## 6. 方案 A 会阉割 DSH 什么

| DSH 能力 | adapter 模式 |
| --- | --- |
| Router/准入/批量决策 | 全丢（Freely Manager 取代） |
| Trigger/Source/Eval/Decision | 全丢 |
| Ticket/Assignment/Stage | 全丢（Freely issue/worktree 取代） |
| Thread/Subscription | 全丢 |
| Report/Attention/ownership/handback | 大部分丢 |
| Mandate/Policy 版本 | 全丢 |
| Watchdog/恢复 | 全丢 |
| 单写 Store/Effect 队列 | 全丢 |
| Panel/IM/health | 大部分丢 |
| Session/模型执行 | 保留 |

结论：这不是“集成 DSH”，是“把 DSH 当 Claude Code 用”。

## 7. 方案 B2 的插件 API 现实

DSH 主插件注入：

```
agents, sessionController, sessionPersistence, workspaceRegistry,
permissionPresets, tools, systemPrompt, skills, webServer, llm, subprocess
```

- 可以创建/解析/提示/停止 Session，注册 tools/skills/prompt。
- DSH 的公开插件入口主要是 Source 插件；第三方插件能否稳定拿到全部服务，需要 spike。
- 若不能，退化为 Source + skill + CLI，但那不是 B2 的“全部能力”。

B2 不加载 `dsh-superagent`，避免 DSH Router/Ticket 与 Freely Manager/A2A 双 loop。

## 8. 何时重评

- B2 只在：DSH 稳定开放 services；允许 Freely 拥有 loop 且 Router/Ticket 可禁用；有真实用户需求；能接受 DSH 编排不用。
- B2 spike 验收：首次 session 收到 task+role prompt；一个真实 issue 到 PR 无 ACP；handoff append-only；gate 阻断；usage 可区分 reported/estimated。
- 没有这组证据，不做全量插件，更不做 adapter。

## 9. 未解

- `fork` degraded 是否算 `--require` 满足？建议不算，但允许显式 `--allow-degraded`。
- 是否引入 `{role}_adapter`，还是永远全 ACP？
- 角色级 model/effort 放 agent-table 还是 slot？
- DSH 服务 API 对第三方插件是否稳定。
- DSH 单仓/单 host 下多项目怎么办。
