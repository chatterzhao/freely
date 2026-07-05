# Brainstorm: human-chat-intake-and-manager-delegation

## Focus

把 human chat intake 与 manager delegation 的 CLI-first 闭环物化为正式 issue 产物，并保留 pre-brainstorm 中已经稳定的 reaction / absorption 边界。

## Key Decisions

1. raw human chat 先进入 `.freely/intake/**`，而不是直接注入某个 AI 会话。
2. manager 负责 notice / claim / reaction / delegate / absorption target，不负责深度解释。
3. `skill:human-interruption-handling` 负责深度解释、worker handoff 与 resolution artifact。
4. `.freely/intake/**` 是短期事件池，长期 canonical facts 仍回到 `docs/B1-docs/raw-**`、`docs/epics/**`、`docs/progress/**` 与 `docs/recovery/**`。

## Open Checks

1. manager 的自动接线与 verification continuity 是否足以证明这条能力已经被 Freely 自举吸收。
2. `freely intake chat/status/claim/resolve` 与 manager prompt / skill contract 的回写是否保持一致。
