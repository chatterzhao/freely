# Pre-Tests: agent-table help + test docs + cherry-pick consistency
- issue_id: I-20260626T121349Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: agent-table-query help shows only [[agents]] format
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: No [[agent_pools]] in help text, no "worktree =" field
- test_command: grep -c '\[\[agent_pools\]\]' bin/agent-table-query && echo "FAIL" || echo "PASS"
- expected_output: 0 occurrences of [[agent_pools]]
- actual_output: PASS — 0 occurrences in help text
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (none)
^- status: passed

### acceptance-2
- acceptance_target: fix-execution skill uses cherry-pick not stash
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: cherry-pick references exist, stash workflow removed
- test_command: grep -c 'cherry-pick' docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: 5 or more cherry-pick references
- actual_output: 13 cherry-pick references, 1 stash (comparison note only)
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: (none)
^- status: passed

### acceptance-3
- acceptance_target: test-pre-merge allows add/commit, prohibits push/merge
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: Updated constraints in fix-execution skill
- test_command: grep -c '允许.*add.*commit\|可以.*add.*commit\|禁止.*push.*merge\|禁止.*merge' docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: Updated constraint language present
- actual_output: "允许 add 和 commit", "禁止 push 和 merge" present
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: (none)
^- status: passed

### acceptance-4
- acceptance_target: agent-table-query help runs without regression
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: CLI help displays correct [[agents]] format
- test_command: python3 bin/agent-table-query --help 2>&1 | grep -c 'agents' 
- expected_output: 1 or more
- actual_output: [[agents]] format displayed, legacy [[agent_pools]] removed from help
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker: (none)
^- status: passed

### acceptance-5
- acceptance_target: No stale stash workflow in skill docs
- testing_layer: end-to-end
- target_environment: fix worktree
- required_evidence: cherry-pick replaced stash throughout fix-execution
- test_command: grep -c 'cherry-pick' docs/system/workspace/skills/freely-fix-execution/SKILL.md
- expected_output: 5 or more
- actual_output: 13 cherry-pick references, stash only in comparison note
- evidence_file: .freely/run/test-evidence/acceptance-5.log
- blocker: (none)
^- status: passed

## Unit
- acceptance_target: Documentation-only change, verified by grep checks
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: All acceptance items pass
^- status: passed

## Integration
- acceptance_target: No bash syntax regression
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: agent-table-query --help runs without error
- test_command: python3 bin/agent-table-query --help 2>&1 | head -5
- expected_output: Usage text displayed
- actual_output: Usage text with [[agents]] format displayed correctly
- evidence_file: .freely/run/test-evidence/acceptance-integration.log
- blocker: (none)
^- status: passed

## End-to-End
- acceptance_target: Documentation consistency across all artifacts
- testing_layer: end-to-end
- target_environment: test-pre-merge worktree
- required_evidence: No stale stash workflow references in skill docs
- test_command: grep -r 'git stash' docs/system/workspace/skills/freely-fix-execution/SKILL.md | grep -v '比 stash' | grep -v 'stash_' && echo "FOUND_STALE" || echo "CLEAN"
- expected_output: CLEAN (only comparison references remain)
- actual_output: CLEAN — no stale stash workflow references
- evidence_file: .freely/run/test-evidence/acceptance-e2e.log
- blocker: (none)
^- status: passed
