---
b1_id: B1-20261103T111400Z
phase_state: completed
source_raw: raw-20261103T111400Z
source_url: https://github.com/chatterzhao/freely/issues/4141
produced_candidate: C-20261103T111400Z-A
created_at: 2026-11-03
---

# B1_IBM: 物化 open raw 文档并回填历史 platform_ids

## Input
- 前置 lane（raw-20261103T091157Z）已把双平台 open 集合对齐为 13=13，并关闭 4 个 Gitee 漂移镜像；但按 GATE 1（一个工位一个 raw issue），跨 raw key 的文档物化/回填无法并入该 lane。
- 当前事实：13 个 open raw key 无本地 `docs/B1-docs/raw-{key}/issue.md`；13 个历史本地 raw 文档缺平台编号（`platform_ids` 不全）。
- 用户要求：open issue 必须本地可追溯且记录双平台编号；历史编号按证据回填，不猜测、不批量补建历史 issue。

## Option A: 等每个 issue 实现 lane 时各自物化（否决）
- 每个 open issue 的 wt-create 会物化自己的 raw 文档，但 13 个 issue 全部开工前 parity 校验持续 FAIL，且历史 13 个文档编号缺口永远没有 lane 承接。

## Option B: 单独 docs-only 治理 lane（选定）
- 一个 fix 工位只改 `docs/`；用 `FREELY_SKIP_IBM_GATE` 合法跳过 IBM 文档门禁（AGENTS.md 唯一合法豁免），因为变更全部是治理文档、不含代码。
- 物化：`platform-adapter.py pull <key> <target>`（经修复后的分页搜索解析双平台副本），写入 platform_ids。
- 回填：按 `[RAW-key]` 标题前缀唯一匹配平台 issue 后写回编号；多匹配不猜。
- 验收：`test-platform-open-parity.py --require-local-docs`（开发态 RED：13 个 open key 缺本地文档；物化+回填后 GREEN）。

## Decision
- Option B。边界：只改 docs/；不创建历史 issue、不删平台 issue、不改代码。

## Candidate
- candidate_id: C-20261103T111400Z-A；milestone: M-20261103T111400Z-A
