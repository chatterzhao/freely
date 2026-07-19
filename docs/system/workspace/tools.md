# Workspace Tools

本文件定义 Freely 当前可用的外部 AI 工具清单，供 `manager`、`worker` 与 `freely-context-source-skill` 读取。

## Routing Principle

- Freely 负责提示词组装与外部 AI CLI 编排。
- Freely 不在脚本里硬编码“命中某条件就必须走某工具”。
- AI 必须读取当前输入、任务强度、工具优先级、工具可用性，再自主决定下一跳工具。

## Runtime Availability Note

- `tools.md` 继续只定义任务路由与工具选择参考，不直接充当 runtime availability fallback 顺序真源。
- 当前 runtime-owned availability manager 使用 project config 中的 `AI_FALLBACK_TOOLS` 作为 ordered recovery list，而不是复用本文件的 routing priority。
- canonical recovery order 是：
  - `AGENT_AI_TOOL`（来自 `.freely/agent-table.toml`）是 current tool+slot 真相；AI_TOOL 已移除，由 load_config 自动从 AGENT_AI_TOOL 派生
  - 同工具 slot / profile recovery first
  - same-tool exhausted 后再从 `AI_FALLBACK_TOOLS` 最左侧开始重新扫描其他工具，而不是把 current tool 隐式插到最前
  - 每进入一个 fallback tool，先继续扫该工具自己的 slot family，再决定是否进入下一个工具
  - 全部不可用时保持 no-launch，并把 earliest-reset target 写成显式 `tool + slot` waiting truth
- runtime work-loop 的切换 contract 是统一的：
  - 各工具可以有不同的错误关键词 / 失败证据
  - 但一旦命中“当前工具这轮工作失败”，统一进入同一条 slot-first / cross-tool fallback recovery path，而不是按 rate-limit、auth、network 分叉多套 switch 方法
- execution-time network taxonomy 也是 runtime-owned truth：
  - `oauth_unreachable` 继续只表示 preflight / inventory 阶段的 launch blocker
  - `execution_network_transient`、`execution_network_persistent`、`proxy_config_invalid` 表示运行中的 network-local failure
  - 这三类 network-local failure 默认不触发 slot rotation 或 cross-tool fallback，而是在当前 `tool + slot` 上执行 bounded retry / cooldown
- 当前已存在 canonical probe-first / switch-lock / no-launch watchdog truth 的工具仍主要是 `codex`；其他工具现已进入统一 slot inventory / current-slot scheduler，但若缺 probe parity，仍以较弱 readiness contract 参与 slot-first recovery，不能冒充与 Codex 等价。

## Runtime Adapter Note

- Freely runtime 已把“工具选择”和“adapter 选择”拆成两个独立轴，当前工作模式以 ACP 为准。
- 当前 canonical truth 是：
  - `AGENT_AI_TOOL`（agent-table.toml）表示选中的外部工具+slot；AI_TOOL 已移除，由 load_config 自动派生工具族名
  - `AGENT_AI_TOOL_ADAPTER_POLICY` 表示该工具期望采用哪条接入策略；当前正常运行值为 `acp`
  - `AGENT_AI_TOOL_ADAPTER` 表示 runtime 依据 policy 和当前支持面解析出的实际 adapter
  - status / introspection 还会暴露当前工具的 `tool_supported_adapters`，作为当前 runtime 支持矩阵
- 当前 runtime 默认 adapter 是 `acp`；`direct` 属于遗留兼容/历史测试路径，不再作为 Freely 的产品工作模式描述。
- 当前 canonical ACP family 来自 `docs/system/workspace/tools/tool-registry.toml`：
  - `claude` 通过 `claude-agent-acp` 接入；`cc`、`cc-use-codex-cli`、`kiro-cli`、`iflow`、`claude-code` 是该 family 的 registry alias
  - `codex` 通过 `codex-acp` 接入
  - `opencode` 通过 `opencode acp` 接入
- 当前 runtime 已冻结一条选择语义：
  - 同工具重选时，继续保留当前 `AGENT_AI_TOOL_ADAPTER_POLICY` 和 `AGENT_AI_TOOL_ADAPTER` truth，不因重写 config 或恢复写回而静默回到默认值
  - 同工具 mutation 时，继续保留该工具当前 `AI_MODEL` / `AI_REASONING_EFFORT` truth，不因只换 adapter 或重写选择而回到工具默认值
  - 只有跨工具切换时，才回落到目标工具自己的 default adapter policy，除非显式给出 adapter / policy override
