# Pre-Tests: 评审 skill 新增 L0 项目意图一致性锚点
- issue_id: I-20261113T113100Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: skill 含 L0 章节且位于四层之前；外部锚点、Q1–Q5、四段举证、失败判据、输出 L0 段、三个真实案例齐全；四层与核心方法仍在
- acceptance_target: 评审具备「以项目既有资产为锚」的漂移检测层
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 直接读评审权威指南文本（不触网、不改运行时）
- required_evidence: AT-001 静态 20 项全 GREEN；基线 1/19 红
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-review-intent-anchor.py
- test_command: python3 docs/system/workspace/scripts/tests/test-review-intent-anchor.py
- expected_output: SUMMARY: 20 ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 19 failed
- actual_RED_output: develop 52b095892 快照的 skill 只有四层，无 L0、无 Q1–Q5、无四段举证、无案例；仅 S2（核心方法存在）通过（AT-001-RED.log）
- actual_output: SUMMARY: 20 ok, 0 failed；L0 在四层之前，五项必答、锚点、举证、失败判据、输出段与三个案例齐全（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T113100Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2,T3
- case_design: 静态断言 L0 的存在与顺序、五项必答、锚点清单、四段举证、失败判据（含「补数据」）、输出段、三个真实案例、以及「四层全绿仍可能整体漂移」的盲区表述；基线对 develop 源码跑同一断言，确认 19 项红。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 运行同一 AT。

## Unit
- acceptance_target: L0 结构与顺序
- testing_layer: unit
- target_environment: feature/raw-20261113T113100Z-review-l0-intent-anchor
- required_evidence: AT-001（本改动为纯文本规则，无函数级单元）
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-review-intent-anchor.py

## Integration
- acceptance_target: 既有评审/CI 不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；四层内容与 verdict 契约零改动
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 下一轮评审实际执行 L0
- testing_layer: end-to-end
- target_environment: 后续任意一轮的 pr-review-guarded
- required_evidence: 人工/A‍CP review 结论含 `## L0：项目意图一致性` 段
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮 pr-review-guarded 的 review 文档

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺口由 R33.8 / R33.9 / R33.10 三次真实评审失效暴露；本轮 skill 文本即按这些真实案例回填。
