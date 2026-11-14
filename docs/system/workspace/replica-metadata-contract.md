# Replica Metadata Contract — 设计判决（raw-20261114T034750Z）

> 状态：**判决已定（选项 A）**。本文件是契约文档，不是实现计划。
> 权威来源：`.freely/goal-arch-debt.md` 当前恢复点；本文件定义「replica 元数据归谁所有、谁能改、走哪条车道」。

## 1. 判决

**replica 元数据保留在 issue 文档的 YAML frontmatter 中，不移到本地状态面。**
跨 raw 的副本字段传播，**必须**走治理车道（governance-only lane），并受字段类判据约束；
issue lane 内只允许同步本 raw 及其 children。

原 raw 提出的「两股设计结构性冲突、必须把字段移出治理文档」**不成立**：
冲突来自「全量同步的正式车道尚未建完 + GATE 1 报错不给指引 + daemon 曾无范围 batch」，
而不是字段放错了地方。按分类，这是**实现未完成 + 机制未接线**，不是设计不完整。

## 2. 审计证据（判决依据）

| 证据 | 原文 / 事实 |
|---|---|
| `ibm-framework.md:309` | 「`platform_state` \| 平台同步状态：open\|closed。由 issue-sync create/close 自动管理」 |
| `ibm-framework.md:312` | 「`platform_ids` \| 每个平台的 issue_id、url、synced_at」 |
| `command-wrapper-metadata-lifecycle.md` Rejection | 「`platform_ids`、`phase_state`、`last_synced_comment_at`、`hash`、`session_refs` 任一缺失或与真相源冲突时拒绝」「失败路径必须是 fail-closed」 |
| `raw_metadata_contract.py:160` | `if keys not in (RAW_METADATA_FIELDS, RAW_METADATA_FIELDS_WITH_SEVERITY): raise MetadataValidationError("raw metadata fields are missing, extra, or reordered")` — `platform_state` 是 21 个必需键之一 |
| `raw_metadata_contract.py:41-46` | R2 precedent：「no bulk 824-doc rewrite」— 历史上已明确拒绝大规模改写既有严格文档 |
| `governance-merge-gate:360` | 「`.freely/config.toml [skip_ibm_gate].allowed_paths` is the single source of truth」 |
| `.freely/config.toml` | `allowed_paths` **含** `docs/B1-docs/`、`docs/B2-docs/` — 跨 raw 文档变更本就有合法车道 |
| `docs/LAWS.md:304` | 「`FREELY_SKIP_IBM_GATE` 是唯一合法的门禁豁免机制……仅限 document\|cleanup\|format」 |
| `raw-20261103T091157Z` | 早已写下「跨 raw key 的文档回填必须单独 governance-only lane + FREELY_SKIP_IBM_GATE」 |

消费方（均从文档读字段，移出即全部要改）：
`raw_metadata_contract.py`、`raw_lifecycle_effects.py`、`frontmatter_contract_cli.py`、
`pr-merge-guarded`、`merge_issue_sync.py`、`wt-close`、
`cmd-create.sh`、`cmd-close.sh`、`cmd-batch.sh`。

## 3. 三选项评估

| 选项 | 做法 | 结论 |
|---|---|---|
| **A** | 字段留在文档；lane 内只同步本 raw；全量走治理车道 + 字段类判据 | ✅ **采用**：与字段表、Rejection、严格契约、R2 教训、LAWS 豁免机制全部一致；零文档迁移 |
| **B** | 全部移到本地状态面（如 `.freely/state/replicas.json`） | ❌ 推翻：违反 `RAW_METADATA_FIELDS` 精确集合与 `validate()`；Rejection 要求 `platform_ids` 必须在文档；9 处消费方要改；500+ 文档迁移；状态面丢失则「本地唯一真相源」无法重建；并引入**第二真相源**（L0 Q4） |
| **C** | 混合：`platform_ids` 留文档，`platform_state` / watermark 移出 | ❌ 推翻：同样破坏严格字段集合（`platform_state` 是第 17 个必需键）；`wt-close` children 预检、`close_platforms`、`cmd-close` 都从文档读它；迁移成本不比 B 小，收益仅少改 3 个字段 |

