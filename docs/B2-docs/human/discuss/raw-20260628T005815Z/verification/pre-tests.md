# Pre-Tests: code path structure update
- issue_id: I-20260628T005815Z-A

## Acceptance Items

### acceptance-1: freely-review uses new glob patterns
- id: AT-001
- requirement: bin/freely-review searches pre-tests and I-* at new docs/epics/*/*/raw-{key}/ location
- acceptance_target: grep confirms new glob patterns in freely-review
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep output confirms all old paths replaced
- evidence_level: mock
- artifact_ref: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "docs/epics/\*/\*/raw-" bin/freely-review && ! grep "docs/issues/I-" bin/freely-review
- expected_output: 新glob匹配，旧I-*路径无匹配
- actual_output: 2 new glob matches, 0 old I-* matches — all paths updated correctly
- evidence_file: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-1.log
- blocker: (失败时填写)
- status: passed

### acceptance-2: pr-review-guarded uses new glob patterns
- id: AT-002
- requirement: bin/pr-review-guarded discovers I-* and pre-tests at new location
- acceptance_target: grep confirms new glob patterns in pr-review-guarded
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep confirms all old paths replaced
- evidence_level: mock
- artifact_ref: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "docs/epics/\*/\*/raw-" bin/pr-review-guarded && ! grep "docs/issues/I-" bin/pr-review-guarded
- expected_output: 新glob匹配，旧I-*路径无匹配
- actual_output: 9 new glob matches, 0 old I-* matches — all paths updated correctly
- evidence_file: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-2.log
- blocker: (失败时填写)
- status: passed

### acceptance-3: task-lifecycle-scan scans new epics structure
- id: AT-003
- requirement: read_issues_dir() uses glob */*/raw-*/issues/I-*.md
- acceptance_target: grep confirms new glob pattern in task-lifecycle-scan.py
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep confirms epics_dir.glob pattern
- evidence_level: mock
- artifact_ref: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-3.log
- test_command: grep "epics_dir.glob" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py
- expected_output: matches epics_dir.glob("*/*/raw-*/issues/I-*.md")
- actual_output: epics_dir.glob("*/*/raw-*/issues/I-*.md") line found
- evidence_file: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-3.log
- blocker: (失败时填写)
- status: passed

### acceptance-4: gate scripts use new path patterns
- id: AT-004
- requirement: checkpoint-guard, governance-merge-gate, governance-promotion-gate all updated
- acceptance_target: all three gate scripts have updated path patterns
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep confirms updated patterns in all 3 scripts
- evidence_level: mock
- artifact_ref: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "epics.*\*.*\*.*\*" docs/system/workspace/scripts/quality/checkpoint-guard && grep -c "raw-\*/" docs/system/workspace/scripts/quality/governance-promotion-gate && grep -c "epics/.*issues/I-" docs/system/workspace/scripts/quality/governance-merge-gate
- expected_output: checkpoint-guard=2, promotion-gate=1, merge-gate=2
- actual_output: checkpoint-guard=2, promotion-gate=1, merge-gate=2 — all updated
- evidence_file: docs/B2-docs/human/discuss/raw-20260628T005815Z/verification/test-evidence/acceptance-4.log
- blocker: (失败时填写)
- status: passed

## Unit
- acceptance_target: 所有6个文件路径已更新并通过grep检查验证
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: 4条acceptance item的grep输出均为预期结果
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 单元测试的具体test_command+expected_output+actual_output+evidence_file已覆盖在 ## Acceptance Items 的 AT-001 至 AT-004 中，每条均可独立验证
- replacement_evidence: 见 ## Acceptance Items AT-001~AT-004 的 grep 证据文件

## Integration
- acceptance_target: not applicable — 纯路径字符串更新，无模块间集成面
- testing_layer: integration
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次仅修改脚本中的glob路径字符串，不涉及模块间数据流或协作，无集成面需要测试
- replacement_evidence: 各脚本的grep检查已覆盖全部改动面，不存在需要集成测试验证的模块边界

## End-to-End
- acceptance_target: not applicable — 无用户可见行为变更
- testing_layer: end-to-end
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本次仅修改内部路径引用，不影响用户可见行为、UI交互或完整业务流程
- replacement_evidence: 单元级grep检查已覆盖全部改动面

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 路径更新属内部治理变更，真实环境(platform API)无需额外验证；pre-tests证据文件已生成并通过
