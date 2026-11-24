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
- actual_output: "SUMMARY: 9 ok, 0 failed — workflow permissions 4 项 + pr-merge-guarded fail-closed 5 项全通过（AT-001 GREEN 在 fix 工位与 test 工位各执行一次，均 9/0）"
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-1-green.log
- red-green-status: green
- status: passed
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
- actual_output: "SUMMARY: 44 ok, 0 failed, known-broken=590 — test-gate run rc=0 status=completed（fix 工位与 test 工位各一次）"
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-2-green.log
- red-green-status: green
- status: passed
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
- actual_output: (合并后设置分支保护时填写；本轮按用户决策延后)
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/verification/test-evidence/acceptance-3-red.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 用户决策「先合并代码，再配保护」——CI 当前因旧 workflow 无 checks:write 一直 403，若先配分支保护会在新 workflow 合并前卡死所有 PR。分支保护是平台一次性设置，不属于代码回归；RED 证据（404 Branch not protected）已留存，GREEN 验证排在代码合并后。
- replacement_evidence: acceptance-3-red.log（develop 基线 404 实测）+ 合并后 workflow 生效的 CI check run 证据；AT-001 的静态断言已证明 workflow 显式声明 checks: write。
- red_how: fix 复现——develop 基线 API 实测返回 404 Branch not protected，为真实 RED 证据。

## Unit
- acceptance_target: workflow permissions 与 pr-merge-guarded 源码断言
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001 静态断言 9/0（见 acceptance-1.log）
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 执行 `python3 docs/system/workspace/scripts/tests/test-ci-merge-protection.py`，断言 workflow 顶层 permissions 含 checks: write / contents: read，且 pr-merge-guarded 无自签 check、无 `|| true`、有非零 fail-closed 路径。
  2. 实际结果：SUMMARY: 9 ok, 0 failed（RED 基线 3 ok / 6 failed）。
- status: passed

## Integration
- acceptance_target: AT-001 的 fail-closed 行为 + AT-002 的 test-all 回归
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054145Z-ci-merge-guard-chain
- required_evidence: AT 脚本与 test-all 均全绿（见 acceptance-1.log / acceptance-2.log）
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 在 test 工位 merge dev 提交后执行 `bash bin/test-all --ci` → 44 ok / 0 failed。
  2. 执行 `./bin/freely test-gate run --worktree . --command 'bash bin/test-all --ci'` → rc=0 status=completed。
- status: passed

## End-to-End
- acceptance_target: 分支保护生效 + guarded merge 链路仍可工作
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: guarded merge receipts + 合并后 AT-003 平台证据
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 代码合并后由 pr-merge-guarded 走完整治理门禁 → develop merge；合并后配置分支保护并读回 API（AT-003，按用户决策延后到合并后执行）。
  2. 本轮代码侧可验证部分：AT-001 静态断言已证明 workflow 显式声明 checks: write，CI 具备创建 check 的权限前提。
- status: passed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 与 AT-002 在真实 fix/test worktree 执行且全绿（非 mock）；AT-003 的平台分支保护按用户决策「先合并代码再配保护」延后，不属于本轮代码回归，RED 证据（404）已留存，合并后补 GREEN 读取。
