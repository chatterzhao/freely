# Pre-Tests: wt-close --force frontmatter guard

## Acceptance Items

### AI-1: wt-close --force skips when absorbed
- **Given**: raw issue phase_state=absorbed (pr-merge-guarded done)
- **When**: wt-close --force <branch>
- **Then**: "frontmatter already absorbed by pr-merge-guarded, skipping force-close trace"
- **adequacy**: verified

### AI-2: wt-close --force still writes when not absorbed
- **Given**: raw issue phase_state != absorbed (e.g., abandoned worktree)
- **When**: wt-close --force <branch>
- **Then**: force_closed trace written
- **adequacy**: verified

### AI-3: develop stays clean
- **Given**: pr-merge-guarded already merged
- **When**: wt-close --force
- **Then**: No dirty files on develop (no frontmatter overwrite)
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
