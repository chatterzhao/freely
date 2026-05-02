# PRD

## Goal

让 Freely 在 sandboxed operator session 里，即使默认 `$FREELY_HOME` 不可写、`/bin/ps` 不可用，也仍能通过合法的 project-scoped runtime path 继续 bootstrap、status 和 interruption routing，而不是把人或 agent 逼回 protected root 上写。

## Requirements

1. 默认 global operator home 不可写时，Freely 必须能得到一个明确且可审计的 fallback operator-state root。
2. fallback 不能模糊 global/shared state 与 project-scoped bootstrap state 的边界。
3. process discovery/readiness 在 `ps` 不可用时必须降级，而不是把 `start/status/live-status/chat` 直接判成 generic command failure。
4. 降级模式仍要保留最小可信证据：
   - pid file
   - session state
   - prompt / continuity / intake artifacts
   - 明确的 degraded / unavailable 标记
5. 任何降级都不能放宽 protected branch owner-development 约束。

## Non-Goals

- 不扩展到 generic Git sandbox bypass
- 不重开 global restart manifest 设计
- 不重做 worktree tool boundary bootstrap
- 不承诺在无进程探测能力时仍提供完整 process snapshot
