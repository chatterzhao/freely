# Progress: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/manager-exit-contract-expected-worker-guard-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-manager-exit-contract-expected-worker-guard`
- updated_at: `2026-04-21 23:12 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Real self-host observation showed Freely could patrol once but fail to sustain autonomous looping because daemon-mode `TERM` could become a false `operator_stop`.
- A second restart blocker also existed: a lone same-project dispatcher/watchdog residue could cause `start` or `daemon start` to refuse even though no authoritative supervisor was alive.
- The runtime fix and focused regressions are complete in the blocker worktree.
- Canonical `develop` then exposed one more followthrough seam: runtime was reading the new `## Worker Delegation` continuity shape as if no worker prompts existed, so freshly generated worker lanes could not launch even though manager continuity had already selected them.
- The continuity parser and worker-launch consumption path are now updated to read that current handoff shape.
- Guarded replay then exposed one more same-owner retirement seam: an already merged-clean blocker worktree could still be treated as a recoverable active worker. Runtime now settles those lanes toward cleanup followthrough, and cleanup can reclaim stale recorded ownership for retire-ready merged worktrees.
- Canonical `develop` then exposed a narrower replay seam after guarded absorption: if the merged blocker lane only stayed dirty in owner progress / verification evidence, runtime still treated it as a relaunchable edit worker because the old guard only recognized fully clean merged worktrees. This followthrough now treats owner-evidence-only dirty merged lanes as retirement/promotion followthrough instead of active edit capacity.
- Canonical `develop` then exposed one more fallback seam in the manager launcher: when no launchable continuity remained, runtime could fall back to the latest generated continuity and relaunch a worker prompt without rechecking whether that prompt now targeted a retire-ready merged lane.
- This followthrough now makes the fallback launcher respect the same `worker_prompt_launchable_for_manager_project()` gate and settle retire-ready merged targets instead of reviving them.
- Canonical self-host replay then showed one more recovery-memory seam: once the stale merged blocker lane had been wrongly revived and left ordinary dirty files behind, manager expected-running recovery and restart-memory selection could still treat that absorbed branch as restore-ready because the older guard only recognized clean or owner-evidence-only merged followthrough.
- This followthrough now blocks automatic relaunch for any worker lane whose branch is already merged into `develop`; if new post-merge work is ever needed, it must materialize as a fresh lane rather than resurrecting the absorbed worktree.
- The protected test lane replay now passes again; the remaining completion work is develop absorption, real self-host task completion, and temporary lane retirement.
- A fresh-session verification at `2026-04-21 05:36 PDT` disproved the previous "already green" claim: `test-freely-daemon-start-reuses-live-supervisor-without-relaunch` failed before reuse because its `ps`-count assertion could observe a transient duplicate `daemon-run` snapshot.
- A narrow same-lane fix then hardened that regression to wait for a stable single `daemon-run` process snapshot before asserting reuse, instead of treating a startup race between separate `ps` calls as a product failure.
- As of `2026-04-21 05:42 PDT`, the refreshed feature worktree verification passes every required feature-local regression and gate again with that repair in place.
- A second fresh-session recheck at `2026-04-21 05:47 PDT` passed the same full feature-local verification chain without any additional source edits, so the lane remains green on current-session truth.
- A third same-session verification at `2026-04-21 05:54 PDT` reran the owner-required feature-local regression and gate set from this worker continuation; every command still passed, and no additional implementation edits were needed beyond the already-present regression hardening in this worktree.
- A fourth worker-continuation verification at `2026-04-21 06:12 PDT` reran the full owner-required feature-local chain, including the daemon lifecycle regressions, continuity/retirement regressions, `./bin/pretests-gate`, and `./bin/governance-check`; every command passed again with no further source edits.
- Canonical `develop` self-host replay then exposed a remaining continuity-consumption seam: manager wrote the current direct `## Worker Delegation` handoff with a bare `prompt_path`, but runtime only parsed `prompt_path` after an explicit `launchable_queue`/`queue` subsection, so post-cycle worker launch treated the continuity as prompt-empty and restarted manager instead.
- The runtime parser now treats direct `## Worker Delegation` `prompt_path` entries as launchable by default, matching the manager-written continuity shape that self-host dogfooding is actually producing.
- The current-format continuity-consumption and manager worker-launch regressions now exercise that direct handoff shape, and a post-AI-cycle launch regression passes against the same parser path.
- Canonical `develop` self-host replay then exposed one more stale-target seam outside the worker-launch bootstrap path: `sync_project_tooling_from_source()` could still rewrite `.freely/config.env` and `.githooks` into a directory under the managed `*-worktrees` root even after that path dropped out of the authoritative `git worktree list --porcelain` fleet.
- `sync-tooling` now no-ops for those under-root non-authoritative targets before copying config or rewriting hooks, while still allowing valid managed worktree sync and fresh-project bootstrap outside the worktree root.
- Canonical `develop` self-host replay then exposed a continuation-handoff seam: after context compaction, manager could relaunch on `fresh_with_handoff`, lose the current continuity anchor, and spend the next round rewriting manager continuity instead of executing the already-selected maintenance / retirement followthrough.
- The continuity resume-focus helper now recognizes the current `## Primary Judgement`, `## Queue`, and `## Next Supervision Priority` headings and applies the same anchor across both `resume` and `fresh_with_handoff`, with an explicit success return so prompt building cannot fail when an optional section is absent.
- The same repair worktree also exposed an absorbed-lane overreach: a never-started worker branch cut from `develop` could be treated as already absorbed solely because its branch was still an ancestor of `develop`.
- Runtime now only classifies a merged worker lane as absorbed after that worktree has recorded worker state, while cleanup followthrough prompts with complete verification metadata remain launchable until the lane is actually retire-ready.
- Focused regressions now cover current-format continuity anchoring, active-worker state projection, stale discovery cache refresh before launch, retire-ready merged prompt suppression, and absorbed-merged dirty-worker recovery suppression in addition to the earlier direct worker-delegation launch checks.
- Canonical `develop` daemon replay then exposed one more same-owner state-refresh seam: after manager wrote a new manager-owned continuity with no worker prompt, `manager_worker_launch_state.env` could keep advertising an older queued worker prompt and an older consumed continuity as the current truth.
- Canonical `develop` replay now exposes a narrower autonomy-stop seam: even after worker recovery logic exists, manager can still legally terminate with `EXIT_KIND=stop_ai` while authoritative supervision truth shows a runtime-owned expected-running worker remains down/degraded.
- This followthrough now counts unresolved expected-running workers directly from manager supervision truth, surfaces that count in the manager exit-contract directive, and refuses `stop_ai` by forcing a same-session repair handoff until recovery/cleanup resolves the worker.
- A focused regression proves runtime now blocks premature manager stop when a worker remains unresolved, and the guarded test-pre-merge lane passed that new regression plus `./bin/governance-check`.
- The result was another `fresh_with_handoff` patrol that saw the latest continuity excerpt but still carried stale queued prompt state, so manager stayed in verification judgment without ever advancing the cleanup-only task it had already selected.
- Runtime now treats manager-authored no-worker continuity as authoritative enough to supersede stale queued worker-prompt state, while still preserving older unconsumed prompts across newer runtime-seeded startup stubs and runtime fallback continuity.
- Canonical `develop` daemon replay then exposed one more tool-availability seam: after `cc` ended `tool_runtime_failure`, cross-tool recovery could still select `kiro-cli` even though the immediately preceding self-host evidence had already proven this machine was at Kiro monthly request limit.
- Runtime now persists `kiro_monthly_request_limit` as a tool-availability state with a recovery hint and skips that cached-unavailable Kiro candidate during later auto-switch / manager bootstrap selection, instead of re-burning the same exhausted tool before moving on.
- Canonical `develop` self-host replay then exposed one more same-owner followthrough seam: guarded merge push followthrough had already succeeded, but local `origin/develop` tracking truth still lagged behind `HEAD`, so manager/live-status kept surfacing `develop_push_followthrough_state=push_pending` and continued to treat protected push followthrough as an unresolved gating fact.
- Runtime now refreshes the local upstream tracking ref to the pushed `HEAD` immediately after a successful `develop-push attempt`, so later manager patrols do not stall on a false `ahead>0` reading after guarded delivery has already completed.
- Canonical `develop` self-host replay then exposed one more hygiene seam: after push truth cleared, manager still looped on untracked `docs/system/workspace/scripts/runtime/__pycache__/` residue in canonical `develop` and the disposable absorbed-merged premerge lane instead of advancing the selected cleanup / replay followthrough.
- Runtime and the lead-agent startup snapshot now auto-clean untracked disposable Python cache residue (`__pycache__` / `.pyc`) before dirty-state hygiene judgement, so manager no longer treats runtime-only cache artifacts as durable lane dirt.
- Canonical `develop` self-host replay then exposed one more launcher seam: once hygiene cleared, manager finally resumed the same Codex session, but the runtime still passed `--add-dir` through `codex exec resume`, which the current Codex CLI rejects with `unexpected argument '--add-dir'`, causing repeated `ai_exit_rc_2` instead of continuity followthrough.
- Runtime now keeps `--add-dir` on fresh Codex launches but omits it from `codex exec resume`, matching the current CLI contract while preserving project-root cwd scoping.
- Canonical self-host replay then exposed one more worker-bootstrap seam: a stale worker target could still enter missing-config bootstrap, call `freely init` without inherited default-autonomy consent, ignore that init failure, and continue mutating `config.env` for a path that no longer belonged to the authoritative fleet.
- Runtime now refuses to bootstrap worker targets outside the authoritative `git worktree list --porcelain` fleet, requires missing-config worker init to succeed before any post-init config writes continue, and carries `--accept-default-autonomy` during that bounded runtime-owned bootstrap path.
- The same autonomous-loop owner then exposed one more supervisor seam in the bounded repair space: manager and worker rounds could end without a machine-checkable exit artifact, so runtime had no precise contract for `stop_ai`, `resume_manager`, `delegate_workers`, `worker_done`, `worker_blocked`, or `worker_handoff_needed`, and could not force the same session to repair missing closeout state before broader patrol resumed.
- Runtime now injects explicit manager/worker exit-contract directives into prompts, clears stale role-specific contract files before each new AI cycle, validates the resulting artifact after `ai_exit_rc_0`, and reuses the exact `LAST_TOOL_RESUME_TARGET` to repair missing or malformed contracts before any broader followthrough continues.
- The remaining completion work is guarded promotion into `develop`, canonical `develop` self-host task completion, and temporary lane retirement.

