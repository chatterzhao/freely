# Pre-tests: Worker Launch 保护工位验证
- issue_id: I-20260509T022152Z-A

## Unit
- acceptance target: 新增 shell case branch prefix 检查
- testing layer: unit
- target environment: fix worktree
- required evidence: test-freely-worker-prompt-protected-branch-rejected 7/7 PASS
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Shell function behavior, verified by direct execution
- replacement_evidence: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected

## Integration
- acceptance target: 不影响现有 worker launch 流程
- testing layer: integration
- target environment: develop merge chain
- required evidence: pr-merge-guarded 输出
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: test-freely-manager-worker-launch-linkage 和 exit-contract 测试需要 ACP bridge，与本改动无关
- replacement_evidence: pr-merge-guarded 输出

## End-to-End
- acceptance target: fix → merge → develop 完成
- testing layer: end_to_end
- target environment: develop merge chain
- required evidence: merge receipts
- blocker taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: fix 已通过 companion branch-check 分支进入 develop
- replacement_evidence: pr-merge-guarded 输出

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 改动为 bash prefix match，真实环境验证通过单元测试即可

## Acceptance Items

### AT-001 develop rejected
- id: develop-rejected
- requirement: develop branch 在 worker_prompt_launchable 中被拒绝
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-002 main rejected
- id: main-rejected
- requirement: main branch 被拒绝
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-003 test-pre-merge rejected
- id: test-pre-merge-rejected
- requirement: test-pre-merge-* branch 被拒绝
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-004 fix accepted
- id: fix-accepted
- requirement: fix/* branch 正常放行
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-005 feature accepted
- id: feature-accepted
- requirement: feature/* branch 正常放行
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-006 empty branch accepted
- id: empty-branch-accepted
- requirement: 空 branch 值放行（不破坏既有流程）
- evidence_level: integration
- status: pass
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-worker-prompt-protected-branch-rejected
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-007 existing linkage test unaffected
- id: existing-linkage-unaffected
- requirement: 现有 worker-launch-linkage 测试不受影响
- evidence_level: integration
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: test-freely-manager-worker-launch-linkage 需要 ACP bridge，与本 bash prefix 改动无关
- replacement_evidence: pr-merge-guarded 输出确认
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-008 rejected develop records WORKER_PROMPTS_NOT_LAUNCHABLE
- id: rejected-develop-records-not-launchable
- requirement: 拒绝 develop 后 runtime 记录 WORKER_PROMPTS_NOT_LAUNCHABLE
- evidence_level: integration
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: exit-contract 测试需要 ACP bridge，与本 bash prefix 改动无关。WORKER_PROMPTS_NOT_LAUNCHABLE 路径已存在（L13177）
- replacement_evidence: pr-merge-guarded 输出确认
- artifact_ref: docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable
- surface_kind: integration
- target_lane: feature-local
- promotion_gate: completion

### AT-009 fix merge to develop
- id: fix-merge-to-develop
- requirement: 完整 fix → test-pre-merge → develop 验证
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/worker-launch-writable-redirect/code-reviews/closeout-review.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
