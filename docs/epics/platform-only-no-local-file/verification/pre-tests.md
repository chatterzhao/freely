# Pre-Tests; issue_id: I-20260627T021849Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: 无本地文件时 platform-only 不报错，fallback 到平台搜索
- testing_layer: integration
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260627T021849Z-platform-only-no-local-file --dry-run
- expected_output: --dry-run complete; actual_output: --dry-run complete; status: pass
## Integration
- acceptance_target: dry-run pass; testing_layer: integration
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260627T021849Z-platform-only-no-local-file --dry-run
- expected_output: --dry-run complete; actual_output: --dry-run complete; status: pass
## End-to-End
- acceptance_target: 真实 platform-only 关闭 orphan issue; testing_layer: end-to-end
- not_applicable_reason: 下次遇到 orphan issue 时验证
## Real-Environment; real_environment_status: not_tested
