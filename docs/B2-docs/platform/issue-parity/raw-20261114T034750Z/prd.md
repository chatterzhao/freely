# PRD: replica 元数据归属的设计判决

- issue_id: I-20261114T034750Z-A
- source_raw: raw-20261114T034750Z
- workflow_kind: feature
- milestone: M-20261114T034750Z-A
- story: platform/issue-parity

## 目标

对「replica 元数据写在治理文档里是否与 GATE 1 结构性冲突」给出**设计判决**，
并把判决写成契约文档，供 `raw-20261114T051655Z`（lane 模型 / 字段类判据）实现时作为写入面依据。

## 唯一改动范围

1. 新增 `docs/system/workspace/replica-metadata-contract.md`：判决、A/B/C 评估与推翻证据、字段分类、车道规则、不放宽边界、落地依赖。
2. 新增 AT `test-replica-metadata-decision.py`，CORE/CI_CORE 各 +1。
3. B1/B2 治理文档；`projection.lock` 重录。

## 不退化边界

- 不改 GATE 1 / `RAW_METADATA_FIELDS` / `raw_metadata_contract.validate()` / Rejection 条款；
- 不改任何运行时代码；不迁移或批量改写历史文档（R2 precedent）；
- 不新增硬门禁、不新增豁免通道；不夹带 `4435` / `051655Z` 的实现。

## 功能需求

- FR-1：明确选定选项 A（字段留在文档），并记录 B/C 被推翻的证据。
- FR-2：审计证据可追溯（字段表、严格契约、Rejection、config allowed_paths、LAWS、历史 raw）。
- FR-3：定义生命周期字段 / 副本字段两类清单及其写入者。
- FR-4：定义 issue lane 与治理车道的规则、接口三分（scan / scoped / full-sweep）。
- FR-5：明确「不改 GATE 1、不迁移、不改字段契约」的硬边界；AT 断言契约与 gate 未被本轮改动。
- FR-6：写明落地依赖 `031043Z`（已合并）/ `4435` / `051655Z`。
- FR-7：本轮 B1 按 B0 自举（§0 设计意图审计 + §0.1 四问 + 推翻原假设）。
- FR-8：基线（develop）在 FR-1..FR-7 上红。

## 验收

AT-001 GREEN `25 ok / 0 failed`；基线 `2 ok / 23 failed`；`bin/test-all --ci` 全绿；
`check-runtime-size` / `check-skill-frontmatter` / `projections verify` 均绿。