- 当前显式配置入口包括：
  - `freely init --tool-adapter <adapter> [--tool-adapter-policy <policy>]`
  - `freely set-tool --tool <tool> [--tool-adapter <adapter>] [--tool-adapter-policy <policy>]`
- 当前 runtime 主路径是：`monitor-ai-acp.sh` → `run-acp-prompt.py` → `acp-bridge.py` → 外部工具 ACP adapter。
- `direct` / `prefer_acp_fallback_direct` 只属于 legacy compatibility 术语；新能力设计、SVG 和运行时语义以 ACP 主路径为准。

## Runtime Security Review Note

- Freely runtime 现在开始显式暴露 project-local security review truth，但这一层仍然是 advisory capability，不是新的 launch blocker。
- `freely doctor` 现在也承接 machine-enforced baseline security audit slices，而不只靠人工记忆；当前已 canonical 的自动化 slice 包括 execution-boundary audit、build artifact exposure audit、以及 supply-chain/install-intake baseline audit。
- 当前 canonical truth 是：
  - `FREELY_SECURITY_REVIEW_POLICY` 表示项目希望如何触发内部安全评审，首批默认值为 `advisory-on-high-risk-or-uncertainty`
  - `FREELY_SECURITY_REVIEW_SCOPE` 表示当前冻结的 review scope，首批默认值为 `execution-boundary-and-reviewer-support`
- 这两个 truth 目前只进入：
  - project-local config
  - `freely baseline-status`
  - `freely live-status`
  - `freely doctor`
- 它们当前不直接改变：
  - launch flags
  - approval posture
  - adapter selection
  - fallback routing
- 真正的 reviewer / committee runtime 若要 materialize，应以后续 owner 单独承接，而不是在这条 advisory baseline 里偷渡。

## Local Boundary Contract

- Freely 把“项目根目录”和“sibling worktrees 根目录”视为两个不同的本地边界：
  - project root 是 integration / merge / runtime bootstrap surface
  - sibling `{project}-worktrees` root 是 owner development surface
- 项目级工具配置按工具解耦：
  - `codex` 走 `codex-acp`，并继续使用 project-local `.codex/config.toml` / `.freely/bin/codex` 边界材料
  - `claude` family 走 `claude-agent-acp`；`cc`、`kiro-cli`、`iflow` 等 registry alias 复用 Claude ACP family 的接入面
  - `opencode` 走 `opencode acp`，并通过 `OPENCODE_CONFIG` 等 slot/materialization truth 注入项目边界
- 新 worktree 不依赖 Git 复制 ignored / untracked local files：
  - 标准入口 `wt-create` 和 protected-branch auto-worktree hook 会调用 `freely sync-tooling --source-project <root> --project <worktree>`
  - `sync-tooling` 先复制最小 `.freely/config.env`，再在目标 worktree 重新 materialize 各工具本地边界

## Available Tools

### iflow

- availability: available
- priority: P1-default
- strengths:
  - 持续多轮推进
  - 非交互 `-p -y` 提示执行
  - 适合首跳自治和研究/文档型收敛
- recommended_when:
  - 需要沿用 `iflow` 这个历史工具名/profile 触发 Claude ACP family
  - 任务仍在理解、收敛、路由、文档编排阶段
- tool-native reference:
  - fresh/auto: `iflow -p "<assembled prompt>" -y --max-turns 100`
  - resume/auto with explicit session file: `iflow -r <session-file> -p "<assembled prompt>" -y --max-turns 100`
  - resume/auto without explicit target: `iflow -c -p "<assembled prompt>" -y --max-turns 100`
  - fresh/step: `iflow -p "<assembled prompt>" --default --max-turns 100`
- runtime_notes:
  - Freely runtime currently routes `iflow` as a registry alias of the `claude` ACP family, so runtime session/fork/resume behavior comes from `claude-agent-acp`, not from `iflow` tool-native CLI resume semantics.
  - Tool-native `iflow --continue` only means recent conversation, not workcell-scoped explicit session addressing.
  - Tool-native `iflow --resume <session-file>` can target a specific session file, but Freely does not use that path as the canonical runtime session mechanism.
  - Freely now treats sibling worktree reachability as a boundary bootstrap concern for `iflow`: runtime launch adds `--add-dir <project-worktrees-root>`, and `freely init` writes a project-local `.freely/bin/iflow` wrapper with the same boundary. This extends the reachable workspace beyond the project root; it does not replace normal project-root access.
  - When a new worktree is created, Freely can rematerialize these local boundaries with `freely sync-tooling --source-project <project-root> --project <worktree>`, so ignored or untracked tool-local files do not get stranded in the primary root.

### codex

