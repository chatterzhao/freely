# PRD: token-efficient-session-continuity-and-rotation-governance

## Goal

让 Freely 在 context pressure 下优先保住高质量 continuity，再以低 token 的方式进入 `fresh_with_handoff` 或恢复流程。

## Requirements

1. 统一 `context warn`、`context rotate`、`fresh_with_handoff`、continuity artifact 与旧会话证据引用的正式边界。
2. 明确 manager continuity 与 worker continuity 的默认目标对象、最小内容和 owner。
3. handoff 默认只携带 continuity artifact、结构化 handoff 与旧证据路径引用，不默认重喂整份旧 `jsonl` / cycle log。
4. watchdog 只负责 availability/runtime 恢复，不负责替 AI 做语义压缩。
5. 形成一份统一的 `trigger -> owner -> artifact -> action -> fallback` 矩阵，供 runtime / skill / prompt 共享。
6. 正式写明“官方若公开非交互压缩能力，应优先评估并重构采用”的演进规则。
