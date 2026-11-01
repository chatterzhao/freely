---
analysis_id: HARNESS-20261101T031502Z
phase_state: in_progress
created_at: 2026-11-01
---

# 角色级 harness 选择：UI / CLI / TUI 应该改哪份配置

## 0. 先分清两种形态的“harness”

截图里的 Runtime 选择器列的是本机 CLI（OpenCode、CodeBuddy、Codex、Cursor、Gemini CLI、Kimi Code、Qwen Code…）。这套列表不能直接搬进 Freely，因为两种部署形态的“harness”不是同一个对象：

| 形态 | harness 是什么 | 角色选择的对象 | 配置真源 |
| --- | --- | --- | --- |
| Freely 主应用 | 外部 ACP CLI（Claude/Codex/OpenCode/Cline） | 每个角色用哪个 **tool + slot** | `.freely/agent-table.toml` |
| Freely 作为 `@freely/dsh-freely` 插件 | DSH 本身 | 每个角色用哪个 **DSH preset + model** | DSH settings/KV（可镜像到 `.freely/harness.toml`） |

所以：

- **主应用**：截图里的 CLI 列表只有 ACP 支持的那几个可选；Cursor/Gemini/Kimi/Qwen 等当前没有 ACP adapter，应显示为“不支持/需要 adapter”，不能假装可选。
- **DSH 插件**：不要列外部 CLI；列 DSH 的 preset/model。除非 DSH 本身通过 ACP gateway 接了某个 backend，那也只是 DSH 的 backend，不是 Freely 的 harness。

## 1. 现状：配置已经能按角色分，但入口是全局的

`.freely/agent-table.toml` 已经是角色级真源：

```toml
[[agents]]
role = "manager"
manager_id = "manager_01"
manager_slot = "claude-apikey-ds-flash-auto"
pool = 1

[[agents]]
role = "worker"
worker_id = "worker_01"
worker_slot = "opencode-apikey-ds-flash-auto"
pool = 10

[[agents]]
role = "reviewer"
reviewer_id = "reviewer_01"
reviewer_slot = "cline-account-ds-flash-free-auto"
pool = 99
```

`.freely/config.toml` 是全局：

```toml
AGENT_AI_TOOL_ADAPTER = "acp"
AGENT_AI_TOOL_ADAPTER_POLICY = "acp"
FREELY_ACP_CLAUDE_BIN = ".../claude-agent-acp"
FREELY_ACP_OPENCODE_BIN = ".../opencode"
```

问题：

1. `freely set-tool` 只改全局 tool/adapter，不改 `{role}_slot`；不能做“Manager 用 Claude、Worker 用 OpenCode、Reviewer 用 Cline”。
2. 现有 runtime 已经能按 `manager_slot/worker_slot/reviewer_slot` 分辨角色，但没有 UI/CLI 统一入口。
3. adapter 是全局的；如果三个角色用不同 adapter（acp/direct），当前配置表达不了。短期应约束“三角色都用 ACP”，或后续加 `{role}_adapter`。
4. 模型/effort 也没有角色级字段；当前模型多在 slot 的 CLI 配置里。

## 2. UI 应该长什么样

截图的结构可以复用：标题 + “跟随全局” + 本机候选 + 健康状态。但 Freely 要加角色维度：

```
┌─ 选择 Agent Harness ───────────────────────────────┐
│  [Manager]  [Worker]  [Reviewer]                    │
│                                                     │
│  ☑ 跟随 Manager（仅 Worker/Reviewer 显示）           │
│                                                     │
│  ● OpenCode      native fork · resume · usage   ✓   │
│  ● Codex         degraded fork · resume        ✓   │
│  ● Claude        native fork · resume · usage   ✓   │
│  ○ Cursor        无 ACP adapter                  ✕   │
│  ○ Gemini CLI    无 ACP adapter                  ✕   │
│                                                     │
│  Slot:  [opencode-apikey-ds-flash-auto      ▾]      │
│  Model: [跟随 slot / 可选覆盖              ▾]      │
│                                                     │
│  变更预览：worker_slot: codex-... → opencode-...    │
│  [验证]  [应用（下次 session 生效）]                 │
└─────────────────────────────────────────────────────┘
```

关键交互：

1. **角色 tab**：Manager / Worker / Reviewer 分开选。
2. **跟随/复制**：Worker/Reviewer 可“跟随 Manager”或“复制到其他角色”；默认各自独立。
3. **候选健康**：binary、ACP、fork（native/degraded）、resume、usage；不可用的置灰并给原因。
4. **slot**：tool 选定后列出该 tool 的可用 slot；slot 是账号/凭据/profile，不只是 tool。
5. **应用前 diff**：展示 `agent-table.toml` 的旧值/新值，不直接改文件。
6. **生效时机**：写配置只影响**下一次新建/恢复 session**；不杀正在跑的 Worker/Reviewer。Manager 可显式“轮换”。
7. **审计**：谁、何时、从什么改到什么；写入 `.freely/run/harness-config-audit.jsonl`。

