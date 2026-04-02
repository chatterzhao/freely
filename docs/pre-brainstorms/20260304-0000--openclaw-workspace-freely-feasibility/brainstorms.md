# 研究：Freely 能否作为 OpenClaw 的子功能（仅靠 `~/.openclaw/workspace-freely/`）

## 结论（先给答案）

在 **不改 OpenClaw 源码** 前提下，结论分两种：

1. **严格版（只允许改/放 `~/.openclaw/workspace-freely/`，其他任何路径都不动）**  
   结论：**不可完整落地**。  
   原因：OpenClaw 的 agent 绑定、hooks 启用、cron 持久化、默认 workspace 指向，都会落在 `~/.openclaw/openclaw.json` 和 `~/.openclaw/cron/` 等路径，不是 workspace 内部。

2. **工程版（不改 OpenClaw 源码，但允许用 OpenClaw 官方 CLI 做一次配置）**  
   结论：**可落地 70%~85% 的 Freely 能力**，可作为“Freely-on-OpenClaw profile”。  
   能实现：文档驱动、自治循环、技能化流程、定时触发、会话与记忆连续性。  
   难完整实现：Freely 当前的独立 supervisor/PID 监控语义、极简四输入启动面、严格 GitFlow/工作树强制门禁（需要额外脚本治理）。

研究基线：OpenClaw 版本 `2026.2.26`（本机 `openclaw --version`），研究日期 `2026-03-04`。

---

## 证据要点（源码+文档）

- Workspace 是 agent 的 home，支持注入 `AGENTS.md/SOUL.md/USER.md/TOOLS.md/HEARTBEAT.md/BOOTSTRAP.md/MEMORY.md`。  
  见：`openclaw/docs/concepts/agent-workspace.md`、`src/agents/workspace.ts`、`src/agents/system-prompt.ts`
- `workspace/skills` 具有最高优先级，可覆盖 managed/bundled skills。  
  见：`openclaw/docs/tools/skills.md`、`src/agents/skills/workspace.ts`
- `workspace/hooks` 可被发现，但要真正启用，通常需要 `hooks.internal.enabled` 和 `hooks.internal.entries.*.enabled`。  
  见：`openclaw/docs/automation/hooks.md`、`src/hooks/loader.ts`、`src/cli/hooks-cli.ts`
- Cron 能做持续调度，但 job 存储在 `~/.openclaw/cron/jobs.json`。  
  见：`openclaw/docs/automation/cron-jobs.md`、`src/cron/service.ts`
- OpenClaw 明确是“workspace 为默认 cwd，不是硬隔离沙箱”。  
  见：`openclaw/docs/concepts/agent-workspace.md`
- 子会话/cron 会使用 bootstrap 精简集，不会自动注入所有文件。  
  见：`src/agents/workspace.ts` 的 `filterBootstrapFilesForSession`

---

## 与 Freely 能力映射

### 可直接承接（适合放进 `workspace-freely/`）

- `AGENTS.md`：固化 Freely 宪法、loop 方法论、文档门禁流程
- `skills/`：把 doc-loop / dev-loop / review-loop 做成技能入口
- `hooks/`：在 `agent:bootstrap`、`command:new/reset` 阶段注入/记录流程
- `memory/` + `MEMORY.md`：承接 Freely 的连续性与 checkpoint 语义
- `BOOT.md` + cron：实现“定时唤醒继续推进”

### 需要 workspace 外配合（严格版下卡死）

- 将某个 agent 指向 `workspace-freely`（`agents.list[].workspace`）
- 启用 hooks（`hooks.internal.enabled/entries`）
- 管理 cron job（存储在 `~/.openclaw/cron/`）
- 渠道路由/多 agent 绑定（`openclaw.json`）

### 与 Freely 当前脚本语义不完全等价

- Freely `bin/freely start` 是 supervisor 模式（监控外部 AI 进程退出并重启）  
  OpenClaw 更偏“事件驱动 + agent run 队列”，不是同一层级的 PID 监督器。
- Freely 强调四输入最小面（项目路径/意图/宪法/AI 规格）  
  OpenClaw 以 gateway + config 为中心，天然配置面更大。
- Freely 的 GitFlow/pre-develop/worktree 强门禁  
  OpenClaw 可以“执行脚本”，但门禁本身需要仓库侧脚本和流程治理，不是 OpenClaw 原生策略。

---

## 可行落地方案（推荐）

目标：把 Freely 做成 OpenClaw 的一个“工作区画像 + 技能包”，不改 OpenClaw 源码。

1. 建立 `~/.openclaw/workspace-freely/`
2. 写入 Freely 版 `AGENTS.md`（宪法、三层循环、验收门禁、恢复规则）
3. 放置 `skills/freely-*.md`（issue intake、doc-loop、dev-loop、review gate）
4. 放置 `hooks/`（session-memory 增强、bootstrap 补充、周期状态落盘）
5. 用官方 CLI 做一次配置：
   - `openclaw agents add freely --workspace ~/.openclaw/workspace-freely`
   - `openclaw hooks enable <freely相关hook>`
   - 配置 cron 周期唤醒
6. 在目标项目仓库继续保留 Freely 的治理脚本（如 worktree/hook gate），由 OpenClaw skills 去调用

这条路径满足“**不改 OpenClaw 源码**”，同时最大化复用 OpenClaw 现有能力。

---

## 最终判定

- 若你的约束是“**除了 `workspace-freely` 目录，其他路径完全不可变**”：  
  **不可完整实现 Freely。**
- 若你的约束是“**不改 OpenClaw 源码，但允许用 OpenClaw 官方配置机制**”：  
  **可以把 Freely 产品化为 OpenClaw 的子功能画像，且有较高可行性。**

