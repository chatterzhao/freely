# Pre-Tests
- issue_id: I-20260705T122651Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: B2 SKILL.md 中无缺 story/raw 层的 docs/epics 路径
- acceptance_target: grep 确认所有 code-reviews/verification/test-evidence 路径包含 raw- 或 {raw key}
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gitignore/raw-20260705T122651Z/verification/test-evidence/at-001.log
- test_command: '! grep -nE "docs/epics/[a-z-]+/code-reviews|docs/epics/[a-z-]+/verification|docs/epics/[a-z-]+/test-evidence" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md | grep -v "raw-\|{raw key}" && echo PASS'
- expected_output: PASS (no bare paths without raw/key)
- expected_RED_output: found bare paths
- actual_RED_output: 10处缺层路径
- actual_output: PASS
- evidence_file: at-001.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 10 处缺层
### acceptance-2
- id: AT-002
- requirement: pr-review-guarded 无 fallback 路径 docs/B2-docs/git-worktree/code-reviews
- acceptance_target: grep 确认无此字符串
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 不存在
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gitignore/raw-20260705T122651Z/verification/test-evidence/at-002.log
- test_command: '! grep -q "docs/B2-docs/git-worktree/code-reviews" bin/pr-review-guarded && echo PASS'
- expected_output: PASS
- expected_RED_output: found fallback string
- actual_RED_output: found line 184
- actual_output: PASS
- evidence_file: at-002.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前有 fallback
## Unit
- acceptance_target: AT-001 + AT-002
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001, AT-002
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary
- not_applicable_explanation: grep validation
- replacement_evidence: AT-001 + AT-002
