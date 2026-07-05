# Pre-Tests: manager-chat-reentry-and-cleanup-misrouting-governance

1. supervisor-level chat 不再输出 `RESTART_POINT=cleanup`。
2. cleanup-only chat 仍输出 `RESTART_POINT=cleanup`。
3. runtime 通过 `freely chat` 处理 broad supervisor request 时，intake 最终是 `delegated`，且 `ABSORPTION_TARGET="handoff://continuation"`。