- availability: available
- priority: P1-default
- strengths:
  - 工程实现与仓库内读写
  - 在 worktree 中执行开发/文档修改
  - 适合 issue 已较清晰后的持续实现
- recommended_when:
  - 任务已命中 usable issue
  - 需要直接在仓库中进行实现、验证、修文档
- tool-native reference:
  - fresh/auto: `codex exec --skip-git-repo-check -C <project-root> --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
  - fresh/step: `codex exec --skip-git-repo-check -C <project-root> - < <prompt-file>`
  - resume/auto: `codex exec resume <SESSION_ID> --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
  - fresh_with_handoff/auto: `codex exec --skip-git-repo-check -C <project-root> --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
- runtime_notes:
  - Freely runtime launches `codex` through `codex-acp`; first launch downloads the pinned adapter into the Freely ACP cache unless `FREELY_CODEX_ACP_BIN` overrides it.
  - Current ACP path supports `fresh` / `fresh_with_handoff` / `resume` / `fork`; `fresh_with_handoff` is a launch-kind for continuity repair, not the deprecated worker handoffs storage.
  - Current ACP bridge can auto-answer ACP permission requests in `mode=auto`; `AI_REASONING_EFFORT` mapping remains tool/adapter-specific.
  - Freely treats `codex` as an explicit session-addressed resume tool: canonical continuity target is the concrete ACP `sessionId`, not `resume --last`.
  - Codex posture is now split into two layers on purpose:
    - project-local baseline: `freely init` materializes a project-scoped `.codex/config.toml`; in `auto` mode this baseline now writes `approval_policy = "never"` while keeping `sandbox_mode = "workspace-write"` and `network_access = false` as the recommended local defaults
    - launch-time injection: runtime still adds `--dangerously-bypass-approvals-and-sandbox` for current non-interactive auto execution, and now also injects `--add-dir <project-worktrees-root>` so sibling worktrees remain reachable without falling back to editing `develop`; this extends Codex reach beyond the project root, not away from it
  - `freely init` also materializes project-local manual wrappers under `.freely/bin/` for `codex`, `claude`, `iflow`, and `kiro-cli`; for tools with verified extra-dir support, those wrappers inject the canonical sibling `{project}-worktrees` root.
  - `wt-create` and the protected-branch auto-worktree hook now call `freely sync-tooling` after `git worktree add`, so local managed boundaries are regenerated in the new worktree even if `.gitignore` excludes the underlying directories.
  - If the runtime lacks an explicit Codex session target, it must rotate to `fresh_with_handoff` instead of silently falling back to `--last`.
  - Freely runtime may choose `fresh_with_handoff` when the previous Codex session is technically resumable but no longer healthy to keep extending.
  - Current rotation triggers include `context compacted`, missing resume evidence, local `resume_streak` threshold, and high context-window usage.
  - When context-window usage first crosses the local warn threshold, the next prompt should first refresh the phase-appropriate continuity artifact before continuing.
  - Default Codex runtime config is project-scoped `gpt-5.4` with reasoning effort `medium` unless the project explicitly overrides it.

### kiro-cli

- availability: available
- priority: P2-weak-contract
- strengths:
  - 能承接单目录下的连续对话
  - 具备交互式恢复入口
- recommended_when:
  - 需要沿用 `kiro-cli` 这个历史工具名/profile 触发 Claude ACP family
  - 任务可接受该 alias 当前由 Freely registry 映射到 `claude-agent-acp`
- tool-native reference:
  - fresh/auto: `kiro-cli chat --no-interactive --trust-all-tools --model <model> < <prompt-file>`
  - resume/auto: `kiro-cli chat --resume --no-interactive --trust-all-tools --model <model> "继续上次未完成工作，按项目意图和宪法持续推进。"`
  - interactive fallback: `kiro-cli chat --resume-picker`
- runtime_notes:
  - Freely runtime currently routes `kiro-cli` as a registry alias of the `claude` ACP family, so runtime session/fork/resume behavior comes from `claude-agent-acp`, not from `kiro-cli` tool-native CLI resume semantics.
  - Tool-native `kiro-cli --resume` 当前只恢复当前目录最近会话，不是 canonical 的 explicit session-addressed resume。
  - `--resume-picker` 只是人工交互 fallback，不能作为 supervisor/runtime 默认重入路径。
  - 当 cycle log 出现 `Monthly request limit reached` 或 `Unable to verify subscription status: service error` 时，Freely 当前会把它们视为 Kiro availability failure，写入 canonical reason 并停止本地盲目 relaunch，后续 recovery 交回 watchdog / manager control plane。

### cc

- availability: experimental
- priority: P1-default
- strengths:
  - Claude Code 作为顶层 agent 提供会话管理与工具编排
  - 适合作为普通 Claude Code tool，在 Freely 中承接上下文管理、并行 worktree、subagent 和非交互会话
- recommended_when:
  - 需要 `Claude Code` 的 agent/context 管理
- tool-native reference:
  - fresh/auto: `claude -p --permission-mode bypassPermissions --session-id <uuid> "<assembled prompt>"`
  - resume/auto: `claude -p --permission-mode bypassPermissions --resume <session-id> "<assembled prompt>"`
- runtime_notes:
  - `cc` 不默认启用 `codex-cli` MCP；它是 Claude ACP family 的普通 Claude Code profile。
  - Freely runtime launches this family through `claude-agent-acp`; tool-native commands above are manual reference, not runtime launch truth.
  - `cc` 当前没有单独的 project-local tool config materialization；Freely 主要通过 launch-time flags 注入 non-interactive posture，例如 `--permission-mode bypassPermissions`、`--session-id`、以及可选 debug/model/effort parameters。
  - Freely runtime 现在会额外注入 `--add-dir <project-worktrees-root>`，并由 `freely init` 写出对应的 `.freely/bin/claude` wrapper，避免 Claude 在 repo root 会话里因为 sibling worktree 不可达而退回 protected branch 上写；项目根目录本身仍是合法的集成/merge 工作面。
  - 如果新 worktree 是通过标准 Freely 入口创建的，Claude 对应的受管 wrapper 也会在目标 worktree 被重新 materialize，而不依赖 Git 复制 ignored local files。
  - Freely 会为每个运行中的 workcell 分配独立 `session-id`，降低多 worker / 多 worktree 并发时串会话的风险。
  - `cc` 的 continuity 证据以 `Claude session-id + Claude jsonl + debug/cycle log` 为主。

### cc-use-codex-cli

- availability: experimental
- priority: P1-default
- strengths:
  - 继续使用 Claude Code 作为顶层 agent/context manager
  - 默认强制附带 `codex-cli` MCP policy，让 repo work 优先交给 Codex
- recommended_when:
  - 需要 `Claude Code` 的会话和上下文能力
  - 同时希望 repo 实现、review、verification 默认走 Codex MCP
- tool-native reference:
  - fresh/auto: `claude -p --permission-mode bypassPermissions --session-id <uuid> --append-system-prompt "<fixed codex-cli MCP policy>" "<assembled prompt>"`
  - resume/auto: `claude -p --permission-mode bypassPermissions --resume <session-id> --append-system-prompt "<fixed codex-cli MCP policy>" "<assembled prompt>"`
- runtime_notes:
  - `cc-use-codex-cli` 是固定 profile，不要求用户再单独配置 capability 参数。
  - `cc-use-codex-cli` 是 `claude` ACP family 的 registry alias，主要通过 launch-time materialization 工作，而不是写独立 project-local Claude config。
  - Freely 会固定注入：`model=gpt-5.4`、`sandbox=workspace-write`、`approval-policy=never`；当当前 branch 是 protected branch 时，system prompt 会明确区分 project root 的 read/merge/integration 用途，与 owner development 的 dedicated worktree 用途，并同步为 Claude 注入 `--add-dir <project-worktrees-root>`。
  - 每个 running workcell 使用独立 `Claude session-id`，降低多 worker / 多 worktree 并发时的会话串线风险。
  - 证据模型分两层：
    - 外层：`Claude session-id`、`Claude jsonl path` 与 `cycle/debug log`
    - 内层：`Codex threadId` 与 `Codex jsonl path`
  - `Codex threadId` 优先从 `Claude jsonl` 的 `mcp__codex-cli__codex` tool result 提取，而不是仅依赖 debug log 或时间窗口猜测。

## Selection Policy

- AI 应根据当前输入判断任务强度：
  - routing/research/doc-convergence
  - issue-materialization/doc-loop
  - implementation/dev-loop
- AI 应优先选择当前可用且最匹配任务强度的工具。
- 若多个工具都可用，优先选择更接近当前阶段的工具，而不是固定偏好某一个工具。
- AI 负责产出 `selected_tool`、`why_selected`、`next_prompt` 与 `target_skill_or_loop`。
- 若 `selected_tool` 与当前运行工具一致，AI 不能把 `next_prompt` 当作结束信号；应在当前会话继续执行第二跳，并仅把 `next_prompt` 作为可追溯的中间产物。
- CLI 的具体启动参数由 Freely runtime 统一执行，不要求 AI 自己发明命令格式。
- 输出应包含：
  - selected_tool
  - why_selected
  - next_prompt
  - target_skill_or_loop
