---
schema_version: '1'
local_id: raw-20261114T034750Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T034750Z-A
platform_ids:
  github:
    issue_id: '4555'
    url: https://github.com/chatterzhao/freely/issues/4555
    synced_at: ''
  gitee:
    issue_id: IKV9SF
    url: https://gitee.com/zhaoquan/freely/issues/IKV9SF
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-parity/raw-20261114T034750Z/issues/I-20261114T034750Z-A.md
last_synced_comment_at:
  github: '2026-11-14T09:13:21Z'
  gitee: '2026-11-14T09:13:21Z'
hash: ''
created_at: '2026-11-14T03:47:50Z'
updated_at: '2026-11-14T09:13:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T034750Z-A
source_candidate: ''
completed_at: '2026-11-14T09:13:20Z'
closeout_note: ''
severity: P1
---

# feat: replica 元数据写在治理文档里与 GATE 1 结构性冲突

workflow_kind: feature

## feat: replica 元数据写在治理文档里与 GATE 1 结构性冲突

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T034750Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T03:47:50Z |
| updated | 2026-11-14T03:47:50Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T034750Z`。实现前请用 `wt-create --raw-key 20261114T034750Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（R33.16 / R33.18 实测）

每次 `issue-sync` 与平台交互，都会改写 issue 文档里的 **replica 元数据**：

- `platform_ids`（新平台 id / url / synced_at）
- `platform_state`（open / closed）
- `last_synced_comment_at`、`updated_at`

一次全量 batch 实测改动 **108 个跨 raw 文档**；一次 daemon 前置 batch 又改动 **58 个**。
这些文件都在 `docs/B1-docs/`、`docs/B2-docs/`——正好是 GATE 1 管辖的治理路径。

结果：
- 在 issue lane 的工位里跑任何同步，都会让工位变脏，PR 无法通过 GATE 1；
- 执行者只能回滚（丢掉平台侧的 id 映射，下次 batch 重复建单）或违规提交；
- R33.18 / R33.16 两轮都被这个摩擦卡住，并诱发了「删 wt-close 检查」「git reset 丢实现」两次偏差。

## 设计张力（不是简单 bug）

两股设计同时成立：

1. `ibm-framework.md`：**本地文档是唯一真相源**；`platform_ids` / `platform_state` 是文档字段，「由 issue-sync create/close 自动管理」；`command-wrapper-metadata-lifecycle.md` 把它们列为**必须有**的元数据（缺失即拒绝进入路由与证据判定）。
2. `docs/LAWS.md` + GATE 1：**一个工位只处理一个 raw**；跨 raw 的文档变更必须走 governance-only lane。

于是「同步必然改文档」与「一个工位只能改本 raw 文档」在结构上冲突：
只要一次同步涉及多个 raw，就必然违反其一。

## 待回答的设计问题（本轮不预设答案）

1. replica 元数据是否应该放在**受治理的 issue 文档**里？
   - 选项 A：保持现状（文档内），但同步只能在本 raw 的 lane 内发生，全量同步必须走 governance lane；
   - 选项 B：把 replica 元数据移到**不受 GATE 1 管辖的本地状态面**（如 `.freely/state/replicas.json`），issue 文档只保留生命周期字段（`phase_state` 等）；
   - 选项 C：混合——`platform_ids` 留在文档（它是身份），`platform_state` / `synced_at` / watermark 移到状态面（它们是缓存）。
2. 哪个选项能同时满足：
   - 「本地是唯一真相源、平台丢了能从本地重建」（B 需要保证状态面可重建或可丢弃）；
   - 元数据缺失时 fail-closed（`command-wrapper-metadata-lifecycle` 的 Rejection 条款）；
   - 一次同步不再污染其它 raw 的治理文档。
3. 若选 C，`platform_state` 从文档移出后，`wt-close` 的 children 预检读哪里？如何保证它读到的仍是「合并后的真相」？

## 影响面

- `bin/issue-sync.d/`（create / close / batch / lib-state）、`raw_lifecycle_effects`、`wt-close`、`pr-merge-guarded` 的同步落盘；
- `command-wrapper-metadata-lifecycle.md`、`ibm-framework.md` 字段表；
- 所有既有 issue 文档的迁移路径（含 500+ 历史文档）。

## 边界

- 不改 GATE 1 的强度；
- 不在本条内做实现——先出设计判决（B1 五分类：设计不完整 / 设计张力），再决定是否拆实现 candidate；
- 与 `raw-20261114T031043Z`（daemon 无范围 batch）解耦：那条即使修好范围，本条仍成立（全量同步仍会产生跨 raw 写）。

### comment-20261114T091321Z
- source: system
- event: promote_finalized
- children: ["I-20261114T034750Z-A"]

拆解为以下任务:
1. [I-20261114T034750Z-A](will-be-updated)
