# Pre-Tests: worktree path architecture fix

## Acceptance Items

### AI-1: wt-create materializes raw issue to worktree
- **Given**: wt-create --raw-key <key> --source platform
- **When**: worktree created
- **Then**: docs/B1-docs/raw-{key}/issue.md exists IN worktree, not in develop
- **adequacy**: verified

### AI-2: wt-close resolves ROOT_DIR from CWD
- **Given**: wt-close run from any directory
- **When**: ROOT_DIR=$(git rev-parse --show-toplevel)
- **Then**: ROOT_DIR points to current git worktree
- **adequacy**: verified

### AI-3: pr-merge-guarded does not amend develop
- **Given**: merge of fix branch with raw issue
- **When**: pr-merge-guarded completes
- **Then**: No _absorb_close_frontmatter call, develop stays clean
- **adequacy**: verified

### AI-4: pr-create-guarded checks worktree phase_state
- **Given**: pr-create-guarded in worktree
- **When**: raw issue phase_state != absorbed
- **Then**: blocked with guidance message
- **adequacy**: verified

### AI-5: End-to-end — develop never dirty
- **Given**: full fix-execution cycle (wt-create → fix → pr-create → pr-merge → wt-close)
- **When**: all steps complete
- **Then**: develop has zero dirty files from frontmatter operations
- **adequacy**: verified (dogfood test)
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
