# PRD

## Goal

让 Freely 对 generic-subject 的 protected-ancestry receipt gap 也保持可审计，但不把 ordinary receipt-gap ledger 退化为 hash 白名单。新的 contract 必须显式证明：某个 trailerless ancestry merge 是被一个 trailer-bearing protected batch merge 吸收的同一受治理链路，而不是任意历史 merge。

## Requirements

1. 在现有 ordinary receipt-gap surface 上定义一个显式的 stronger-evidence path，或证明单独 ledger 更安全。
2. `governance-check` 必须将 unparseable-subject ancestry gap 与 parseable-subject gap 分开验证。
3. 新路径必须要求 batch-level absorbing merge truth、bounded owner truth、verification truth。
4. 旧路径必须保持不变：parseable subject 仍然按 subject/source/target 精确比对。
5. malformed、under-evidenced、wrong-batch 的新条目必须 fail closed。
6. 当前 April 10 preferred-auth ancestry chain 要能在新 contract 下通过，而不是靠破坏旧 contract 兜底。

## Non-Goals

- 不接受 hash-only backfill
- 不改写历史 merge commit
- 不把普通 evidence_refs 解释成隐式 schema
- 不扩到 break-glass receipt policy
- 不处理与 preferred-auth bug fix 本身无关的实现范围
