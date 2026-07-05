# Pre-Tests
- issue_id: I-20260703T162506Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: _update_agent_table_slot 正确更新 agent-table.toml
- acceptance_target: worker_slot 值改变
- testing_layer: unit
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- task_refs: A1
- target_environment: test-pre-merge
- required_evidence: 执行前 opencode → 执行后 claude
- evidence_level: mock
- artifact_ref: docs/B2-docs/git-worktree/closeout/raw-20260703T162506Z06Z/verification/test-evidence/acceptance-1.log
- test_command: grep worker_slot .freely/agent-table.toml
- expected_output: claude-apikey-ds-flash-auto
- expected_RED_output: opencode-apikey-ds-flash-auto (unchanged - bug)
- actual_RED_output: opencode-apikey-ds-flash-auto unchanged after "update"
- actual_output: worker_slot = "claude-apikey-ds-flash-auto"
- evidence_file: docs/B2-docs/git-worktree/closeout/raw-20260703T162506Z06Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: before fix: print lied about update, file never changed
## Unit/Integration/End-to-End/Real-Environment
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 covers unit verification
## Real-Environment
- real_environment_status: pass
- real_environment_reason: verified on test-pre-merge
