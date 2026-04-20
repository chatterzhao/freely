# Pre-tests: latest-manager-continuity-worker-consumption-governance

## Success Criteria

### Pre-merge success criteria

1. delegated continuation 的 prompt 注入只消费当前 manager continuity 之后的新 handoff，不再自动重放更早 supervision round 的 backlog。
2. `Human chat intake queue` 不再把 `STATUS="delegated"` 的 intake 伪装成 front-door 未分诊聊天。
3. `live-status` 仍能正确显示 delegated item 计数，但 front-door intake snapshot 不再重复显示 delegated 项。

### Post-merge success criteria

1. 在 canonical `develop` 上真实执行 `freely chat` 后，新治理插话会成为当前主管轮次消费的 delegated continuation，而不会被旧 `runtime-lifecycle-validation` continuation 抢占。
2. 当前主管 prompt 可以把旧 `runtime-lifecycle-validation` worktree 仅当作 inventory 观察对象，而不是当前 delegated continuation handoff。
3. 这次 same-family repair 完成后，当前修复 worktree 走完 `feature -> test-pre-merge-* -> develop`，并清理已完成的 feature 与 pre-merge worktree / branch。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `manager prompt filters delegated continuation backlog older than the latest manager continuity`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

### PT-2
- id: `PT-2`
- requirement: `front-door intake snapshot excludes delegated items while live-status still reports delegated counts truthfully`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

### PT-3
- id: `PT-3`
- requirement: `canonical develop replay consumes the fresh success-standard governance interruption instead of reusing the stale runtime-lifecycle-validation continuation`
- evidence_level: `dogfood`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`