## 2026-04-21 20:55 PDT Exit Contract Enforcement Followthrough

- `FAIL`: the bounded self-loop owner still had one non-machine-checkable seam: manager/worker rounds could terminate without a structured exit artifact, so runtime could not distinguish lawful stop, precise manager resume, worker delegation, worker completion, worker block, or worker handoff without guessing from free text.
- `PASS`: manager prompt build now injects a hard exit-contract directive with one exclusive `EXIT_KIND` from `stop_ai`, `resume_manager`, or `delegate_workers`, and worker prompt build does the same for `worker_done`, `worker_blocked`, or `worker_handoff_needed`.
- `PASS`: runtime now clears stale role-specific contract files before launch, routes post-cycle handling through one unified exit-contract dispatcher, and writes a repair handoff that reuses the exact current resume target when the contract is missing or malformed.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-stop-ai`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-retire-ready-merged-cleanup-handoff-not-reclaimed`
- `PASS`: authoritative cleanup-handoff prompt resolution now falls back from a missing local worker prompt to `worker-verification-contract.env` `SOURCE_PROMPT_FILE`, matching the real runtime shape that canonical `develop` produced.
- `PASS`: when both a worker-local reentry prompt and a verification contract `SOURCE_PROMPT_FILE` exist, merged-lane settle/reclaim now prefers the contract-backed cleanup handoff prompt, preventing the worker bootstrap prompt from masking the real cleanup scope.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `PENDING`: carry this same-owner followthrough through guarded promotion into canonical `develop`, then rerun real daemon self-host acceptance until Freely finishes one real task, lawfully closes the temporary worktree, and advances to another task.

