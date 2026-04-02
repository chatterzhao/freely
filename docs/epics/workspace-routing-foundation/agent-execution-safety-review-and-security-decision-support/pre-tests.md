# Pre-Tests: agent-execution-safety-review-and-security-decision-support

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `execution-boundary-contract` 明确：
   - tool flags、project-local config、launch-time injection、observed posture 需要在同一 capability contract 下可比对
   - execution-boundary review 属于可复用 capability，而不是单个产品 consent surface
2. `reviewer-committee-contract` 明确：
   - reviewer / committee semantics 是内部 AI 决策增强
   - 不把用户拉回逐步审批链路
3. `nonblocking-guidance-boundary` 明确：
   - safeguard recommendation 属于 capability 输出
   - safeguard 不完整默认不直接升级成 runtime blocker

### Post-merge integration acceptance

1. follow-on implementation owner 必须能直接引用这一条 owner 作为：
   - execution-boundary review 的 contract source
   - reviewer / committee semantics 的 contract source
2. capability owner 与 product owner 的边界必须保持稳定：
   - 不接管 activation consent
   - 不重写 Freely 默认 autonomy posture
3. follow-on skill / reference / runtime-helper 实现不应重新定义这条 owner 已冻结的最小 contract。

### Post-merge application-native real-environment acceptance

1. future runtime implementation 应能基于这条 owner：
   - 输出 execution-boundary review summary
   - 拉起 reviewer / committee support
   - 写回 reviewer-backed continuation evidence
2. future runtime implementation 若缺 capability 实现，可以暂不适用，但不允许回退到“用户逐步审批才是默认主路”的表述。

### Post-merge end-to-end dogfood acceptance

1. future dogfood sessions 讨论 reviewer / committee semantics 时，应能直接引用这条 owner，而不是每轮重新口头定义。
2. future security capability splits 继续拆 supply-chain、secret/artifact exposure、incident remediation 时，不得回灌并重写这条 owner 的边界。

### Non-Goals

1. 本轮不实现真实 security skill / runtime helper。
2. 本轮不定义 Freely 默认强制 sandbox 或强制交互批准。
3. 本轮不把 supply-chain、secret scanning、artifact exposure、incident remediation 一次性并入同一个 owner。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `issue artifacts freeze one reusable execution-boundary review contract across tool flags, project config, launch-time injection, and observed posture`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/issues/agent-execution-safety-review-and-security-decision-support.md`

### PT-2
- id: `PT-2`
- requirement: `issue artifacts freeze reviewer and committee semantics as internal AI decision enhancement rather than user approval replacement`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/agent-execution-safety-review-and-security-decision-support/prd.md`

### PT-3
- id: `PT-3`
- requirement: `issue artifacts state that safeguard recommendation is supported output without turning safeguard incompleteness into the default blocker`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/candidates.md`

## Pre-merge Focused Regression / Smoke

1. acceptance target:
   - IBM artifacts are internally consistent and clearly separate capability owner from product owner
2. testing layer:
   - wording / structure review
3. target environment:
   - feature worktree
4. required evidence:
   - `./bin/governance-check`
5. blocker taxonomy:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - repair IBM artifacts in the feature worktree before claiming materialization complete

## Post-merge Integration Acceptance

1. acceptance target:
   - later skill/runtime-helper work can cite one stable owner for execution-boundary review and reviewer committee semantics
2. testing layer:
   - contract review against canonical `develop`
3. target environment:
   - `develop`
   - protected verification worktree
4. required evidence:
   - issue artifacts are merged and referenced by follow-on capability work
5. blocker taxonomy:
   - `definition_missing`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
6. failure handling / replay expectation:
   - if follow-on work still needs to renegotiate capability boundary, reopen from a feature worktree and repair the owner issue artifacts

## Post-merge Application-Native Real-Environment Acceptance

1. acceptance target:
   - future runtime can use reviewer/committee support without confusing it with user-step approval
2. testing layer:
   - future runtime replay against this owner
3. target environment:
   - live Freely runtime on `develop`
4. required evidence:
   - follow-on implementation cites this owner
5. why_not_applicable:
   - this IBM slice only freezes capability contract; it does not yet ship live runtime behavior
6. replacement_evidence:
   - stable owner contract exists for the next implementation slice

## Post-merge End-to-End Dogfood Acceptance

1. acceptance target:
   - future dogfood sessions can escalate to reviewer/committee semantics without conversationally redefining the model each time
2. testing layer:
   - future dogfood replay against canonical owner
3. target environment:
   - canonical `develop` runtime
4. required evidence:
   - follow-on implementation points to this owner for reviewer/committee behavior
5. why_not_applicable:
   - this IBM slice does not yet ship the actual skill/runtime helper
6. replacement_evidence:
   - issue / prd / pre-tests / tasks define the contract for the next implementation slice