## 3. 写配置的映射

### 3.1 Freely 主应用

| UI 选择 | 写入 | 说明 |
| --- | --- | --- |
| role=manager, tool=claude, slot=claude-apikey-x | `manager_slot = "claude-apikey-x"` | 只改角色行 |
| role=worker, tool=opencode, slot=... | `worker_slot = ...` | 同上 |
| role=reviewer, tool=cline, slot=... | `reviewer_slot = ...` | 同上 |
| “应用到全部” | 三个 slot 一起改 | 仍保留角色行 |
| adapter | `AGENT_AI_TOOL_ADAPTER=acp` | 短期全角色统一；混合 adapter 需新字段 |
| binary | `FREELY_ACP_<TOOL>_BIN` | tool 级，不是角色级；缺失时探测 PATH/cache |
| model/effort | 暂不改 | 当前在 slot 的 CLI 配置里；角色级模型要新字段 |

**不要**直接改 `.freely/config.toml` 的 `AGENT_AI_TOOL` 来表达角色级选择；那是全局旧字段。角色级真源是 `agent-table.toml` 的 `{role}_slot`。

### 3.2 Freely 作为 DSH 插件

| UI 选择 | 写入 | 说明 |
| --- | --- | --- |
| role=manager, preset=freely-manager, model=... | DSH settings/KV | DSH 是 harness 真源 |
| role=worker, preset=freely-worker, model=... | DSH settings/KV | Worker 独立 preset |
| role=reviewer, preset=freely-reviewer, model=... | DSH settings/KV | Reviewer 只读 preset |
| 镜像/导出 | `.freely/harness.toml` | 只做可移植副本，不双写权威 |

插件模式下不要复用 `agent-table.toml` 的 `{role}_slot` 作为 harness 真源；slot 是外部 CLI 概念，DSH 没有“slot”。应改成 `{role}_preset` / `{role}_model` 的插件配置。

## 4. 统一后端接口

UI、CLI、TUI 都应调用同一个后端，不各自写文件：

```
freely harness list   [--role manager|worker|reviewer] [--json]
freely harness show   [--json]
freely harness set    --role worker --tool opencode --slot opencode-apikey-x
freely harness set    --all --tool claude --slot claude-apikey-x
freely harness set    --role reviewer --preset freely-reviewer --model deepseek-v4
freely harness validate [--role ...] [--strict]
freely harness apply  --file harness.toml
```

规则：

1. `set` 先 probe，再写；probe 失败不落盘。
2. `validate` 调 `harness-status --strict`；角色级 require 需要扩展 `--role`。
3. 写前备份 `agent-table.toml`，写后重新读取校验。
4. 写审计记录；失败回滚。
5. 运行中的 session 不重启；输出 `pending_restart_roles`。
6. 同一后端支持 JSON，TUI/UI 只做展示。

## 5. 验证与错误状态

| 状态 | UI | 行为 |
| --- | --- | --- |
| binary missing | 红色“未安装” | 禁止应用 |
| ACP 不可用 | 红色“无 ACP” | 禁止应用 |
| fork=degraded | 黄色“fork 降级” | 允许，但提示 Reviewer/Worker 首轮冷启动 |
| resume 不支持 | 黄色 | 允许，但提示上下文不连续 |
| slot 不存在 | 红色 | 禁止应用 |
| 运行中 session | 蓝色“下次生效” | 不杀进程 |
| 混合 adapter | 红色“暂不支持” | 要求全角色 ACP，或先加 per-role adapter |

## 6. 与截图的关系

截图是“本机 Runtime/CLI 选择器”，适合 Freely 主应用的候选列表；但要做三处改造：

1. **角色 tab**：Manager/Worker/Reviewer 分开。
2. **能力/健康列**：不仅 Wi-Fi 图标，要显示 ACP/fork/resume/usage。
3. **过滤**：没有 ACP adapter 的 CLI 置灰，不误导。

DSH 插件形态应做成“角色 → DSH preset/model”的选择器，外观可以类似，但候选对象不同。

## 7. 建议的最小落地

1. 先做 `freely harness show/list/set`（只改 `{role}_slot`），不碰 UI。
2. 用 `harness-status` 做 probe/validate，补 `--role`。
3. TUI 复用同一 JSON 接口；UI 后做。
4. 暂时强制三角色 adapter 都是 `acp`；混合 adapter 单独设计 `{role}_adapter`。
5. 角色级 model/effort 作为下一阶段；先不要伪装已支持。

## 8. 未解

- `{role}_adapter` 是否值得引入，还是永远全 ACP？
- 角色级 model/effort 放 `agent-table.toml` 还是 slot 的 CLI 配置？
- 运行中的 Manager 轮换如何不打断当前 patrol？
- DSH 插件的配置权威在 DSH settings 还是 `.freely/harness.toml`？建议 DSH 权威、文件只读镜像。
- UI 是否支持“同一 tool 不同 slot”按角色分配？当前 `{role}_slot` 已支持，UI 要展示 slot 而非只展示 tool。