## 2026-04-21 18:15 PDT Worker Bootstrap Guard Followthrough

- `FAIL`: canonical self-host replay exposed a bounded launcher seam after the Codex resume repair: a stale worker target could still enter missing-config bootstrap, call `freely init` without inherited default-autonomy consent, ignore that failing init result, and continue mutating `config.env` for a path that no longer belonged to the authoritative fleet.
- `PASS`: runtime now hard-gates worker bootstrap on authoritative worktree membership, requires `freely init` success before post-init config writes proceed, and carries `--accept-default-autonomy` through this runtime-owned missing-config bootstrap path.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-inherits-tool-adapter`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `PENDING`: absorb this same-owner followthrough into canonical `develop`, then rerun daemon self-host acceptance until Freely completes one real task, lawfully retires the temporary lane, and advances to another task.

## 2026-04-21 08:45 PDT Kiro Availability Memory Verification

- `FAIL`: canonical `develop` self-host replay advanced past the stale manager continuity blocker, but a later `cc` `tool_runtime_failure` still cross-switched into `kiro-cli` even though the same replay had already established `kiro_monthly_request_limit`; runtime had classification for the Kiro failure, but no persisted availability memory for later candidate selection.
- `PASS`: runtime now writes `tool-availability-kiro-cli.env` when Kiro monthly-limit truth is observed, derives a recovery hint from the reset line when present and otherwise falls back to the next calendar-month boundary, and skips that cached-unavailable Kiro candidate during later cross-tool recovery.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-skips-known-unavailable-kiro`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `PENDING`: absorb this same-owner followthrough into canonical `develop`, then rerun `./bin/freely daemon start` until a real task completes, the corresponding worktree is lawfully closed, and the daemon proceeds to another task.

