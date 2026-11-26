## 0. 设计意图审计（先于方案）

### 广搜关键词族与分层
| 关键词族 | 命中 |
|---|---|
| updated_at / `| updated |` | `raw_metadata_contract.py:276`、`raw_lifecycle_effects.py:262`、`cmd-comment.sh:54`、`lib-platform.sh:175`、`issue_create_contract.py:189,213` |
| raw-reconciliation / content_diverged | `raw_reconciliation.py:60-107,135-193`、`raw-reconciliation-gate.py:31-58` |
| issue-sync update / 平台投影 | `bin/issue-sync.d/cmd-update.sh`、`sync/issue_create_contract.py` |

一个功能可能有多份文档（当前实现 / 历史局部 / 过期恢复点）。本次命中均为当前生效实现；`docs/B2-docs/**` 中旧轮次记录只作背景，不作为现状。

### 外部锚点（引用原文）
- `issue_create_contract.py:184`：`Render the platform body for local_id from its local document`；`:213` 由 `metadata.get('updated_at')` 生成表格行。
- `raw_reconciliation.py:96`：`A raw document without an explicit labels field cannot assert platform labels. Comparing that dimension would report a fake divergence ...`——已存在「把生成型元数据排除出 canonical 比较」的先例。
- 本轮实证：#4703 收口被 `content_diverged` 连续阻断 6 次，每次都是手工改 `| updated |` 行后重跑 `issue-sync update`。

### 判定
**设计不完整**：canonical projection 比较了从 frontmatter 派生的表格行，而该行有多个合法写入者（`transition`/`comment`/platform pull），没有单一回写通道。不是实现偏差，也不是门禁应删除。

### 与既有断言冲突
无。排除生成型时间戳行不触碰 `state`/`raw_key`/`title`/`labels`/人类正文的比较，既有「必须拒绝」断言保持。

### 影响面
`raw_reconciliation._body()`（canonical 投影）、对应 AT；不改 `platform_body()` 其他字段、不改任何平台写通道。

## 0.1 全局适配四问
- Q1 类别：副本传播判据（治理元数据修复）。
- Q2 职责边界：frontmatter `updated_at` 是事实；正文表格派生值是投影。最终判定属于 `canonical_projection`。
- Q3 结构性冲突：若要求「每次改 frontmatter 都同步改正文表格」会给 4 个写入者加同一责任，违反单一事实源；改判据层，不改写入者。
- Q4 门禁失配：门禁测的是「平台与本地是否同一内容」，但把生成型时间戳当作内容；先改判据模型，不放宽门禁。

## 1. 发散与收敛
- 方案 A：`issue-sync update` 写平台前回写本地正文表格。优点保留严格比较；缺点只覆盖一个入口，其他 3 个写入者仍漂移，且只读命令产生本地写。
- 方案 B：在 `canonical_projection._body()` 中把 `| updated | ... |` 归一化为占位符（要求行存在，忽略值），类比已排除的 `phase/*` 标签。优点覆盖所有写入者、零平台写、无第二真源；缺点该行的时间戳差异不再被比较（但它没有语义内容）。
- 决策：选 **B**。A 是「修一个入口」，B 是「修正判据对象」。

## 2. 决策与边界
- 仅对 `| updated |` 行做值归一化；`created`/`phase_state`/`kind`/`canonical` 等仍严格比较。
- 必须保留控制用例：人类正文不同仍判 `content_diverged`，证明门禁强度未降。
- 非目标：不改 `platform_body()` 字段语义、不改平台写通道、不夹带其他 issue。
