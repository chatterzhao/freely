# Issue: claude-code-codex-mcp-runtime-governance

- issue_id: `I-20260321-0217`
- title: Claude Code tool profiles and Codex MCP session evidence governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `claude-code-codex-mcp-runtime-governance`
- issue-name: `claude-code-codex-mcp-runtime-governance`
- source_candidate: `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/candidates.md#c-20260320-2145-001`
- additional_source_candidates:
  - `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/candidates.md#c-20260320-2145-002`
  - `docs/pre-brainstorms/20260321-0148--cc-codex-session-evidence-resolution/candidates.md#c-20260321-0148-001`
- source_brainstorm:
  - `docs/pre-brainstorms/20260320-2145--cc-tool-profiles-and-concurrent-session-continuity/brainstorms.md`
  - `docs/pre-brainstorms/20260321-0148--cc-codex-session-evidence-resolution/brainstorms.md`
- execution_base: `feature/research-codex-in-cc-mcp`
- integration_target: `feature/research-codex-in-cc-mcp`
- depends_on: `feature/research-codex-in-cc-mcp`
- session_refs:
  - {tool: cc-use-codex-cli, session_id: "11111111-2222-4333-8444-555555555555", jsonl_path: "/Users/zhaoyu/.claude/projects/-private-tmp-freely-cc-codex-real-ed64yw-project/11111111-2222-4333-8444-555555555555.jsonl", role: "integration-smoke"}
  - {tool: codex-cli, session_id: "019d0f86-7c2e-7f50-999f-10cf4935e7ba", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/21/rollout-2026-03-21T01-27-02-019d0f86-7c2e-7f50-999f-10cf4935e7ba.jsonl", role: "integration-smoke"}
  - {tool: cc-use-codex-cli, session_id: "current-worktree-session", jsonl_path: "unavailable://supervisor-cycle-had-not-yet-written-session-state", role: "review-followthrough"}

## Why

Freely 已经支持多个顶层 AI tool，但 `Claude Code` 仍缺两类关键治理能力：

- 明确区分纯 `cc` 与固定 profile 的 `cc-use-codex-cli`
- 在 `cc-use-codex-cli` 下把 `Claude session-id -> Claude jsonl -> Codex threadId -> Codex jsonl` 收敛为可恢复、可并发验证的双层证据模型

如果缺这两层能力，Freely 无法稳定把 `Claude Code` 作为顶层 agent/context manager，同时让仓库实现默认下沉到 `Codex MCP`。

## Scope

1. 为 Freely 增加两个显式顶层工具：`cc` 与 `cc-use-codex-cli`
2. 让 `cc-use-codex-cli` 固化 `codex-cli` MCP policy，而不是把 capability 参数暴露给用户侧
3. 去掉 interruption / signal 等旁路对 `codex exec` 的硬编码，统一走 tool launcher
4. 为 `cc` / `cc-use-codex-cli` 建立 per-workcell `Claude session-id` continuity
5. 增加 `session-evidence-resolver.sh`，精确反查 `Claude jsonl` 与 `Codex jsonl`
6. 补齐对应脚本级回归与 live smoke evidence

## Acceptance

- `freely init --ai cc:auto` 生成纯 `Claude Code` profile
- `freely init --ai cc-use-codex-cli:auto` 生成固定 `Codex MCP` profile
- `monitor`、`interruption-manager-handler` 与 `signal-intent-handler` 不再硬编码 `codex exec`
- `cc` / `cc-use-codex-cli` 使用独立 `Claude session-id` 维持多 worktree / 多 worker continuity
- Freely status 能显示 `Claude jsonl path`、`Codex threadId` 与 `Codex jsonl path`
- `cc-use-codex-cli` 的真实 smoke 能看到 `MCP server "codex-cli": Calling MCP tool: codex`

## IBM Handoff

- implementation_scope_summary:
  - 承接已落盘的 `cc` / `cc-use-codex-cli` runtime、fixed Codex MCP policy、session evidence resolver 与脚本级回归。
  - 进入后续收口时不要再把 capability 设计回退成用户手工拼参数；保持 `cc-use-codex-cli` 作为固定 top-level profile。
  - merge 路径必须尊重派生关系：当前 issue 先回收进 `feature/research-codex-in-cc-mcp`，父分支通过 review 后再决定是否继续进入 `develop`。
- required_doc_refs:
  - `docs/system/workspace/tools.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - `docs/system/workspace/scripts/runtime/session-evidence-resolver.sh`
  - `docs/system/workspace/scripts/monitor-ai-cli.sh`
  - `docs/system/workspace/scripts/runtime/interruption-manager-handler`
  - `docs/system/workspace/scripts/runtime/signal-intent-handler`

## Completion

- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/runtime/session-evidence-resolver.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- `docs/system/workspace/scripts/runtime/interruption-manager-handler`
- `docs/system/workspace/scripts/runtime/signal-intent-handler`
- `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `docs/system/workspace/scripts/tests/test-session-evidence-resolver`
- `docs/system/workspace/scripts/tests/test-freely-cc-codex-evidence-status`
- `docs/system/workspace/scripts/tests/test-freely-session-rotation`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `bash docs/system/workspace/scripts/tests/test-session-evidence-resolver`
- `bash docs/system/workspace/scripts/tests/test-freely-cc-codex-evidence-status`
- live smoke:
  - `./bin/freely init --ai cc-use-codex-cli:auto`
  - `./bin/freely start`
  - inspect `.freely/logs/cycle-*.debug.log` for `MCP server "codex-cli": Calling MCP tool: codex`

## Next

- 当前 issue 已有实现与验证证据，但依赖父分支 `feature/research-codex-in-cc-mcp`；下一步先检查当前分支能否无冲突合回父分支。
- 若父分支 review / governance / ancestry 仍未完成，则继续在父分支层面收口，不得跳过上游直接 merge 到 `develop`。
