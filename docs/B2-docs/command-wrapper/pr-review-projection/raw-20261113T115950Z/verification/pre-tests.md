# Pre-Tests: pr-review-guarded 引导同步 L0
- issue_id: I-20261113T115950Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: ACP prompt 与人工回退都先跑 L0（锚点 / Q1–Q5 / 四段举证 / 输出段 / intent 维度），且 verdict 解析行为不变；基线两处都不含 L0
- acceptance_target: L0 规则真正落到评审执行入口
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: end-to-end
- target_environment: 直接读 pr-review-guarded 文本 + 导入 review_verdict.py 验证解析（不触网）
- required_evidence: AT-001 静态 36 项全 GREEN；基线 10/26 红
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-review-guidance-l0.py
- test_command: python3 docs/system/workspace/scripts/tests/test-review-guidance-l0.py
- expected_output: SUMMARY: 36 ok, 0 failed
- expected_RED_output: SUMMARY: 10 ok, 26 failed
- actual_RED_output: develop 7820299c4 的 prompt 只有四维、无 L0、无 intent；人工步骤无 L0（AT-001-RED.log）
- actual_output: SUMMARY: 36 ok, 0 failed；Step 0 在四层之前、四类锚点、Q1–Q5、四段举证、intent 强制 fail、人工先 L0、解析五例不变（AT-001-GREEN.log）
- evidence_file: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261113T115950Z/verification/test-evidence/AT-001-RED.log,AT-001-GREEN.log
- red-green-status: green
- status: passed
- blocker: ''
- task_refs: T1,T2,T3
- case_design: 分段断言 prompt（L0 声明 / Step 0 顺序 / 四类锚点原文 / Q1–Q5 / 四段举证 / 禁止自证 / intent 维度 / 四层维度保留）与人工步骤（先 L0 / Q1–Q5 / 四段 / 输出段 / 顺序），再导入 review_verdict 验证 5 个解析样例与词表。
- red_how: fix RED — git archive develop 导出基线树，用 --source-dir 运行同一 AT。

## Unit
- acceptance_target: 引导文本结构
- testing_layer: unit
- target_environment: feature/raw-20261113T115950Z-pr-review-l0-guidance
- required_evidence: AT-001 静态组
- blocker_taxonomy: execution_pending_or_failed
1. python3 docs/system/workspace/scripts/tests/test-review-guidance-l0.py

## Integration
- acceptance_target: 既有评审与 merge 判定不退化
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: bin/test-all --ci 全绿；test-verdict-contract 仍绿
- blocker_taxonomy: execution_pending_or_failed
1. bin/test-all --ci

## End-to-End
- acceptance_target: 下一轮评审实际按 L0 执行
- testing_layer: end-to-end
- target_environment: 后续任意一轮 pr-review-guarded
- required_evidence: review 文档含 '## L0：项目意图一致性' 段
- blocker_taxonomy: execution_pending_or_failed
1. 下一轮 pr-review-guarded 的人工/ACP 结论

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 缺口由 R33.8–R33.10 三次「四层全绿仍漂移」的真实评审失效暴露；R33.14 只补了 skill，本轮补执行入口。