## 2026-04-21 09:25 PDT Develop Push Followthrough Tracking Refresh Verification

- `FAIL`: canonical `develop` self-host replay showed `merge-guarded` had already pushed successfully, but local branch truth still reported `develop...origin/develop [ahead 73]`; manager therefore kept surfacing `develop_push_followthrough_state=push_pending` and never cleared that gating fact before cleanup sequencing.
- `PASS`: `develop-push attempt` now rewrites the local upstream tracking ref to the pushed `HEAD` immediately after a successful push, so later `develop_push_followthrough_snapshot_for_project()` reads `clean` instead of replaying stale ahead-count truth.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `PENDING`: absorb this repair into canonical `develop`, then rerun daemon self-host acceptance to verify manager advances past false push followthrough and actually completes cleanup/task closeout.

## 2026-04-21 16:45 PDT Disposable Pycache Hygiene Verification

- `FAIL`: canonical `develop` self-host replay no longer stalled on false push followthrough, but manager still looped across `fresh` and repeated `fresh_with_handoff` rounds because canonical `develop` plus `test-pre-merge-20260421-absorbed-merged-scan-routing-fix` only looked dirty from untracked `docs/system/workspace/scripts/runtime/__pycache__/` residue.
- `PASS`: runtime now auto-cleans untracked disposable Python cache residue before dirty-state hygiene judgement, and the lead-agent startup snapshot uses the same narrow rule so manager prompts stop freezing on runtime-only cache artifacts.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-develop-push-pending`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-develop-push-attempt`
- `PENDING`: absorb this repair into canonical `develop`, then rerun daemon self-host acceptance until one real task completes, the relevant worktree closes, and the daemon advances to another task.

## 2026-04-21 17:55 PDT Codex Resume Add-Dir Followthrough

- `FAIL`: after hygiene cleared, canonical `develop` replay finally reached manager continuity resume, but `tool_run_direct_from_prompt_file()` still passed `--add-dir` through `codex exec resume`; current Codex CLI rejects that form and the daemon looped on `ai_exit_rc_2` instead of resuming followthrough.
- `PASS`: fresh Codex launches still pass `--add-dir`, but resume launches now omit it so `codex exec resume --skip-git-repo-check <session>` matches the actual CLI contract.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
- `PENDING`: absorb this launcher repair into canonical `develop`, then rerun daemon self-host acceptance and verify resume no longer collapses into `ai_exit_rc_2`.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`
14. `bash docs/system/workspace/scripts/tests/test-freely-merged-clean-worker-handoff-guard`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
16. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
17. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
18. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
19. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
20. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
21. `./bin/governance-check`
22. `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
23. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
24. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-absorbed-merged-dirty-worker`
14. `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
15. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
16. `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
17. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
18. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
19. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`

## 2026-04-21 05:29 PDT Recheck Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed in the feature worktree on this recheck.

## 2026-04-21 05:33 PDT Fresh-Session Recheck Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed again in the feature worktree during this fresh session.

## 2026-04-21 Sync-Tooling Stale-Target Followthrough

1. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-stale-target-worktree-blocked`
2. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
3. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`

All three commands passed in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-sync-tooling-authoritative-target-guard`.

## 2026-04-21 05:36 PDT Failure Reproduction

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`

Observed result:

- `FAIL`: `expected exactly one daemon-run process before reuse, found 2`
- Interpretation: the lane was not honestly promotion-ready at the start of this session because the fresh-session reuse regression still had a startup-window race.

## 2026-04-21 05:42 PDT Narrow Fix And Recheck Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
4. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
5. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
6. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
7. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
8. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
9. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
10. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
11. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
12. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
13. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
14. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
15. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
16. `./bin/governance-check`

All commands above passed after the narrow test hardening.

## 2026-04-21 05:47 PDT Fresh-Session Verification Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed again in the feature worktree during this fresh-session verification.

