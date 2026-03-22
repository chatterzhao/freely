# Workspace Tools

本文件定义 Freely 当前可用的外部 AI 工具清单，供 `lead-agent` 与 `context-source-skill` 读取。

## Routing Principle

- Freely 负责提示词组装与外部 AI CLI 编排。
- Freely 不在脚本里硬编码“命中某条件就必须走某工具”。
- AI 必须读取当前输入、任务强度、工具优先级、工具可用性，再自主决定下一跳工具。

## Available Tools

### iflow

- availability: available
- priority: P1-default
- strengths:
  - 持续多轮推进
  - 非交互 `-p -y` 提示执行
  - 适合首跳自治和研究/文档型收敛
- recommended_when:
  - 任务仍在理解、收敛、路由、文档编排阶段
  - 需要较长 prompt 驱动下一跳工作
- example:
  - fresh/auto: `iflow -p "<assembled prompt>" -y --max-turns 100`
  - resume/auto with explicit session file: `iflow -r <session-file> -p "<assembled prompt>" -y --max-turns 100`
  - resume/auto without explicit target: `iflow -c -p "<assembled prompt>" -y --max-turns 100`
  - fresh/step: `iflow -p "<assembled prompt>" --default --max-turns 100`
- runtime_notes:
  - `iflow --continue` only means recent conversation, not workcell-scoped explicit session addressing.
  - `iflow --resume <session-file>` can target a specific session file, but Freely does not yet materialize it as a canonical per-workcell resume target.
  - Until that materialization exists, `iflow` remains a weaker continuity contract than `codex` / `cc`.

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
- example:
  - fresh/auto: `codex exec --skip-git-repo-check -C <project-root> --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
  - fresh/step: `codex exec --skip-git-repo-check -C <project-root> - < <prompt-file>`
  - resume/auto: `codex exec resume <SESSION_ID> --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
  - fresh_with_handoff/auto: `codex exec --skip-git-repo-check -C <project-root> --dangerously-bypass-approvals-and-sandbox - < <prompt-file>`
- runtime_notes:
  - Freely treats `codex` as an explicit session-addressed resume tool: canonical continuity target is the concrete `SESSION_ID`, not `resume --last`.
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
  - 当前任务不要求并发安全的 explicit session-addressed resume
  - 可以接受“当前目录最近会话”语义
- example:
  - fresh/auto: `kiro-cli chat --no-interactive --trust-all-tools --model <model> < <prompt-file>`
  - resume/auto: `kiro-cli chat --resume --no-interactive --trust-all-tools --model <model> "继续上次未完成工作，按项目意图和宪法持续推进。"`
  - interactive fallback: `kiro-cli chat --resume-picker`
- runtime_notes:
  - `kiro-cli --resume` 当前只恢复当前目录最近会话，不是 canonical 的 explicit session-addressed resume。
  - `--resume-picker` 只是人工交互 fallback，不能作为 supervisor/runtime 默认重入路径。
  - 因此 `kiro-cli` 当前不应被标记为并发安全的 canonical continuity tool。

### cc

- availability: experimental
- priority: P1-default
- strengths:
  - Claude Code 作为顶层 agent 提供会话管理与工具编排
  - 适合作为普通 Claude Code tool，在 Freely 中承接上下文管理、并行 worktree、subagent 和非交互会话
- recommended_when:
  - 需要 `Claude Code` 的 agent/context 管理
- example:
  - fresh/auto: `claude -p --permission-mode bypassPermissions --session-id <uuid> "<assembled prompt>"`
  - resume/auto: `claude -p --permission-mode bypassPermissions --session-id <same-uuid> "<assembled prompt>"`
- runtime_notes:
  - `cc` 不默认启用 `codex-cli` MCP；它是纯 Claude Code 顶层工具。
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
- example:
  - fresh/auto: `claude -p --permission-mode bypassPermissions --session-id <uuid> --append-system-prompt "<fixed codex-cli MCP policy>" "<assembled prompt>"`
  - resume/auto: `claude -p --permission-mode bypassPermissions --session-id <same-uuid> --append-system-prompt "<fixed codex-cli MCP policy>" "<assembled prompt>"`
- runtime_notes:
  - `cc-use-codex-cli` 是固定 profile，不要求用户再单独配置 capability 参数。
  - Freely 会固定注入：`model=gpt-5.4`、`sandbox=workspace-write`、`approval-policy=never`、`cwd=project-root`。
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
