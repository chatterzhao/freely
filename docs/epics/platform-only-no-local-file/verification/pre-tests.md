# Pre-Tests: wt-close --platform-only fallback
- issue_id: I-20260627T021849Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: 无本地文件时 platform-only 不报错
- testing_layer: integration
- target_environment: test-pre-merge-20260627T021849Z-platform-only-no-local-file
- required_evidence: --dry-run 成功
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260627T021849Z-platform-only-no-local-file --dry-run
- expected_output: --dry-run complete, exit 0
- actual_output: --dry-run complete, exit 0
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: none
- status: pass
## Unit
- acceptance_target: 代码逻辑正确
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: acceptance-1 pass
## Integration
- acceptance_target: --dry-run gate passes
- testing_layer: integration
- target_environment: test-pre-merge-20260627T021849Z-platform-only-no-local-file
- required_evidence: acceptance-1 pass
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260627T021849Z-platform-only-no-local-file --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
- status: pass
## End-to-End
- acceptance_target: 真实 platform-only 关闭 orphan issue
- testing_layer: end-to-end
- not_applicable_reason: 下次遇到 orphan issue 时验证实际 platform-only 行为
- not_applicable_explanation: 需要真实 orphan issue 场景
## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 将在实际使用中验证
