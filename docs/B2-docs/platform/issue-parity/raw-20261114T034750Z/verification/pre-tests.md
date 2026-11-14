# Pre-Tests: replica 元数据归属的设计判决

- issue_id: I-20261114T034750Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: 判决文档含 A/B/C 评估与选定 A、B/C 推翻证据、字段分类、车道规则、接口三分、不放宽边界、落地依赖；AT 断言 `RAW_METADATA_FIELDS` 与 gate 未被本轮改动；本轮 B1 按 B0 自举；基线红
- acceptance_target: 锁定写入面，使 `051655Z` 不会按 B/C 方向改错对象
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 直接读判决契约与 B1 产物文本（不触网、不改运行时）
- required_evidence: AT-001 GREEN 25/0；基线 2/23
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-replica-metadata-decision.py
- test_command: python3 docs/system/workspace/scripts/tests/test-replica-metadata-decision.py
- expected_output: SUMMARY: 25 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 23 failed
- actual_RED_output: develop 8ef15600a 无判决契约、无本轮 B1 产物；S1–S4/S7–S13/S16–S20 红（AT-001-RED.log）
- actual_output: SUMMARY: 25 ok, 0 failed；S14/S15 证明字段契约与 GATE 1 零改动、S19 证明 P0 显式推翻原假设、S17/S18/S20 证明 B0 自举（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261114T034750Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 静态断言判决完整性（三选项/推翻证据/字段分类/车道/边界/依赖），再断言 `raw_metadata_contract.py` 仍含 `platform_state`、`governance-merge-gate` 仍拥有 `is_governance_only_path`（防偷跑实现），最后自举检查本轮 B1 的 §0/§0.1 与 candidate 两字段。
- red_how: fix RED — `git archive develop` 导出基线树，用 `--source-dir` 运行同一 AT。

## Unit

- acceptance_target: 判决契约结构
- testing_layer: unit
- target_environment: feature/raw-20261114T034750Z-replica-metadata-design
- required_evidence: AT-001 S1–S16
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-replica-metadata-decision.py

## Integration

- acceptance_target: 既有契约/CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；check-runtime-size / check-skill-frontmatter / projections verify 均绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End

- acceptance_target: `051655Z` 按本判决实现写入面
- testing_layer: end-to-end
- target_environment: `raw-20261114T051655Z` 的 B1
- required_evidence: 其 B1 §0 引用本契约，且实现不迁移历史文档、不改 RAW_METADATA_FIELDS
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮 `051655Z` 的 B1 产物

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 张力由 R33.16 / R33.18 两次「一次同步污染 108/58 个跨 raw 文档」实测暴露；P0 审计发现 config allowed_paths 已含 B1/B2-docs、契约字段集合严格，故推翻「移出文档」方向。
