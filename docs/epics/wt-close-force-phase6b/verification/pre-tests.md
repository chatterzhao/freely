# Pre-Tests: wt-close Phase 6b force fix
- issue_id: I-20260626T130431Z-A

### acceptance-1
- acceptance_target: Phase 6b with --force prints severe warning
- testing_layer: unit
- test_command: grep -c '严重警告.*已经用.*force.*参数彻底丢弃' docs/system/workspace/scripts/worktree/wt-close
- expected_output: 1
- actual_output: 1 — warning present in force branch
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

### acceptance-2
- acceptance_target: Phase 6b without --force uses safe git worktree remove (no --force)
- testing_layer: unit
- test_command: grep -A20 'if \[\[ "\$FORCE" == true \]\]' docs/system/workspace/scripts/worktree/wt-close | grep 'git worktree remove "' | grep -v -- '--force'
- expected_output: safe remove line present in else branch
- actual_output: git worktree remove "$_tp_wt" without --force in else branch
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed

### acceptance-3
- acceptance_target: --force 时用 -D, 非 --force 时用 -d
- testing_layer: unit
- test_command: grep -A20 'if \[\[ "\$FORCE" == true \]\]' docs/system/workspace/scripts/worktree/wt-close | grep 'git branch -D' && grep -A20 'else' docs/system/workspace/scripts/worktree/wt-close | tail -15 | grep 'git branch -d '
- expected_output: -D in force branch, -d in else branch
- actual_output: git branch -D in force branch, git branch -d in else branch
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed

### acceptance-4
- acceptance_target: bash syntax valid
- testing_layer: integration
- test_command: bash -n docs/system/workspace/scripts/worktree/wt-close && echo "OK"
- expected_output: OK
- actual_output: Syntax OK
- evidence_file: .freely/run/test-evidence/acceptance-4.log
^- status: passed

### acceptance-5
- acceptance_target: wt-close --help still works
- testing_layer: end-to-end
- test_command: freely wt-close --help 2>&1 | head -3
- expected_output: Usage text
- actual_output: Usage text displayed correctly
- evidence_file: .freely/run/test-evidence/acceptance-5.log
^- status: passed
