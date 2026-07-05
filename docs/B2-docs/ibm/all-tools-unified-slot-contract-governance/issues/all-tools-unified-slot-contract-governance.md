# Issue: all-tools-unified-slot-contract-governance

- issue_id: `I-20260401-0840-A`
- title: All-tools unified slot contract governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `all-tools-unified-slot-contract-governance`
- issue-name: `all-tools-unified-slot-contract-governance`
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-0840-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Ordered cross-tool fallback v1 is already in place, but Freely still lacks the final scheduler model requested by users:

- every tool participates in one slot contract
- current tool always tries own slots first
- cross-tool fallback always restarts from the leftmost configured priority
- every entered tool again sweeps its own slots before moving on
- all-tools-unavailable pins the earliest-known `tool + slot` recovery target

## Scope

1. Freeze `~/.ai-auth/<tool>-<slot>/` as canonical slot inventory truth for all tools.
2. Introduce a generic current-slot truth surface and stop relying on Codex-only naming for the scheduler pointer.
3. Generalize `ai-cli` inventory APIs so `login/save/list/switch/whoami/status/delete` can reason about per-tool slots, not only Codex.
4. Keep Codex watchdog strength intact, but let manager recovery iterate slots generically for every tool before cross-tool fallback.
5. Preserve `AI_FALLBACK_TOOLS` semantics: cross-tool fallback always restarts from the leftmost configured tool.
6. When all tools/slots are unavailable, keep no-launch and pin earliest-known `tool + slot` waiting truth.

## Non-Goals

1. Do not claim cross-tool resume equivalence.
2. Do not weaken Codex probe-first / switch-lock / no-launch invariants.
3. Do not require every non-Codex tool to instantly gain identical auth/probe semantics; capability gaps stay explicit.

## Acceptance

1. Old `I-20260331-1840-A` is closed as the ordered-fallback v1 slice; this owner becomes the canonical follow-on for all-tools slot parity.
2. `ai-cli` can enumerate slot inventory for arbitrary tools via `~/.ai-auth/<tool>-<slot>/`, and can persist per-tool current-slot truth outside Codex.
3. Generic `current_slot` truth exists for non-Codex tools; runtime still mirrors it into legacy `LAST_ACTIVE_SLOT` for compatibility.
4. When `AUTO_SWITCH_SLOT=true`, manager recovery tries the current tool's next slot before cross-tool fallback, even for non-Codex tools.
5. Once cross-tool fallback begins, manager always restarts from the leftmost configured tool and then enters that tool's slot family before moving on.
6. The waiting path pins earliest-known recovery as `tool + slot`, not only tool.
7. Focused regressions prove non-Codex same-tool slot rotation, earliest `tool + slot` waiting truth, and preserved left-to-right fallback order.
8. Live validation proves: current tool `kiro-cli` unavailable, current Codex slot dead, manager still reaches a later usable Codex slot before launch.

## Completion

- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/milestones.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`
- `docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-entry-blocked-cross-tool-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
- `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/code-reviews/20260401-all-tools-unified-slot-contract-verification.md`
- live validation on `develop`

## Next

- `2026-04-01 09:55 PDT` canonical develop validation and merge absorption are complete; this owner is closed.
- Future work may deepen per-tool probe/reset parity, but the shared slot contract and scheduler semantics should not be reopened here.
