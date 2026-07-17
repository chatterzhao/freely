# Pre-Tests: 历史状态批量收敛
- issue_id: I-20260715T121608Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 16 处有据历史状态漂移全收敛
- acceptance_target: 3 个 merge 实证且无欠账 I-* 为终态 + 13 个 legacy raw 有终态
- testing_layer: integration
- target_environment: fix/raw-20260715T121608Z-legacy-state-reconcile
- required_evidence: harness 对照断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260715T121608Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/gate/governance/raw-20260715T121608Z/verification/harness/at001-reconcile.sh
- expected_output: "AT-001 PASS: 16/16 状态已收敛"
- expected_RED_output: "AT-001 FAIL: 16+ 处未收敛"
- actual_RED_output: AT-001 FAIL: 19 处未收敛（首版含 6 I-drift；其中 3 个因历史欠账被 gate 实拦后显式撤出范围，见 IDN）
- actual_output: AT-001 PASS: 16/16 状态已收敛
- evidence_file: docs/B2-docs/gate/governance/raw-20260715T121608Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — develop 现状即漂移态，harness 首跑必列 19 处清单（acceptance-1-red.log 存证）

## Unit
- acceptance_target: 无独立单元面
- testing_layer: unit
- target_environment: fix/raw-20260715T121608Z-legacy-state-reconcile
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯治理文档字段收敛，无代码
- replacement_evidence: AT-001 对照断言

## Integration
- acceptance_target: 19 文件对照断言
- testing_layer: integration
- target_environment: fix/raw-20260715T121608Z-legacy-state-reconcile
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## End-to-End
- acceptance_target: guarded merge chain 本身即端到端（doc-only）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260715T121608Z-legacy-state-reconcile → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. pr-create/merge 门禁回执

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 平台状态实测（13 个 GH issue CLOSED/MERGED 逐一 gh api 核验）+ merge 实证 git log 可考
