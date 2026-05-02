# Brainstorms

## Topic

- 为 `cc` / `cc-use-codex-cli` 增加可精确恢复的会话证据解析能力：
  - `Claude session-id`
  - `Claude jsonl path`
  - `Codex MCP threadId`
  - `Codex jsonl path`

## Problem

- 当前 runtime 已经能稳定记录：
  - `Claude session-id`
  - `Codex MCP used`
- 但 `Claude jsonl path`、`Codex threadId`、`Codex jsonl path` 仍未被 Freely 自动解析回写。
- 之前的保守判断是：`Claude Code` 外层不稳定暴露 `Codex threadId/jsonl`，所以 runtime 只能先记录 `unavailable://...`。
- 这会让后续恢复、handoff、并发 worker 证据都偏弱。

## New Finding

- 本机真实验证说明，`Claude jsonl` 已经足够作为主解析源：
  - `~/.claude/projects/<sanitized-project>/<session-id>.jsonl`
- 同一份 `Claude jsonl` 中已经包含：
  - `sessionId`
  - `cwd`
  - `mcp__codex-cli__codex` tool use
  - 对应 `tool_result`
  - `tool_result.mcpMeta.structuredContent.threadId`
- 这意味着：
  - `Codex threadId` 不需要靠 debug log 猜
  - 也不需要靠启动时间扫目录猜
  - 可以先用 `Claude session-id` 精确定位 `Claude jsonl`
  - 再从 `Claude jsonl` 精确提取 `Codex threadId`
  - 最后用 `threadId` 精确反查 `~/.codex/sessions/**`

## Converged Resolution

- 主解析链路应改为：
  1. Freely 启动 `cc` / `cc-use-codex-cli` 时，已有：
     - `project root`
     - `Claude session-id`
  2. 直接构造并解析 `Claude jsonl path`
  3. 从 `Claude jsonl` 提取：
     - 是否命中过 `mcp__codex-cli__codex`
     - 最新 `threadId`
  4. 用 `threadId` 反查 `Codex jsonl path`
  5. 回写到 session state / status / handoff

## Why This Is Better Than Timestamp Matching

- 时间窗口匹配只能做 fallback，不应做主方案。
- 真正的稳定主键已经存在：
  - `Claude session-id`
  - `Codex threadId`
- 这对以下场景更稳：
  - 多 worktree
  - 多 worker
  - manager / worker 并发
  - 同一台机器多个 `Claude` 会话同时运行

## Intended Runtime Shape

- 新增硬模块，而不是只做 skill：
  - `runtime/session-evidence-resolver.sh`
- 它负责：
  - `sanitize_claude_project_key(project_root)`
  - `find_claude_jsonl_for_session(project_root, claude_session_id)`
  - `extract_codex_thread_id_from_claude_jsonl(claude_jsonl_path)`
  - `find_codex_jsonl_for_thread(thread_id)`
- Freely runtime/watchdog 在工具进程结束后调用它，必要时也可在 status/watchdog 路径中重算。

## Evidence Model

- `cc` / `cc-use-codex-cli` 未来统一采用四字段证据：
  - `claude_session_id`
  - `claude_jsonl_path`
  - `codex_mcp_thread_id`
  - `codex_mcp_jsonl_path`
- 若任一层不存在，必须显式写 `unavailable://...` 原因，不允许静默留空。

## Recovery Use

- 恢复和 handoff 不应该把整份 jsonl 重喂给提示词。
- 正确做法是把这些路径作为引用证据写入：
  - `previous_claude_session_id`
  - `previous_claude_jsonl_path`
  - `previous_codex_thread_id`
  - `previous_codex_jsonl_path`
- 需要时再让后续 skill / agent 定位并读取局部片段。

## Acceptance Hint

- 一次真实 `cc-use-codex-cli` 运行后，Freely status 至少应显示：
  - `claude_session_id_current`
  - `last_claude_jsonl_path`
  - `last_codex_mcp_used=1`
  - `last_codex_mcp_thread_id=<thread-id>`
  - `last_codex_mcp_jsonl_path=<exact-jsonl-path>`
- 多 worktree / 多 session 情况下，不应串到错误 jsonl。
