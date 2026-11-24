# Pre-Tests: CI 合并保护链 fail-closed 收口
- issue_id: I-20261124T054145Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: workflow 显式声明 checks: write，且 pr-merge-guarded 不再自签 success check
- acceptance_target: raw issue 三处修复的代码面
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261124T054145Z-ci-merge-guard-chain
- required_evidence: 单一 AT 脚本在 develop 基线 RED、工位 GREEN，含源码断言与 fail-closed 行为断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-ci-merge-protection.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed，且列出 workflow 缺 permissions / 存在自签 fallback / check 缺失时仍返回 0 三项失败
- actual_RED_output: "SUMMARY: 3 ok, 6 failed — 失败项：workflow declares a top-level permissions / grants checks write / grants contents read / no self-created success check fallback / no `|| true` swallowing / explicit non-zero fail-closed path"
- actual_output: (GREEN 阶段由 skill freely-test-execution 执行后填写)
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-1-red.log
- red-green-status: red
- status: pending
- red_how: fix 复现——用 develop 基线源码跑同一脚本，三处缺陷真实存在导致断言失败；不 mock 通过。
- acceptance_target_check: 覆盖 workflow permissions、pr-merge-guarded 自签移除、check 缺失 fail-closed 三个改动面

### acceptance-2
- id: AT-002
- requirement: 回归不破坏既有 CI 门禁与测试子集
- acceptance_target: 不改 SUMMARY 格式、不破坏 test-all
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054145Z-ci-merge-guard-chain
- required_evidence: bin/test-all --ci 全绿且 SUMMARY 行格式不变
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-2.log
- test_command: bash bin/test-all --ci
- expected_output: SUMMARY: 44 ok, 0 failed, known-broken=590（AT-001 接入后计数 +1）
- expected_RED_output: 不适用——本项仅回归，RED 由 AT-001 承担
- actual_RED_output: not_applicable: regression-only
- actual_output: (GREEN 阶段填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: 回归项，fix 场景下不单独 RED；依赖 AT-001 的 RED 证明缺陷存在。

### acceptance-3
- id: AT-003
- requirement: develop 分支保护已生效（平台一次性设置结果可验证）
- acceptance_target: 分支保护 required_status_checks 含 governance/pr-merge-guard 且 enforce_admins 为真
- testing_layer: end-to-end
- target_environment: GitHub 平台（gh api 只读）
- required_evidence: API 读取结果快照，非 404 Branch not protected
- evidence_level: real_env
- artifact_ref: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-3.log
- test_command: gh api repos/chatterzhao/freely/branches/develop/protection --jq '{checks: .required_status_checks.contexts, enforce_admins}'
- expected_output: checks 含 governance/pr-merge-guard，enforce_admins 为 true
- expected_RED_output: HTTP 404 Branch not protected（develop 基线实测结果）
- actual_RED_output: "HTTP 404 Branch not protected — gh api repos/chatterzhao/freely/branches/develop/protection 实测返回 {\"message\":\"Branch not protected\",\"status\":404}"
- actual_output: (GREEN/平台设置后填写)
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-3-red.log
- red-green-status: red
- status: pending
- red_how: fix 复现——develop 基线 API 实测返回 404 Branch not protected，为真实 RED 证据。

## Unit
- acceptance_target: workflow permissions 与 pr-merge-guarded 源码断言
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001 的静态断言部分
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: AT-001 的 fail-closed 行为 + AT-002 的 test-all 回归
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054145Z-ci-merge-guard-chain
- required_evidence: AT 脚本与 test-all 均全绿
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 分支保护生效 + guarded merge 链路仍可工作
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: AT-003 平台证据 + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: fail
- real_environment_reason: develop 基线分支保护 API 返回 404 Branch not protected（RED 证据）；修复后需重新读取并翻转为 pass
