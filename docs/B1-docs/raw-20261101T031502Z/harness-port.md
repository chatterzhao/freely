---
analysis_id: HP-20261101T231000Z
phase_state: in_progress
topic: HarnessPort 与 DSH adapter
created_at: 2026-11-01
---

# HarnessPort：把 agent harness 当基座，而不是宿主

## 0. 结论

Freely 现在的事实是：

- 通过 ACP 调 Claude/Codex/OpenCode/Cline；`run-acp-prompt.py` 支持 session/new、resume、fork（失败降级 new）、prompt、usage。
- 工具/能力差异靠代码分支兜底；没有统一 capability probe。
- DSH 原型没有 ACP 服务端，只有 Cordis 插件/管理 API；不能当普通 ACP CLI 用。
- `mcpServers` 固定传 `[]`，MCP 不由 Freely 编排。

所以“可切换基座”需要的是一个**显式 HarnessPort**，不是再加一个 `AGENT_AI_TOOL` 值。

## 1. HarnessPort 最小接口

| 方法/字段 | 作用 | 缺失时 |
| --- | --- | --- |
| `probe()` | 返回 binary 是否存在、版本、协议、能力 | fail-closed 或降级 |
| `capabilities()` | session/fork/resume/stream/interrupt/tools/skills/usage/cache/subagent/mcp | 每项 native/degraded/unknown/unsupported |
| `start()` | 新建 session，返回 session_id | 不能派工 |
| `prompt()` | 发送 prompt，返回 stopReason/usage/事件流 | 不能执行 |
| `resume()` | 恢复同一 session | 上下文丢失 |
| `fork()` | 从父 session 派生 | 冷启动/上下文丢失 |
| `interrupt()` | 中止当前 turn | 只能杀进程 |
| `usage()` | input/output/cache 字段 | 只能估算 |
| `close()` | 结束 session | 资源泄漏 |

关键：**能力不是布尔**。`fork` 至少有 `native / degraded / unsupported / unknown` 四态；`usage` 至少有 `reported / estimated / absent`。布尔会把“尝试后降级”误报成“支持”。

## 2. 当前四家 ACP CLI 的实测/代码事实

| 能力 | Claude | Codex | OpenCode | Cline |
| --- | --- | --- | --- | --- |
| session/new | 是 | 是 | 是 | 是 |
| resume | 是 | 是 | 是 | 是 |
| fork | native | degraded（尝试后 new） | native | degraded（尝试后 new） |
| usage | 部分 | 部分 | 部分 | 少 |
| cache 字段 | provider 依赖 | provider 依赖 | provider 依赖 | provider 依赖 |
| MCP | 自身配置 | 自身配置 | 自身配置 | 自身配置 |
| 工具白名单 | ACP/preset | ACP/preset | ACP/preset | ACP/preset |

`harness-status` 已按 registry + 代码事实输出 `native/degraded`，不是手写“支持/不支持”。

## 3. 三种集成模式

### 模式 A：ACP 子进程（现状）

- Freely runtime 启动 `claude-agent-acp`/`codex-acp`/...；JSON-RPC over stdio/socket。
- 优点：进程隔离、工具链成熟、可替换。
- 缺点：能力受 ACP 覆盖限制；MCP/tool policy 受 CLI 影响。

### 模式 B：DSH 插件桥（DSH 作为基座）

- 在 DSH 宿主内注册一个 Freely 可见的 endpoint；Freely 发 prompt，插件开 DSH Session 并回事件。
- 优点：复用 DSH 的 Session/tool/preset；深度集成。
- 缺点：必须解决“谁拥有 Router/Ticket”；插件要跟随 DSH 版本；不是通用 ACP。

### 模式 C：Node bridge（DSH 作为库）

- Freely 侧起一个 Node 进程，用 DSH SDK 建 Session，暴露 JSON-RPC 给 Python runtime。
- 优点：不依赖 DSH 服务；可控。
- 缺点：要维护 DSH SDK 适配；升级断裂；双进程生命周期。

结论：**短期只做 A + HarnessPort 契约；DSH 只做 B 的 spike，不把 C 作为主路径。**

## 4. 按角色选择

Freely 的 Manager/Worker/Reviewer 对 harness 的需求不同：

| 角色 | 关键能力 | 可降级 |
| --- | --- | --- |
| Manager | resume、usage、stream、tools（scan/chat 读取） | fork 不需要 |
| Worker | fork/resume、tools、skills、usage | fork 可降级为 new |
| Reviewer | fork/resume、review 读取、usage | fork 可降级，但要显式记录 |

配置面应从“全局单值”变成“按角色 + fallback”，并显示 capability probe 结果。DSH 的 Runtime picker 是 UX 参考，不是实现参考。

## 5. 缓存语义

- ACP 的 `usage` 字段不一定有；没有时 runtime 用 `prompt_bytes//4` 估算。必须标 `input_source=estimated`，不能当真实命中率。
- HarnessPort 应暴露 `usage_reported`、`cache_reported`、`prompt_bytes`，让上层知道“能不能算命中率”。
- 不同 harness 的 cache 语义不同；跨 harness 比较前先统一口径。

## 6. 与 DSH 的对比

| 维度 | DSH | Freely |
| --- | --- | --- |
| harness 绑定 | 绑定 DSH/Cordis | ACP 多 CLI |
| 集成深度 | 深（Session/tool/preset/client） | 中（session/prompt/usage） |
| 可替换性 | 低（换宿主=重写） | 高（换 CLI=换 adapter） |
| 能力契约 | 宿主 API 隐式 | 需要显式 HarnessPort |
| 插件模式 | Cordis bundle | 无 host plugin API |

结论：**Freely 的架构方向更对，但契约必须显式化；DSH 的深度值得借鉴，但不能把 DSH 当 ACP。**

## 7. 未解

- `fork` 的 degraded 是否应算“满足 require fork”？建议不算，但允许显式 `--allow-degraded`。
- 按角色选 harness 的配置放 `.freely/config.toml` 还是 agent-table？
- DSH 插件桥的所有权：DSH 拥有 Router/Ticket 时，Freely 只做工具插件；Freely 拥有 loop 时，DSH 只做 harness。两者不能同时拥有。
- 跨 harness 的 usage/cache 口径如何统一？
