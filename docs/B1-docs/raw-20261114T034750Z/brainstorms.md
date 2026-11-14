# B1 Brainstorm — raw-20261114T034750Z

## 0. 设计意图审计（先于方案）

- 外部锚点（引用原文）:
  - 设计文档: `docs/system/workspace/ibm-framework.md:309`「`platform_state` | 平台同步状态：open\|closed。由 issue-sync create/close 自动管理」；`:312`「`platform_ids` | 每个平台的 issue_id、url、synced_at」；`command-wrapper-metadata-lifecycle.md` Rejection「`platform_ids`、`phase_state`、`last_synced_comment_at`、`hash`、`session_refs` **任一缺失**或与真相源冲突时拒绝」「失败路径必须是 fail-closed」；`docs/LAWS.md:304`「`FREELY_SKIP_IBM_GATE` 是唯一合法的门禁豁免机制：仅跳过 IBM governance 文档门禁……仅限 document\|cleanup\|format」。
  - 既有验收测试: `test-issue-sync-close-linked.py`、`test-wt-close-children.py`、`test-raw-issue-pull-parity.py`、`test-batch-scope-filter.py`。
  - 门禁源码注释/理由: `raw_metadata_contract.py:160`「`if keys not in (RAW_METADATA_FIELDS, RAW_METADATA_FIELDS_WITH_SEVERITY): raise MetadataValidationError("raw metadata fields are missing, extra, or reordered")`」；同文件 `:41-46` 注释「Adding it as a required 22nd field would make validate() reject all 59 existing strict docs + the canonical new_raw_metadata() output (**R2 precedent: keep compatibility, no bulk 824-doc rewrite**)」；`governance-merge-gate:360`「Paths where FREELY_SKIP_IBM_GATE=1 is allowed. **Authority: .freely/config.toml [skip_ibm_gate].allowed_paths is the single source of truth**」。
  - 既有同类实现: `.freely/config.toml [skip_ibm_gate].allowed_paths` = `['templates/', 'docs/B1-docs/', 'docs/B2-docs/', ...]`；`issue-sync batch --auto`（raw-20261114T031043Z 已落地）；`postmerge_commit_guard.py`（raw-20261114T065554Z 已落地）。
  - 配置约束: GATE 1 的 config 覆盖硬编码默认（R33.14 已核实），当前 allowed_paths **含** B1/B2-docs。
- 判定（五分类）: **实现未完成 + 机制未接线**，而**不是设计不完整**。raw 原假设「两股设计结构性冲突、必须把 replica 元数据移出治理文档」经审计**不成立**：治理车道本就允许改 `docs/B1-docs/`、`docs/B2-docs/`；冲突来自「全量同步没有正式车道 + GATE 1 报错不给指引 + daemon 无范围 batch」，其中后两项已有对应 raw 或已落地。
- 与既有断言的冲突: 若选 B/C 移出字段，会**直接违反** `RAW_METADATA_FIELDS` 严格字段集合、`validate()` 的 keys 精确匹配、Rejection 的「缺失即拒绝」，并需迁移 500+ 历史文档——R2 已有明确「no bulk rewrite」教训。
- 影响面: 本轮只产出**设计判决契约文档**（DDR），不改任何运行时代码、不改字段契约、不迁移文档。落地依赖 `raw-20261114T031043Z`（已合并）/ `raw-20261113T141456Z`（#4435）/ `raw-20261114T051655Z`（#4574）。

### 0.1 全局适配反思（四问）

1. **类别**：这是**设计判决**（治理元数据归属），不是副本传播、不是实现 bug。按 raw 边界「不在本条内做实现」，本轮只落判决与契约文档。
2. **职责边界**：`platform_ids` / `platform_state` 的**所有权**归 issue 文档（严格契约 + Rejection）；`issue-sync` 是唯一写入口；GATE 1 管**生命周期字段**的归属，治理车道管**副本字段**的跨 raw 传播。三者不能混：把「写入面」问题错当成「字段归属」问题，就会去动契约（B/C），那是改错对象。
3. **结构性冲突**：真正被排除的反设计是「每次同步给每个文档开工位走 IBM」——按 A 只需一条治理车道即可；而 B/C 反而会引入「状态面与文档两份真相源」，制造新的 Second-Source（L0 Q4）。
4. **门禁失配**：GATE 1 测的是**路径/身份**（分支 key vs 文档 key），副本字段传播是**字段类**变更；`051655Z` 已登记「字段类判据」。本轮**不改 GATE 1**、不给任何新豁免，只在判决里说明依赖。

## 1. 审计：raw 原假设为何不成立

raw 说「同步必然改文档」与「一工位只能改本 raw 文档」结构冲突。实测：

