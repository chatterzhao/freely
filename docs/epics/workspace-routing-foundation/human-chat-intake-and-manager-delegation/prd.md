# PRD: human-chat-intake-and-manager-delegation

## Problem

Freely needs CLI-first human chat intake as a formal discovery and continuation source, but the intake must stay durable, manager-visible, and route back into the same governance loops instead of bypassing them.

## Product Requirement

Human chat intake must write durable intake artifacts, let the manager notice/claim/classify them, and hand off to `human-interruption-handling` for resolution and canonical absorption guidance.

## Non-goals

- Do not let human chat bypass pre-brainstorm / issue / continuation routing
- Do not let the human-side CLI directly claim or resolve intake items
- Do not create a second state store outside `.freely/intake/**`
