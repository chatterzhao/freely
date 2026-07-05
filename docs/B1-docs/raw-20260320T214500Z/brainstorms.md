# Brainstorms

## Topic

- 在 Freely 中把 `Claude Code` 收敛为两个明确顶层 tool：
  - `cc`
  - `cc-use-codex-cli`
- 同时解决多 worktree / 多 worker 并发下的 continuity 串线问题。

## Problem

- 之前的实现把 `cc + codex-cli capability` 作为内部参数拼装，用户仍需理解 capability/profile。
- `cc` 的 resume/fresh-with-handoff 判断一度沿用了顶层 `codex` 的 `LAST_TOOL_SESSION_ID` 证据，这对 `Claude Code` 不成立。
- `cc-use-codex-cli` 的目标不是替换 `Claude Code` 的底层 provider，而是在 `Claude Code` 内部稳定优先调用 `Codex MCP`。
- 如果没有并发隔离，多个 worker/worktree 同时使用 `cc` 时容易串会话。

## Converged Decision

- 对外暴露两个顶层 tool，而不是让用户自己拼 capability：
  - `cc`
    - 纯 `Claude Code`
    - 默认 `--permission-mode bypassPermissions`
    - 不默认附带 `codex-cli` policy
  - `cc-use-codex-cli`
    - 顶层仍是 `Claude Code`
    - 固定附带 `codex-cli` MCP policy
    - 固定注入：
      - `model=gpt-5.4`
      - `sandbox=workspace-write`
      - `approval-policy=never`
      - `cwd=project-root`

## Provider Boundary

- `cc` 要先有可用 provider 才能工作。
- 当前本机已验证的可用路径是：
  - `Claude Code -> CCR -> 第三方 provider`
- `Codex MCP` 不能单独替代 `Claude Code` 主 provider。
- `cc-use-codex-cli` 的真实语义是：
  - 继续使用 `Claude Code` 的会话、上下文、agent/tool orchestration
  - 仓库实现工作默认优先下沉给 `codex-cli` MCP

## Concurrency Conclusion

- 不再把隐藏的 `Codex threadId` 当当前阶段的阻塞项。
- 当前阶段对多并发的稳定做法是：
  - 每个 running workcell 分配独立 `Claude session-id`
  - `resume` 时沿用同一个 `session-id`
  - `fresh_with_handoff` 时轮换到新 `session-id`
- 这样可以覆盖：
  - 多 worktree 并发
  - 多 worker 并发
  - manager / worker 各自独立 continuity
- `Codex MCP` 若在 `Claude` 内部被调用，其 continuity 先作为该 `Claude session-id` 的内层行为处理。

## Evidence Model

- `cc` / `cc-use-codex-cli` 采用双层 evidence：
  - `Claude` 外层 evidence
    - `Claude session-id`
    - cycle log
    - debug log
  - `Codex MCP` 内层 evidence
    - 是否命中过 `Codex MCP`
    - 若外层未暴露 `thread_id/jsonl_path`，则显式记为 `unavailable://...`
- 这比“字段留空”更重要，因为空值无法区分：
  - 尚未调用
  - 上游未暴露
  - runtime 漏记

## Runtime Mapping

- `tool=cc`
  - `claude -p --permission-mode bypassPermissions --session-id <uuid>`
- `tool=cc-use-codex-cli`
  - `claude -p --permission-mode bypassPermissions --session-id <uuid> --append-system-prompt "<fixed codex-cli policy>"`
- `auto` 模式的免交互语义：
  - `Claude Code`: `bypassPermissions`
  - `Codex MCP`: `approval-policy=never`

## Why Not Hidden Thread First

- 公开资料表明 `Codex MCP` 底层存在 `thread_id`，但 `Claude Code` CLI 外层不稳定暴露它。
- 直接把 runtime 续接绑定到隐藏 `thread_id`，会让并发治理依赖不可控的上游可见性。
- `Claude session-id` 是当前更稳定、可脚本化、可验证的并发隔离锚点。

## Implemented Outcome

- `parse_ai_spec()`、`start-lead-agent.sh` 已支持：
  - `cc`
  - `cc-use-codex-cli`
- `monitor-ai-cli.sh` / `tool-launchers.sh` 已支持：
  - `--claude-session-id`
  - `cc` / `cc-use-codex-cli` 的差异化固定参数
- `interruption-manager-handler` 和 `signal-intent-handler` 已不再硬编码 `codex exec`
- `Freely` session state 已新增：
  - `CLAUDE_SESSION_ID_CURRENT`
  - `CLAUDE_SESSION_ID_PREVIOUS`
- `select_launch_kind` 已改为：
  - `codex` 看 `LAST_TOOL_SESSION_ID`
  - `cc` / `cc-use-codex-cli` 看 `CLAUDE_SESSION_ID_CURRENT`

## Verification

- 配置/参数测试：
  - `test-freely-init-cc-config`
  - `test-freely-init-ai-default-precedence`
  - `test-monitor-ai-cli-cc-args`
- 中断链测试：
  - `test-interruption-manager-handler-cc`
  - `test-signal-intent-handler-cc`
- continuity/rotation 测试：
  - `test-freely-session-rotation`
- 真实烟测先前已证明：
  - `Freely -> cc` 可启动和接收插话
  - 独立 `claude -p` 调用里，`cc-use-codex-cli` 确实可触发 `Codex MCP`

## Remaining Non-Blocking Enhancement

- `Codex MCP threadId` 若后续能从稳定接口拿到，可再作为增强型 evidence 写入 runtime。
- 当前阶段不再把它当多并发稳定性的前置条件。
