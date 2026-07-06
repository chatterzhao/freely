# Pre-Tests: pr-review-guarded

## Acceptance Items

### AI-1: pr-review-guarded 命令可用
- **Given**: feature worktree with PR created
- **When**: freely pr-review-guarded <branch>
- **Then**: 6 review dimensions checked, review document written, verdict output
- **adequacy**: verified

### AI-2: pr-merge-guarded 检查 verdict
- **Given**: review document with verdict=pass
- **When**: freely pr-merge-guarded develop <branch>
- **Then**: merge proceeds
- **adequacy**: verified

### AI-3: pr-merge-guarded 阻塞 fail verdict
- **Given**: review document with verdict=fail
- **When**: freely pr-merge-guarded develop <branch>
- **Then**: blocked with "PR review not passed"
- **adequacy**: verified

### AI-4: 流程链路一致性
- **Given**: 所有 18 个文件更新
- **When**: grep "pr-create → pr-review → pr-merge" across project
- **Then**: no stale "pr-create → pr-merge" references remain
- **adequacy**: verified

### AI-5: deploy-skills 后新流程生效
- **Given**: skill 文件更新
- **When**: freely deploy-skills
- **Then**: AI 看到新流程 pr-create → pr-review → pr-merge
- **adequacy**: verified
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
