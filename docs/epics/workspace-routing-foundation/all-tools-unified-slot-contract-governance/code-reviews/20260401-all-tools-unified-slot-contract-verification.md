# Verification: all-tools-unified-slot-contract-governance

- issue_id: `I-20260401-0840-A`
- reviewer: `codex`
- verdict: `pass`

## Verified

1. `~/.ai-auth/<tool>-<slot>/` is now the canonical slot inventory contract for every runtime tool, including tools that only expose generic singleton slot containers today.
2. `ai-cli` now supports generic tool slot inventory operations beyond Codex:
   - `login/save` create per-tool slot containers
   - `switch/list/whoami/status/delete` consume the shared current-slot surface
3. Runtime scheduler truth now distinguishes `current_tool/current_slot` from `last_*` observability truth, while still mirroring `current_slot` to legacy `LAST_ACTIVE_SLOT` for compatibility.
4. Manager recovery is slot-first for every tool family that has slot inventory:
   - Codex keeps its stronger probe-first watchdog
   - non-Codex tools now rotate same-tool slots before cross-tool fallback
5. Once same-tool recovery is exhausted, cross-tool fallback restarts from the leftmost `AI_FALLBACK_TOOLS` entry and then sweeps that tool's slots before moving on.
6. If all tools and slots are unavailable, manager launch stays blocked and waiting truth now records earliest-known `tool + slot`, not only tool.
7. Live validation on canonical `develop` proved the requested path end-to-end:
   - current tool `kiro-cli` was blocked by `kiro_monthly_request_limit`
   - current Codex slot `worahe1000@outlook-com-2` was dead
   - control plane selected later usable Codex slot `worahe1001@outlook-com-2`
   - Codex launch then started from that recovered slot
8. Live validation also surfaced and verified a scheduler fix: single-slot failure no longer loops on the same tool when no distinct next slot exists; it now falls through to cross-tool fallback.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-login-creates-slot-container`
2. `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
3. `bash docs/system/workspace/scripts/tests/test-ai-cli-login-creates-incremented-slot`
4. `bash docs/system/workspace/scripts/tests/test-ai-cli-generic-tool-switch-persists-current-slot`
5. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-entry-blocked-cross-tool-fallback`
7. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
8. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
9. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
10. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-non-codex-slot-first-then-cross-tool`
11. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
12. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-tool-slot`
13. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-single-slot-failure-falls-through-to-cross-tool`
14. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
15. `./bin/governance-check`

## Live Evidence

1. Real Codex slot sweep proved the dead slot inventory assumption was correct only for `worahe1000@outlook-com-2` and later siblings, not `worahe1000@outlook-com-1`:
   - forcing current slot to `worahe1000@outlook-com-2`
   - running `bash bin/ai switch codex`
   - observing switch output mark `worahe1000@outlook-com-2` as unusable and move the pointer to `worahe1001@outlook-com-2`
2. Canonical `develop` runtime event log recorded the cross-tool selection with recovered slot:
   - `2026-04-01T09:39:33Z event=tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex active_slot=worahe1001@outlook-com-2 reason=kiro_monthly_request_limit launch_kind=fresh_with_handoff launch_blocked=false earliest_reset=none earliest_slot=none owner=ensure_manager_control_plane`
3. Canonical `develop` runtime event log then recorded the actual launch:
   - `2026-04-01T09:39:48Z event=ai_launch_begin supervisor_pid=1455 tool=codex launch_kind=fresh rotation_reason=initial_start`
4. After the live recovery, the machine current-slot pointer confirmed the new target:
   - `~/.ai-auth/.codex-current-slot = worahe1001@outlook-com-2`

## Residual Risk

1. Codex still has the strongest probe/watchdog parity; `kiro-cli`, `cc`, `iflow`, and `opencode` now share the unified slot contract and generic scheduler path, but not yet Codex-equivalent auth/probe depth.
2. earliest-recovery hints remain strongest where tools expose structured reset truth; tools without reset metadata still participate as unavailable targets without equally rich timing hints.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