## 2026-04-21 05:54 PDT Worker Continuation Verification Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed in the feature worktree during this worker continuation verification. No new source edits were required after these reruns.

## 2026-04-21 06:12 PDT Worker Continuation Verification Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
6. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
7. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
8. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
11. `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
12. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
13. `./bin/governance-check`

All commands passed again in the feature worktree during this worker continuation verification. No further source edits were required.

## 2026-04-21 07:47 PDT Continuity Handoff / Launch-Gating Verification

- `FAIL`: canonical `develop` self-host replay still looped after worker launch recovery because manager resumed from a compacted handoff, rewrote manager continuity again, and never actually executed the current continuity's queued followthrough.
- `FAIL`: the same repair worktree then showed `worker_prompt_launchable_for_manager_project()` still over-classified never-started worker branches as absorbed merged lanes, which broke active-worker reentry and stale-cache launch flows even though those branches had not been retired.
- `PASS`: anchored current-format manager continuity across both `resume` and `fresh_with_handoff`, including the new section headings and a deterministic helper return path.
- `PASS`: narrowed absorbed-merged classification to require recorded worker state, and kept cleanup followthrough prompts launchable until the target lane is truly retire-ready.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-projection-without-state`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-refreshes-stale-discovery-cache`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-retire-ready-merged-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-absorbed-merged-dirty-worker`
- `PASS`: replayed `feature/manager-followthrough-handoff-resume-20260421 -> test-pre-merge-20260421-manager-followthrough-handoff-resume` through `./bin/merge-guarded`; the protected test lane stayed green on the representative same-owner regressions.
- `PENDING`: absorb this repair into canonical `develop`, then complete the required self-host daemon acceptance and temporary lane retirement.

## 2026-04-21 08:31 PDT Manager Launch-State Supersession Verification

- `FAIL`: canonical `develop` daemon replay still stalled after that repair because a new manager-authored continuity with no worker prompt did not overwrite `LAST_MANAGER_CONTINUITY_CONSUMED` or `QUEUED_WORKER_PROMPTS`; the next `fresh_with_handoff` round therefore kept seeing stale queued worker-prompt truth from `064955` even though the current continuity had already moved to manager-owned cleanup.
- `PASS`: narrowed `manager_worker_launch_state_refresh_for_status()` so only `freely-runtime-startup-stub` and `freely-runtime-fallback` continuity may preserve an older unconsumed worker prompt; a newer manager-authored no-worker continuity now supersedes stale queued prompt state and clears the stale queue.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-preserves-unconsumed-prompt-across-startup-stub`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `PENDING`: guarded replay into `develop`, then canonical `develop` self-host acceptance must prove Freely can finish one task and continue instead of cycling through manager-owned continuity rewrites.

## Current Lane Judgement

 - lane_state: `feature-local green after a narrow regression hardening fix`
- blocker_reproduction: `no`
- guarded_promotion_ready: `yes`
- remaining_blocker: `canonical develop replay is still required before retirement`

## Next Action

1. Replay `feature/manager-exit-contract-expected-worker-guard-20260421 -> test-pre-merge-20260421-manager-exit-contract-expected-worker-guard -> develop` through `./bin/merge-guarded` with this refreshed owner evidence included.
2. On canonical `develop`, run `./bin/freely daemon start` until one task completes to the current-project success standard, its temporary worktree closes lawfully, and the daemon proceeds to the next task.
3. Retire the temporary feature/test-pre-merge lanes for this stop-guard followthrough after canonical replay succeeds.

## 2026-04-21 23:10 PDT Ordinary Manager Stall Recovery Followthrough

- `FAIL`: canonical `develop` self-host replay advanced past the retired absorbed-cleanup lane, but a fresh manager `codex` round with no delegated continuation, no new intake, and no new runtime artifacts could still sit on one ordinary prompt indefinitely; existing stall recovery only covered pending-intake and delegated-continuation shapes, so autonomy could stop making progress without triggering a repair handoff.
- `PASS`: runtime now treats a manager round with an ordinary prompt, no pending intake, no delegated continuation, and no runtime log progress beyond the stall threshold as recoverable stalled manager work, and forces the same local continuation reentry path already used by the narrower stall classes.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery-without-runtime-progress`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
- `PENDING`: replay this followthrough through guarded promotion, then rerun canonical `develop` daemon self-host acceptance until Freely completes one task, retires the corresponding temporary lane lawfully, and advances to another task.