B/C 被推翻的记录保留在此，防止后人以「减少脏文档」为由重开该方向。

## 4. 字段分类（唯一定义）

**生命周期字段**（只能由该 raw 的 lane 修改）：
`phase_state`、`status`、`kind`、`local_id` / `issue_id`、`promoted_from`、`absorbed_into`、
`canonical_issue_path`、`pre_tests_path`、`verification_artifact_dir`、标题与正文、
`created_at`、`schema_version`、`intake_id`、`author`、`channel`、`session_refs`、
`promoted_children`、`source_candidate`、`completed_at`、`closeout_note`。

**副本字段**（`issue-sync` 是唯一写入口；允许治理车道跨 raw 传播）：
`platform_ids`、`platform_state`、`primary_platform`、`last_synced_comment_at`、
`hash`、`updated_at`、`synced_at`（`platform_ids` 内）。

> 注意：`platform_state` 语义是「所有配置平台副本都已关闭」的**本地投影**，不是缓存；
> 它与 `phase_state` 一起构成收口判据，移出文档会使 `wt-close` 的 children 预检失去合并后真相。

## 5. 车道规则

### 5.1 issue lane（`fix/*`、`feature/*` 含 raw key）

- 只允许改**本 raw 及其 children** 的副本字段；
- 生命周期字段只能由该 raw 的 lane 改；
- 同步入口：`issue-sync batch --raw-key <key>` 或 `batch --auto`（已由 `raw-20261114T031043Z` 落地）；
- GATE 1 的「一个工位一个 raw」约束**不放宽**。

### 5.2 全量同步（治理车道）

- 分支类别：`chore/sync-<date>`（第三类分支，无 raw key）；
- 标记：`FREELY_SKIP_IBM_GATE=1` + 合规 `--reason`；
- **逐文档与 base 比对**：任一生命周期字段变化 → **拒绝**；仅副本字段变化 → 允许；
- 这比现有 `is_governance_only_path`（按目录放行）更严，补上「治理车道能改 phase」的洞；
- 不自动建 PR、不自动 merge。

### 5.3 接口三分（范围由调用方声明）

| 命令 | 权限 | 上下文 |
|---|---|---|
| `issue-sync scan` | 只读 drift 报告，永不写 | 任意 |
| `issue-sync batch --raw-key K [K2...]` | 只碰给定 raw 及其 children | lane 内 |
| `issue-sync batch --all --lane governance` | 全量，受字段类判据约束 | 治理车道 |

daemon 只允许 `scan` 或 `batch --auto`（本 lane）；**禁止无参 batch**。

## 6. 不放宽边界（硬约束）

- 不改 GATE 1 的强度、不给 issue lane 任何新豁免；
- 不改 `RAW_METADATA_FIELDS` / `raw_metadata_contract.validate()` / Rejection 条款；
- 不改 `command-wrapper-metadata-lifecycle.md` 的「stale 拒绝」语义；
- **不迁移、不批量改写历史文档**（R2 precedent）；
- 不新增第二份安装态/副本真相源；
- 不把「字段类判据」做成可补字段通过的门禁——校验的是逐文档 diff 事实。

## 7. 落地依赖（按队列顺序）

| raw | 内容 | 状态 |
|---|---|---|
| `raw-20261114T031043Z` | `batch --auto` 限定本 lane / 受保护分支跳过；修绝对路径过滤失效 | **已合并** |
| `raw-20261113T141456Z`（#4435） | GATE 1 报错给 governance-only lane 指引；白名单单一真源 | 待 |
| `raw-20261114T051655Z`（#4574） | 第三类分支 + 字段类判据 + `scan`/`batch --all` 三分 | 待（依赖本判决确定写入面） |

本文件**不**替它们做实现；它只锁定「写入面 = issue 文档内的副本字段」，使后续实现不会按 B/C 方向改错对象。
