# Issue: runtime-network-failure-taxonomy-and-bounded-recovery-governance

- issue_id: `I-20260330-2358-A`
- title: Runtime network failure taxonomy and bounded recovery governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-network-failure-taxonomy-and-bounded-recovery-governance`
- issue-name: `runtime-network-failure-taxonomy-and-bounded-recovery-governance`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/candidates.md#c-20260330-2358-a`
- source_brainstorm: `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md`
  - `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already had partial network semantics:

- `oauth_unreachable` blocks preflight inventory refresh
- proxy inheritance is handled in project-scoped config truth
- slot/tool fallback already exists for slot-local or tool-local availability failures

But runtime still lacked an explicit execution-time network taxonomy. When a running tool exited due to network timeout, upstream reset, proxy-connect failure, or similar dependency outages, the supervisor could collapse the event into generic `ai_exit_rc_*` handling. That risked three incorrect behaviors:

1. treating network dependency failures like slot/account failures,
2. falling into blind relaunch churn, and
3. losing observability about whether recovery should stay on the current `tool + slot`.

This owner fixes that narrow gap without redesigning the broader availability system.

## Scope

1. Detect execution-time network failures and explicit proxy-config-invalid signals from cycle logs.
2. Classify them into canonical runtime reasons:
   - `execution_network_transient`
   - `execution_network_persistent`
   - `proxy_config_invalid`
3. Persist bounded retry/cooldown state for the current project and current `tool + slot`.
4. Block same-tool slot recovery and cross-tool fallback while the current network-local retry/cooldown window is active.
5. Relaunch only the current `tool + slot` once the bounded retry window expires.
6. Lock the behavior with focused regressions and write the contract back to workspace tool truth.

## Non-Goals

1. Do not redesign `oauth_unreachable`; keep it as the preflight / inventory-stage network blocker.
2. Do not route execution-time network failures into slot/tool fallback.
3. Do not claim earliest-reset parity or dedicated network probing across every supported tool.
4. Do not widen this slice into generic dependency-health orchestration beyond the current bounded state machine.

## Acceptance

1. Execution-time network errors are no longer left as plain `ai_exit_rc_*` when they match the new bounded taxonomy.
2. `proxy_config_invalid` is modeled separately from transient/persistent execution-time failures.
3. Execution-time network-local reasons do not trigger same-tool slot rotation or cross-tool fallback by default.
4. While a network-local retry/cooldown window is active, `ensure_manager_once` does not relaunch or switch away from the current `tool + slot`.
5. Once the retry window expires, manager recovery relaunches the same current `tool + slot`.
6. Focused regressions prove classification, blocking, and bounded relaunch behavior.
7. Workspace truth sources document that runtime network-local failures stay on bounded in-place recovery rather than slot/tool fallback.

## Completion

- `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/brainstorms.md`
- `docs/pre-brainstorms/20260330-2358--network-failure-recovery-governance/candidates.md`
- `docs/pre-brainstorms/INDEX.md`
- `docs/milestones.md`
- `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-network-failure-taxonomy-and-bounded-recovery-governance/code-reviews/20260401-runtime-network-failure-taxonomy-and-bounded-recovery-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-blocks-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-relaunches-current-slot`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-blocks-fallback`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-network-failure-relaunches-current-slot`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
- `./bin/governance-check`

## Next

- `2026-04-01 09:55 PDT` bounded network-local recovery has been absorbed into canonical `develop` and verified; this owner is closed.
- Any future work that widens from bounded in-place retry/cooldown into broader dependency-health orchestration or shared reset prediction must open a new lifecycle.
