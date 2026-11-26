# PRD: raw-20261125T065112Z
## Goal
让 wt-close 的文档、提示与 linked schema 判据与当前 write-free 单入口实现一致。
## 实现方案
改三份文档；在 governance-merge-gate 增 `_validate_linked_strict_frontmatter`，仅对本次改动触及的 linked I-* 强制 YAML block + schema_version；新增 AT 锁住文档与提示。
## Dev-Loop Handoff
RED 1/9 → GREEN 10/0；不改平台写通道，不改 wt-close 运行时逻辑。
