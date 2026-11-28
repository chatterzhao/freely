# Pre-Tests: 打包 parity 回归收口
- issue_id: I-20261128T065937Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: package-runtime-file-parity 不再检出 commands.md，打包可完成
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261128T065937Z-package-parity-regression
- required_evidence: develop RED rc=1 + 工位 GREEN rc=0 + freely-package 成功
- evidence_level: real_env
- artifact_ref: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/quality/package-runtime-file-parity.py --project . --json
- expected_output: "ok: true, undeclared: []"
- expected_RED_output: "ok: false, undeclared: ['docs/system/workspace/commands.md']"
- actual_RED_output: "rc=1; undeclared=['docs/system/workspace/commands.md']; ok=false（develop 基线）"
- actual_output: "ok=true, undeclared=[]（9 runtime-referenced 文件全部在 allowlist）"
- evidence_file: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 基线 bin/freely 与 quality checker 字面引用 commands.md，parity 必然失败。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- case_design: 直接运行 fail-closed 门禁并读 JSON 判定

### acceptance-2
- id: AT-002
- requirement: 原命令名契约能力不降级（含 fail-closed 反例）
- acceptance_target: 目标 3
- testing_layer: integration
- target_environment: test-pre-merge-20261128T065937Z-package-parity-regression
- required_evidence: test-command-name-contract.py 与 t-command-name-contract-01.sh 全绿
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/verification/test-evidence/acceptance-2.log
- test_command: bash -c 'python3 docs/system/workspace/scripts/tests/test-command-name-contract.py && bash docs/system/workspace/scripts/tests/unit/t-command-name-contract-01.sh'
- expected_output: 两个 SUMMARY 均为 0 failed
- expected_RED_output: 不适用（本项为回归保护，基线已绿）
- actual_RED_output: regression-only
- actual_output: "test-command-name-contract.py SUMMARY: 10 ok, 0 failed; t-command-name-contract-01.sh SUMMARY: 4 ok, 0 failed"
- evidence_file: docs/B2-docs/command-wrapper/install-command-parity/raw-20261128T065937Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 命令名契约能力本轮只迁移位置，不改变判据；作为回归保护执行。
- replacement_evidence: AT-001 与全量 CI
- red_how: 基线已绿；RED 证据以 AT-001 为准。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

## Unit
- acceptance_target: checker 迁移后自测与合成反例仍成立
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: t-command-name-contract-01.sh 4 ok / 0 failed
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: parity checker + 命令名契约 AT 同时通过
- testing_layer: integration
- target_environment: test-pre-merge-20261128T065937Z-package-parity-regression
- required_evidence: 两条 acceptance 全绿且 test-all --ci 0 failed
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: freely-package --version auto --activate 成功
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261128T065937Z-package-parity-regression → develop merge chain
- required_evidence: packaging rc=0 与 install-state 刷新成功
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: fix worktree 内 parity rc=0；命令名契约 AT 10/0 与单测 4/0；打包实测在 develop merge 后执行。
