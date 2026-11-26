# PRD: raw-20261125T122804Z
## Goal
让 raw-reconciliation 只比较生命周期语义与人类正文，不把从 frontmatter 派生的 `| updated |` 时间戳当内容分歧。

## 实现方案
在 `raw_reconciliation._body()` 中，去掉注释块后对 `| updated | ... |` 行做值归一化（统一为固定占位），其余文本不变。纯 stdlib、零 I/O；不新增写通道。

## Dev-Loop Handoff
RED（develop 无归一化，updated-only 差异被误判）→ GREEN（归一化后 ok，正文差异仍 blocked）。
