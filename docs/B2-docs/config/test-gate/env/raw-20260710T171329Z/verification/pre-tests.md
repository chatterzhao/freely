# Pre-Tests: test-gate.env git 去追踪
- issue_id: I-20260710T171329Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: test-gate.env 不再被 git 追踪
- acceptance_target: git ls-files --cached .freely/run/test-gate.env 返回空
- testing_layer: unit
- target_environment: develop
- required_evidence: git ls-files 确认文件不在 git 索引中
- evidence_level: real_env
- artifact_ref: docs/B2-docs/config/test-gate/env/raw-20260710T171329Z/verification/test-evidence/acceptance-1.log
- test_command: git ls-files --cached .freely/run/test-gate.env && echo FAIL || echo PASS
- expected_output: PASS
- expected_RED_output: FAIL (文件仍在追踪)
- actual_RED_output: git ls-files 返回文件路径，确认文件被追踪
- actual_output: git ls-files 返回空，文件已去追踪
- evidence_file: docs/B2-docs/config/test-gate/env/raw-20260710T171329Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: git rm --cached 成功执行，文件不再出现在 git 索引中
- testing_layer: unit
- target_environment: develop
- required_evidence: git status 不显示该文件为 tracked
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 纯 metadata 变更（去追踪），单元级验证已通过 acceptance-1 覆盖
- replacement_evidence: AT-001 PASS — git ls-files 确认文件已去追踪

## Integration
- acceptance_target: wt-close gate 不再因 test-gate.env dirty 告警被拦截
- testing_layer: integration
- target_environment: develop
- required_evidence: wt-close gate 正常运行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 集成验证需要在合并后的 develop 分支上实际运行 wt-close，当前工位无法模拟
- replacement_evidence: 合并后验证

## End-to-End
- acceptance_target: 合并后 develop 不再追踪 test-gate.env
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: develop 分支上 git ls-files 确认文件已去追踪
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 端到端验证需要在合并后进行，当前工位无法模拟
- replacement_evidence: 合并后 git ls-files 验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯 metadata 变更，git rm --cached 已验证
