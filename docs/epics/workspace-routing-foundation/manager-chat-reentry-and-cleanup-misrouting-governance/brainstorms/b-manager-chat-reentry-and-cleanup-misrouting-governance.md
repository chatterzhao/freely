# Brainstorm: manager-chat-reentry-and-cleanup-misrouting-governance

## Freeze

- cleanup-only 请求与 broad supervisor audit 必须分流
- broad supervisor audit 不应直接触发 cleanup worker
- broad supervisor audit 应 delegated 到 `handoff://continuation`，由主管下一轮继续 project-level patrol

## Minimal Fix Surface

1. `interruption-manager-handler` prompt wording
2. handler regression
3. runtime intake -> delegated continuation regression
