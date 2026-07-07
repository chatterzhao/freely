# Pre-Tests: issue-sync idempotent + adapter fix
- issue_id: I-20260707T145323Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: issue-sync close 两次后 git status 无变化
- acceptance_target: 幂等——第二次 close 不产生 diff
- testing_layer: unit
- target_environment: test-pre-merge-20260707T145323Z-issue-sync-idempotent-close
- required_evidence: git status 确认无修改
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260707T145323Z/verification/test-evidence/acceptance-1.log
- test_command: "issue-sync close raw-xxx && git add . && git commit -m first && issue-sync close raw-xxx && git status --porcelain"
- expected_output: "(empty = no diff, idempotent)"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 issue-sync close 写 updated_at，第二次跑产生新 commit
## Unit
- acceptance_target: bash -n 通过 + git status 幂等
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 行为测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 行为测试验证幂等性
- replacement_evidence: AT-001 行为测试
## Integration
- acceptance_target: pr-merge-guarded 不再死循环
- testing_layer: integration
- target_environment: test-pre-merge-20260707T145323Z-issue-sync-idempotent-close
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 实际场景验证
- replacement_evidence: wt-create 成功 + pr-merge-guarded 不再循环
## End-to-End
- acceptance_target: pr-create-guarded 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 行为测试通过
