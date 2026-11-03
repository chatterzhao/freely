---
b1_id: B1-20261103T091157Z
phase_state: completed
source_raw: raw-20261103T091157Z
source_url: https://github.com/chatterzhao/freely/issues/4138
produced_candidate: C-20261103T091157Z-A
created_at: 2026-11-03
---

# B1_IBM: 双平台 open issue 对齐与本地 raw 元数据回填

## Input
- raw-20261103T091157Z：走规范 feedback/wt-create/pr-*/wt-close 后，双平台 issue 仍不对齐。
- 审计事实：GitHub 2623 issues（open 14）、Gitee 488 issues（open 18）；4 个 open issue 仅存在于 Gitee（raw-20260715T131531Z / 20260718T035754Z / 20260719T054212Z / 20260720T032133Z）；本地 780 个 raw 文档中 574 缺 Gitee 编号、30 缺 GitHub 编号；13 个 open issue 尚无本地 raw 文档。
- 按月分布显示根因：2026-05 GitHub 1572 条 / Gitee 2 条，2026-07 Gitee 234 条 / GitHub 229 条——历史阶段交替以单平台为主，从未系统性双平台镜像；本地 platform_ids 也未回填。

## Brainstorm
### Option A: 为历史 closed issue 批量补建缺失镜像，追求两平台总数完全相等
- 需要为 ~2100 个 GitHub-only 历史 issue 在 Gitee 补建、并为 ~600 个本地文档补建平台副本。
- 否决：这些多为 2026-05/06 的 closed 历史；批量补建只制造重复归档、污染 Gitee，且没有生命周期价值；总量相等不是 Freely 设计目标（平台是投影，不是独立真相源）。

### Option B: 以"活跃面"为对齐目标：open 集合相等 + open issue 全部本地物化且双平台编号可追溯 + 已有平台副本的本地文档回填编号（选定）
- 对 4 个 Gitee-only open：逐个核对 GitHub 孪生 issue，发现其 GitHub 副本均已于 2026-07 closed（#3915/#3990/#3999/#4040）→ 判定为平台漂移，关闭 Gitee 镜像并写明理由。
- 对 13 个双平台 open：用 adapter pull 物化本地 raw 文档，记录双平台编号。
- 对本地文档缺编号但平台副本存在的：按 `[RAW-key]` 标题前缀唯一匹配回填编号。
- 修 Gitee `search_raw_issue` 只扫第一页（50 条）的缺陷——它正是历史镜像无法被身份解析、导致漂移未被发现的原因。
- 历史 closed 总量差异作为已知遗留债记录，不做批量补建。

### Option C: 只关 4 个 Gitee-only open
- 否决：open 数会相等，但 open issue 仍无本地文档、元数据缺口仍在，下次扫描/收口仍会漂移。

## Decision: Option B
- 对齐口径：open 集合按 raw key 完全相等；每个 open issue 有本地 raw 文档且 platform_ids 双平台编号与平台实际编号一致；平台已存在的副本必须被本地文档记录。
- 不做：历史批量补建、平台 issue 删除、改变既有生命周期语义。

## 不做
- 不批量补建 2026-05/06 的 closed 历史镜像。
- 不删除任何平台 issue。
- 不改 scan 分类与 gate 语义。

## Candidate
- candidate_id: C-20261103T091157Z-A
- status: promoted
- milestone: M-20261103T091157Z-A
