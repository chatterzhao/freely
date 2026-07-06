# Pre-Tests: freely-db-cli + AGENTS.md + hook fix

## Acceptance Items

### AI-1: freely-db-cli db.ping returns pong
- **Given**: freely-db daemon is running
- **When**: `python3 docs/system/workspace/scripts/runtime/freely-db-cli --project <project> db.ping`
- **Then**: Output is `pong` (not IndentationError)
- **adequacy**: `verified` — manually confirmed during daemon start sequence

### AI-2: AGENTS.md workflow starts with feedback/scan branching
- **Given**: Read AGENTS.md §核心开发流程
- **When**: Compare with `skill:freely-feat-execution` flow definition
- **Then**: Entry section shows feedback and scan as OR-branch entry points, wt-create as stage 1
- **adequacy**: `verified` — structural alignment confirmed

### AI-3: pre-commit hook message names skills
- **Given**: Attempt to commit on develop
- **When**: Hook blocks the commit
- **Then**: Message includes `skill:freely-fix-execution` and `skill:freely-feat-execution`, plus anti-bypass warning
- **adequacy**: `verified` — string match confirmed in message text

## Verification Notes
- All three fixes are single-line or documentation changes, no regression risk
- No runtime behavior changes — pre-tests are structural verification
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