```
.freely/config.toml [skip_ibm_gate].allowed_paths
  = ['templates/', 'docs/B1-docs/', 'docs/B2-docs/', ...]
```

`governance-merge-gate:360` 明确 config 是唯一真源，`FREELY_SKIP_IBM_GATE=1` 时这些路径**可以**跨 raw 变更（LAWS.md:304）。
`raw-20261103T091157Z`（platform issue-parity）的 prd/IDN/review 早已写下：

> GATE 1 下，跨 raw key 的文档物化/回填不能混入本 lane，**必须单独 governance-only lane + FREELY_SKIP_IBM_GATE**。

所以设计**已经给出**冲突的解法，缺的是把它接线成可执行的正式流程：
- `raw-20261114T031043Z`：daemon 前置 batch 已改为 `batch --auto`（限定本 lane / 受保护分支跳过），并修掉「绝对路径含工位名导致过滤失效」→ **已合并**；
- `raw-20261113T141456Z`（#4435）：GATE 1 报错不给 governance-only lane 指引、白名单两处真源不一致 → 待；
- `raw-20261114T051655Z`（#4574）：`scan`（只读）/ `batch --raw-key` / `batch --all --lane governance` 三分与字段类判据 → 待。

**结论**：不是「字段放错地方」，是「全量同步的正式车道还没建完」。

## 2. 三选项判决

| 选项 | 做法 | 评估 |
|---|---|---|
| **A 保持文档内 + 全量同步走治理车道** | 字段不动；lane 内只同步本 raw；全量走 `chore/sync-*` + `FREELY_SKIP_IBM_GATE=1`；按字段类判据限制只改副本字段 | ✅ **采用**：与 `ibm-framework` 字段表、Rejection、严格契约、R2 迁移教训、LAWS 豁免机制全部一致；零文档迁移 |
| B 全部移到本地状态面（如 `.freely/state/replicas.json`） | 文档只留生命周期字段 | ❌ 违反 `RAW_METADATA_FIELDS` 精确集合与 `validate()`；Rejection 要求 `platform_ids` 必须在文档；8+ 处消费方要改；500+ 文档迁移；状态面若丢失，「本地唯一真相源」无法重建；且引入第二真相源 |
| C 混合（`platform_ids` 留文档，缓存移出） | 部分字段外移 | ❌ 同样破坏严格字段集合（`platform_state` 是第 17 个必需键）；`wt-close` children 预检、`raw_lifecycle_effects.close_platforms`、`cmd-close` 都从文档读 `platform_state`；迁移成本不比 B 小，收益只是少改 3 个字段 |

**判决：A。** 并明确记录 B/C 被推翻的证据，防止后人以「减少脏文档」为由重开这个方向。

## 3. 判决带来的约束（写进契约文档）

1. `platform_ids` / `platform_state` / `last_synced_comment_at` / `updated_at` 归入**副本字段**，所有权仍属 issue 文档；
2. `phase_state` / `status` / `kind` / `promoted_from` / `absorbed_into` / `canonical_issue_path` / `pre_tests_path` / `verification_artifact_dir` / 标题正文归入**生命周期字段**；
3. **lane 内**（`fix/feature/raw-*`）：只允许改本 raw 及其 children 的副本字段；生命周期字段只能由该 raw 的 lane 改；
4. **全量同步**：必须走治理车道（`chore/sync-*` + `FREELY_SKIP_IBM_GATE=1` + 合规 reason），且逐文档与 base 比对：任一生命周期字段变化 → 拒绝；仅副本字段变化 → 允许；
5. `scan` 只读、`batch --raw-key` 限定、daemon 只 `scan` 或 `--auto`；
6. 不放宽 GATE 1、不新增豁免、不改 `RAW_METADATA_FIELDS`、不迁移历史文档；
7. 落地依赖：`031043Z`（已合并）、`4435`（待）、`051655Z`（待）。

## 4. 证伪

- 「移出字段就干净了」→ 否：违反严格契约与 Rejection，且制造第二真相源（L0 Q4）。
- 「A 等于允许随便改文档」→ 否：字段类判据（依赖 051655Z）逐文档比对生命周期字段，比现状更严。
- 「本轮没写代码等于没推进」→ 否：raw 边界明确「先出设计判决」；本轮产出的是**可执行的判决契约**，直接决定 051655Z 的写入面，避免后者按 B/C 方向做错。

## 5. 边界

- 不改 GATE 1、不改 `RAW_METADATA_FIELDS`、不改 `raw_metadata_contract.validate()`、不改 `command-wrapper-metadata-lifecycle.md` 的 Rejection；
- 不改任何运行时代码；不迁移/批量改写历史文档；
- 不新增硬门禁、不新增豁免通道；
- 不夹带 `4435` / `051655Z` 的实现（它们各自按依赖顺序推进）。
