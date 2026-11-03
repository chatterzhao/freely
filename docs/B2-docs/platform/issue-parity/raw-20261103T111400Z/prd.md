# PRD: open raw 文档物化与历史 platform_ids 回填

- issue_id: I-20261103T111400Z-A

## Goal
13 个 open raw issue 本地可追溯（docs/B1-docs/raw-{key}/issue.md + 双平台编号），13 个历史本地文档补齐已有平台副本的编号；parity --require-local-docs GREEN。

## Modules
- docs/B1-docs/raw-{open key}/issue.md（新增 13 个）
- docs/B1-docs/raw-{历史 key}/issue.md（13 个平台编号回填）
- 无代码变更。

## Invariants
- 编号回填仅在 `[RAW-key]` 标题前缀唯一匹配时发生。
- 不创建历史 issue、不删除平台 issue。
- 变更仅限 docs/。

## Eval Plan
- parity --require-local-docs：RED（13 个 open key 缺文档）→ GREEN。
- 编号一致性由同一测试校验（记录编号与平台实际编号逐项比对）。

## Dev-Loop Handoff
先记录 RED（develop 上 parity --require-local-docs 失败），再物化/回填，最后 GREEN。
