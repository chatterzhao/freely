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
- artifact_ref: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "docs/epics/\*/\*/raw-" bin/freely-review && ! grep "docs/issues/I-" bin/freely-review
- expected_output: 新glob匹配2处，旧I-*路径无匹配
- actual_output: 2 matches for new glob, exit 0 (old I-* not found)
- evidence_file: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-1.log
- blocker: (失败时填写)
- status: passed

### acceptance-2: pr-review-guarded uses new glob patterns
- id: AT-002
- requirement: bin/pr-review-guarded discovers I-* and pre-tests at new location
- acceptance_target: grep confirms new glob patterns in pr-review-guarded
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep output confirms all old paths replaced
- evidence_level: mock
- artifact_ref: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c "docs/epics/\*/\*/raw-" bin/pr-review-guarded && ! grep "docs/issues/I-" bin/pr-review-guarded
- expected_output: 新glob匹配9处，旧I-*路径无匹配
- actual_output: 9 matches for new glob, exit 0 (old I-* not found)
- evidence_file: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-2.log
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
- artifact_ref: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-3.log
- test_command: grep "epics_dir.glob" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py
- expected_output: matches epics_dir.glob("*/*/raw-*/issues/I-*.md")
- actual_output: for mf in sorted(epics_dir.glob("*/*/raw-*/issues/I-*.md")):
- evidence_file: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-3.log
- blocker: (失败时填写)
- status: passed

### acceptance-4: gate scripts use new path patterns
- id: AT-004
- requirement: checkpoint-guard, governance-merge-gate, governance-promotion-gate all updated
- acceptance_target: all three gate scripts have updated path patterns
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: grep output for all three scripts
- evidence_level: mock
- artifact_ref: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "epics.*\*.*\*.*\*" docs/system/workspace/scripts/quality/checkpoint-guard && grep -c "raw-\*/" docs/system/workspace/scripts/quality/governance-promotion-gate && grep -c "epics/.*issues/I-" docs/system/workspace/scripts/quality/governance-merge-gate
- expected_output: checkpoint-guard=2, promotion-gate=1, merge-gate=2
- actual_output: checkpoint-guard=2 (scope_for_path + story_scope_for_path), promotion-gate=1 (staged glob), merge-gate=2 (I-* check + milestone lookup)
- evidence_file: docs/epics/chat-refactor/comment-discuss-split/raw-20260628T005815Z/verification/test-evidence/acceptance-4.log
- blocker: (失败时填写)
- status: passed

## Unit
- acceptance_target: 所有6个文件的路径更新验证通过grep检查
- testing_layer: unit
- target_environment: fix/raw-20260628T182243Z-code-path-structure-update worktree
- required_evidence: 每个acceptance item的grep输出均为预期结果
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: (如不适用填写)
- not_applicable_explanation: (如不适用填写)
- replacement_evidence: (如不适用填写)

## Integration
- acceptance_target: not applicable — 纯路径字符串更新，无模块间集成面
- testing_layer: integration
- target_environment: not_applicable
- required_evidence: not_applicable
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次仅修改脚本中的glob路径字符串，不涉及模块间数据流或协作，无集成面需要测试
- replacement_evidence: 各脚本的grep检查已覆盖全部改动面

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
- real_environment_status: not_tested
- real_environment_reason: 路径更新属内部治理变更，真实环境(platform API)无需验证
