# Verification: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- verification_date: `2026-04-22`
- branch: `feature/live-status-hang-root-cause-20260422`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-live-status-hang-root-cause`
- verifier: `codex`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`
3. `bash docs/system/workspace/scripts/tests/test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path`
4. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-launch-in-flight-state`
6. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
7. `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
8. `bash docs/system/workspace/scripts/tests/test-freely-prompt-build-failure-keeps-supervisor-alive`
9. `bash docs/system/workspace/scripts/tests/test-freely-live-status`
10. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`
11. `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`
12. `bash docs/system/workspace/scripts/tests/test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed`
13. `bash docs/system/workspace/scripts/tests/test-freely-ai-pid-validation-supported-tools`
14. `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal`
15. `bash docs/system/workspace/scripts/tests/test-freely-live-status-active-manager-skips-fleet-refresh`
16. `bash docs/system/workspace/scripts/tests/test-freely-live-status-uses-status-signals-when-manager-idle`
17. `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-count-fast-path`
18. `git diff --check`
19. `./bin/governance-check`
20. Protected-root replay:
   - `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - wait about 70 seconds
   - `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Results

1. All focused regressions above passed in both `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-live-status-hang-root-cause` and the temporary premerge lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-test-pre-merge-live-status-hang-root-cause`.
2. `test-monitor-ai-cli-pid` now proves launch-state writeback records `LAST_AI_STATE="up"` and `LAST_EXIT_REASON="ai_launch_in_flight"` as soon as the child pid is known, before any tool-specific exit timing can race status readers.
3. `test-freely-live-status-startup-self-heals-stale-launch-in-flight-state` proves stale `ai_launch_in_flight` state is self-healed only after the grace window, which keeps the logic tool-agnostic instead of pinning behavior to `codex`.
4. `test-freely-prompt-build-failure-keeps-supervisor-alive` proves `build_prompt` failure no longer kills the supervisor under `set -e`; the runtime records `prompt_build_failed`, keeps the supervisor alive, and `live-status` surfaces retryable truth instead of `startup_self_heal_no_runtime`.
5. `test-freely-daemon-start-detach-contract` keeps the launcher requirement explicit: `daemon start` must spawn `daemon-run` in a new session rather than fall back to shell-owned `nohup ... &`, because short-lived non-interactive callers can otherwise tear the control plane down after startup returns.
6. `test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path` proves `live-status` no longer self-heals a live daemon runtime down when the recorded project root and the inspected project root differ only by path spelling that still resolves to the same on-disk directory.
7. `test-freely-live-status` still passes after the path-equivalence hardening, so the runtime surface and prompt/deep-ref output remain intact.
8. `test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite` still passes in the fresh `2026-04-20` session, so status refresh keeps persisting corrected continuity and prompt anchors even when worker-slot counts do not change.
9. `test-freely-stale-manager-continuity-filter` still passes in the same session, so stale continuity that points at missing worktrees keeps getting filtered instead of being revived into status truth.
10. Canonical protected-root replay on `2026-04-22` showed a newer still-open defect in old `develop`: startup reached `L041 ai_launch_observed`, but watchdog still fired `L223 manager_idle_supervisor_restart trigger=supervisor_alive_ai_missing_after_grace` about 12-19 seconds later because `project_bootstrap_launch_in_flight()` accepted `starting` but not `ai_launch_in_flight`.
11. The focused regression `test-freely-manager-bootstrap-keeps-supervisor-after-ai-launch-observed` now proves the repaired bootstrap gate keeps the supervisor in-flight after both `LAST_EXIT_REASON="ai_launch_in_flight"` and lifecycle `L041 ai_launch_observed`.
12. `test-freely-ai-pid-validation-supported-tools` proves pid ownership now follows the configured supported tool family, including the lawful `claude` launcher behind `cc`, without widening acceptance to foreign same-tool processes.
13. `test-freely-proxy-self-heal` proves bounded network self-heal tries project-scoped proxy modes with a live `hi` probe, respects `AUTO_SETUP_FREELY_PROXY`, and does not silently switch tool or slot when those auto-switch controls are disabled.
14. `test-freely-live-status-active-manager-skips-fleet-refresh`, `test-freely-live-status-uses-status-signals-when-manager-idle`, and `test-freely-live-status-worker-count-fast-path` prove the status surface now uses lightweight reads in manager-active and idle states instead of perturbing the same startup window with heavy refresh work.
15. The first guarded `test-pre-merge-20260422-live-status-hang-root-cause -> develop` replay was blocked only by missing owner lifecycle artifacts in the merge diff; code integration and premerge regression replay both succeeded.

## Verdict

`AT-001` and `AT-002` remain satisfied. `AT-003` is in final guarded-replay closeout: feature and premerge evidence are green, and the remaining proof point is to replay canonical `develop` after this owner evidence lands in the merge diff. The current continuation stays within the same bounded owner: startup now canonicalizes stale machine-owned truth, records launch-in-flight truth before AI exit can race readers, keeps `ai_launch_in_flight` inside the lawful bootstrap grace window, validates AI pids against configured supported tools, preserves a live daemon when project-root spelling differs but the directory identity is the same, and uses proxy/status self-heal without silently re-enabling disabled tool or slot auto-switch.

## Implementation Decision Note

- decision: `Keep startup self-heal scoped to machine-provable stale state, but align bootstrap grace, supported-tool pid truth, proxy self-heal, and manager-active status reads with the runtime-owned signals already published on disk.`
- why_this: `The 2026-04-22 canonical replay showed the user-visible failure still occurred before manager-owned semantic recovery started: the system had already observed AI launch, but startup grace ignored the newer on-disk exit reason and tore the supervisor down anyway. The narrowest correct fix is to harden runtime-owned truth and its lightweight readers rather than special-case one tool family or re-enable global tool/slot switching.`
- alternatives_considered: `Special-case codex; keep hard-coded argv fragments for pid matching; let network failure silently fall back by auto-switching tool/slot; keep heavy live-status refresh while the manager is active; widen this owner into a generic runtime lifecycle redesign.`
- boundary_non_goals: `This note still does not let startup repair semantic continuation, does not lock behavior to codex, does not silently override AUTO_SWITCH_TOOL/AUTO_SWITCH_SLOT, and does not redesign generic post-failure recovery or manager routing.`
- residual_risk: `The final canonical replay still has to prove the repaired bootstrap grace removed the old L041->L223 churn on develop. If that replay still fails, the next likely seam is later ai.pid clearing or pid ownership readback after launch observation, not the governance/doc chain or tool/slot switching policy.`

## Remaining Closeout

1. Replay the guarded `test-pre-merge-20260422-live-status-hang-root-cause -> develop` merge now that the owner lifecycle artifacts are in the diff.
2. Restart canonical root `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` and verify the old `L041 ai_launch_observed -> L223 supervisor_alive_ai_missing_after_grace` sequence no longer appears.
3. Push `develop`, retire the dedicated premerge lane, and retire `feature/live-status-hang-root-cause-20260422` after canonical replay is green.
