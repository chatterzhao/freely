# Pre-Tests: review in test-pre-merge
- issue_id: I-20260625T222357Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pr-review-guarded 找到 test-pre-merge
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- test_command: grep -q "_test_wt=" bin/pr-review-guarded && grep -q "test-pre-merge" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- status: pass

### acceptance-2
- acceptance_target: 前置检查 dirty + sync
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep
- test_command: grep -q "worktree(s) dirty" bin/pr-review-guarded && grep -q "merge-base --is-ancestor" bin/pr-review-guarded && grep -q "cherry-pick" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- status: pass

### acceptance-3
- acceptance_target: SKILL.md 三层 review
- testing_layer: unit
- required_evidence: grep
- test_command: grep -q "代码质量" docs/system/workspace/skills/freely-tdd-review/SKILL.md && grep -q "完成度" docs/system/workspace/skills/freely-tdd-review/SKILL.md && grep -q "代码安全" docs/system/workspace/skills/freely-tdd-review/SKILL.md && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- status: pass

## Unit
- acceptance_target: 代码正确
- testing_layer: unit
- required_evidence: 3 acceptance PASS
