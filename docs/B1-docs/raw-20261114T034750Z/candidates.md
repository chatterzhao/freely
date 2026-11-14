# B1 Candidates — raw-20261114T034750Z

## C-20261114T034750Z-A：replica 元数据归属的设计判决（选项 A）

- status: promoted
- promoted_issue_id: I-20261114T034750Z-A
- promoted_issue_path: docs/B2-docs/platform/issue-parity/raw-20261114T034750Z/issues/I-20261114T034750Z-A.md
- milestone: M-20261114T034750Z-A
- kind: feature
- decision: **判决 A**——replica 元数据保留在 issue 文档；全量同步走治理车道 + 字段类判据。B/C（移出文档）经审计被推翻。本轮只产出设计判决契约文档 `docs/system/workspace/replica-metadata-contract.md`，不做实现、不迁移文档。
- design_verdict: 实现未完成 + 机制未接线（**推翻** raw 预设的「设计不完整 / 结构性冲突」）
- anchor_refs: `ibm-framework.md:309/312` 字段表；`raw_metadata_contract.py:160` 严格字段集合 + `:41-46` R2「no bulk 824-doc rewrite」；`governance-merge-gate:360` config 唯一真源 + `.freely/config.toml` allowed_paths 含 B1/B2-docs
- 范围:
  1. 新增 `docs/system/workspace/replica-metadata-contract.md`：判决、A/B/C 评估表与推翻证据、副本/生命周期字段分类、lane 与全量同步规则、不放宽边界、落地依赖。
  2. 新增 AT `test-replica-metadata-decision.py`，CORE/CI_CORE 各 +1。
  3. B1/B2 治理文档。
- 验收:
  - DDR 含 A/B/C 三选项评估、选定 A、B/C 推翻证据（严格字段集合 / Rejection / 迁移成本 / 第二真相源）；
  - DDR 含副本字段与生命周期字段的分类清单；
  - DDR 明确「不放宽 GATE 1、不改 RAW_METADATA_FIELDS、不迁移历史文档」；
  - DDR 写明落地依赖 `031043Z`（已合并）/ `4435` / `051655Z`；
  - AT 静态断言 `RAW_METADATA_FIELDS` 与 GATE 1 / config 未被本轮改动（防偷跑实现）；
  - 基线（develop）各条红。
- 不退化边界:
  - 不改 GATE 1 / `RAW_METADATA_FIELDS` / `validate()` / Rejection 条款；
  - 不改任何运行时代码；不迁移/批量改写历史文档；
  - 不新增硬门禁、不新增豁免通道；
  - 不夹带 `4435` / `051655Z` 的实现。
