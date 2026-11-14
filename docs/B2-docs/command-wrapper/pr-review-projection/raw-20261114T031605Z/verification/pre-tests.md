# Pre-Tests: B1 增设计意图审计层

- issue_id: I-20261114T031605Z-A

## Acceptance Items

### acceptance-1

- id: AT-001
- requirement: B0 位于发散之前；四类锚点 + 五分类 + 四问 + 冲突/影响面；两个模板与完成自检同步；明确不做硬门禁且 gate 零改动；本轮自身 brainstorms/candidates 自举遵循 B0；基线红
- acceptance_target: 决策前移到 B1 立项阶段，并被机器防回退地钉住
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 直接读 B1 skill 与模板文本 + 本轮 B1 产物（不触网）
- required_evidence: AT-001 GREEN 31/0；基线 3/28
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-b1-design-intent-audit.py
- test_command: python3 docs/system/workspace/scripts/tests/test-b1-design-intent-audit.py
- expected_output: SUMMARY: 31 ok, 0 failed
- expected_RED_output: SUMMARY: 3 ok, 28 failed
- actual_RED_output: develop bbe3baf66 的 B1 skill 只有价值审视与「读边界文档」，无 B0 / 五分类 / 四问 / 模板字段 / 自检项；本轮产物尚不存在（AT-001-RED.log）
- actual_output: SUMMARY: 31 ok, 0 failed；S3 证明 B0 在发散之前、S5–S8 锚点与五分类、S9 四问、S10–S13 模板与自检、S14–S16 无硬门禁且 gate 零改动、S17–S20 本轮自举通过（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261114T031605Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 静态断言 B0 的存在/顺序/五类锚点/五分类/四问/两模板/自检两项/不做硬门禁声明；再检查 `governance-merge-gate` 不含 `design_verdict`（证明没偷偷加硬门禁）；最后自举检查本轮 brainstorms.md 与 candidates.md 是否真的按 B0 产出。
- red_how: fix RED — `git archive develop` 导出基线树，用 `--source-dir` 运行同一 AT。

## Unit

- acceptance_target: skill 结构
- testing_layer: unit
- target_environment: feature/raw-20261114T031605Z-b1-design-intent-audit
- required_evidence: AT-001 静态组 S1–S16
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-b1-design-intent-audit.py

## Integration

- acceptance_target: 既有 B1/CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；check-skill-frontmatter ok（33 skills, 12 loops）
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End

- acceptance_target: 下一个 raw 的 B1 实际执行 B0
- testing_layer: end-to-end
- target_environment: 下一轮 B1
- required_evidence: 下一轮 brainstorms.md 含 `## 0. 设计意图审计` 与四问，candidates.md 含 design_verdict/anchor_refs
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮 B1 产物

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 缺口由 R33.18 / R33.16 三次「拿到 raw 就局部开干」的真实返工暴露；本轮 B1 自身即第一次按 B0 执行（自举 S17–S20）。
