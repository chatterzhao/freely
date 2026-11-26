## 0. 设计意图审计（先于方案）
### 广搜与分层
- 关键词：wt-close / 职责边界 / batch scope / frontmatter schema。命中 `commands.md:14`、`AGENTS.md:14`、`workflow SKILL:273,337`、`runtime/freely:24149`、`governance-merge-gate:985`。
- 当前生效：wt-close 是 `--raw-key` 单入口的只读终态门禁 + 清理器；runtime 提示已是 `batch --auto`（#4699 顺带修过）；下游文档仍描述旧双步/写平台语义。
- 历史记录只作背景：`5e5277e37` 收口单入口，`f1be6b5c3 → 8bc4773cf` 交还平台写权。

### 外部锚点
- `cmd-batch.sh`：`unscoped batch is a cross-raw write`。
- `governance-merge-gate` 已对 strict raw 校验 `schema_version: '1'`，但 touched linked I-* 无等价门禁。
- 本轮实证：按旧提示执行产生跨 raw 平台噪声。

### 判定
**文档/判据不完整**：实现方向正确，说明与门禁覆盖面未同步。
### 冲突 / 影响面
不改 wt-close 写权边界；只改说明、AT 与 linked schema 判据。
## 0.1 四问
- Q1 治理元数据/门禁覆盖；Q2 平台写仍由 issue-sync 独占；Q3 不要求额外工位；Q4 门禁维度（schema）与故障现象（解析空字段）一致，直接补门禁。
## 1. 决策
① 同步三份文档为 write-free + `--raw-key` 单入口；② AT 钉住 docs 与 scoped batch 提示；③ 对本次改动触及的 linked I-* 强制 YAML `---` 块与 `schema_version: '1'`，历史文档不批量改写；④ Phase 7 死代码与双实现统一另列长期架构债，不夹带。
