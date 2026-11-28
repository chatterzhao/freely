# Pre-Tests: 入口命令名与 dispatcher 对齐
- issue_id: I-20261108T134701Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: `bin/freely` 注释与 commands.md 中承诺的 `freely <cmd>` 必须真实存在；未实现命令名 fail-closed
- acceptance_target: 目标 1、2
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261108T134701Z-install-command-parity
- required_evidence: develop RED 与工位 GREEN 的逐断言输出 + SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-command-name-contract.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 至少 1 failed（bin/freely 仍承诺 freely install / checker 缺失）
- actual_RED_output: "SUMMARY: 4 ok, 6 failed（S1/S2/S3/S5/S6/S7 failed；develop 基线）"
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- red_how: develop 基线中 `bin/freely:23,36,40` 明确写 `freely install`，且不存在契约检查脚本；执行 `python3 docs/system/workspace/scripts/tests/test-command-name-contract.py` 得 4 ok/6 failed，bug 可复现。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: 静态扫描入口注释与 commands.md；checker 自测合成反例；runtime 行预算断言

### acceptance-2
- id: AT-002
- requirement: runtime/freely 不新增 install 分派，行预算不变
- acceptance_target: 目标 3
- testing_layer: integration
- target_environment: test-pre-merge-20261108T134701Z-install-command-parity
- required_evidence: `bin/check-runtime-size` rc=0 且 AT 断言 27166 行
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/verification/test-evidence/acceptance-2.log
- test_command: bash bin/check-runtime-size
- expected_output: rc=0，runtime 行数在预算内
- expected_RED_output: 不适用（该门禁在 baseline 已通过；作为回归保护）
- actual_RED_output: "baseline 已通过（回归保护项，非本轮缺陷复现）"
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/command-wrapper/install-command-parity/raw-20261108T134701Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本轮不改 runtime/freely；该门禁在 baseline 已绿，作为回归保护而非缺陷复现面。
- replacement_evidence: AT-001 的 S8/S9 已断言 runtime 行预算与无 install 分派。
- red_how: baseline 已通过，本项作为回归；RED 证据以 AT-001 为准。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T3
- case_design: 直接运行既有行数门禁

## Unit
- acceptance_target: checker 的提取与 fail-closed 逻辑（合成反例）
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: `--self-test` 证明未实现命令名被检出且返回非零
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: AT-001 + AT-002 在 test-pre-merge 全绿
- testing_layer: integration
- target_environment: test-pre-merge-20261108T134701Z-install-command-parity
- required_evidence: 全量 test-all 通过
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 文档承诺与真实可调用命令一致（吃狗粮）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261108T134701Z-install-command-parity → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
