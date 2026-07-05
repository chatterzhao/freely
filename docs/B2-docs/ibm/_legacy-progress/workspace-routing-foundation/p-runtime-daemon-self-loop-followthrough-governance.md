# Progress: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `done`
- runtime_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-resume-incremental-output-evidence-guard-20260425`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-feature-runtime-resume-incremental-output-evidence-guard`
- updated_at: `2026-04-25 20:25 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Real self-host observation showed Freely could patrol once but fail to sustain autonomous looping because daemon-mode `TERM` could become a false `operator_stop`.
- A second restart blocker also existed: a lone same-project dispatcher/watchdog residue could cause `start` or `daemon start` to refuse even though no authoritative supervisor was alive.
- The runtime fix and focused regressions are complete in the blocker worktree.
- Canonical `develop` then exposed one more followthrough seam: runtime was reading the new `## Worker Delegation` continuity shape as if no worker prompts existed, so freshly generated worker lanes could not launch even though manager continuity had already selected them.
- The continuity parser and worker-launch consumption path are now updated to read that current handoff shape.
- Canonical restart observation then exposed one more freshness seam: `daemon stop` recorded `LAST_EXIT_REASON=operator_daemon_stop`, but the startup patrol staleness boundary only refreshed on plain `operator_stop`, so the next fresh patrol could still anchor itself to a pre-stop cleanup continuity instead of the new scan JSON.
- Explicit daemon stop now refreshes the same manager operator-stop boundary used by patrol freshness filtering, so startup patrol can discard pre-stop continuity history and let scan-selected work win the next round.
- Guarded replay then exposed one more same-owner retirement seam: an already merged-clean blocker worktree could still be treated as a recoverable active worker. Runtime now settles those lanes toward cleanup followthrough, and cleanup can reclaim stale recorded ownership for retire-ready merged worktrees.
- Canonical `develop` then exposed a narrower replay seam after guarded absorption: if the merged blocker lane only stayed dirty in owner progress / verification evidence, runtime still treated it as a relaunchable edit worker because the old guard only recognized fully clean merged worktrees. This followthrough now treats owner-evidence-only dirty merged lanes as retirement/promotion followthrough instead of active edit capacity.
- Canonical `develop` then exposed one more fallback seam in the manager launcher: when no launchable continuity remained, runtime could fall back to the latest generated continuity and relaunch a worker prompt without rechecking whether that prompt now targeted a retire-ready merged lane.
- This followthrough now makes the fallback launcher respect the same `worker_prompt_launchable_for_manager_project()` gate and settle retire-ready merged targets instead of reviving them.
- Canonical self-host replay then showed one more recovery-memory seam: once the stale merged blocker lane had been wrongly revived and left ordinary dirty files behind, manager expected-running recovery and restart-memory selection could still treat that absorbed branch as restore-ready because the older guard only recognized clean or owner-evidence-only merged followthrough.
- This followthrough now blocks automatic relaunch for any worker lane whose branch is already merged into `develop`; if new post-merge work is ever needed, it must materialize as a fresh lane rather than resurrecting the absorbed worktree.
- Canonical `develop` replay then exposed one narrower manager-repair seam after the watchdog keepalive fixes landed: `fresh_with_handoff` recovery with `rotation_reason=missing_resume_evidence` could still rebuild the full broad lead-agent startup prompt, so manager spent the next round rereading patrol context and still exited `rc=0` without writing either a fresh manager continuity or `manager-exit-contract.env`.
- The runtime prompt builder now narrows exactly that repair surface. When the role is manager, the handoff says `manager_exit_contract_repair`, and launch selection has already downgraded to `fresh_with_handoff` because resume evidence is missing, Freely emits a bounded repair prompt that requires continuity first and exit contract second instead of re-entering broad startup patrol.
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
- Canonical `develop` replay then exposed one more monitor/runtime seam: Codex could print `failed to refresh available models: timeout waiting for child process to exit` during an otherwise successful manager round, and `monitor-ai-cli.sh` misclassified that single line as `tool_runtime_failure`.
- The monitor now strips that known benign Codex startup noise before runtime-failure classification, so a normal manager patrol no longer falls into same-tool / cross-tool recovery just because model refresh lagged during startup.
- Canonical `develop` replay after that repair exposed a narrower bootstrap seam: `ensure-manager` could still restart a fresh daemon-owned manager as idle before `ai_launch_begin` if worker recovery or fleet prep kept startup between `L010 supervisor_started` and `L020 prompt_build_begin` longer than the initial 15-second bootstrap grace.
- Runtime startup-lifecycle protection now treats `L010 supervisor_started` as in-flight startup evidence, so daemon-owned manager bootstrap can finish pre-prompt recovery work without being killed and relaunched by its own keepalive loop.
- Focused verification passed for the new benign-noise regression while the adjacent real-failure regressions for Codex 429 and reconnect defer stayed green.
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
- Canonical `develop` self-host replay then exposed one more runtime/tool-boundary seam: `monitor-ai-cli` treated Codex `ERROR: Reconnecting... x/5` as immediate network-failure evidence, so the current tool could be killed and cross-tool fallback could start before Codex exhausted its own retry loop.
- The monitor now leaves reconnect-in-progress output alone and lets the tool exit naturally; post-exit runtime classification still maps pure reconnect evidence to the bounded `execution_network_transient` / `execution_network_persistent` path, while hard failures like Codex 429 remain immediate monitor-level kill signals.
- The same replay family also exposed one more recovery-memory seam: after exhausting `cc`, `iflow`, and `kiro-cli` inside one bounded fallback episode, project tool selection could remain pinned to the last failed fallback instead of returning to the original tool for the next retry.
- Runtime auto-recovery now remembers the origin tool for the current episode, preserves attempted-tool memory across the episode, and restores the original tool once every configured fallback has failed.
- Canonical `develop` replay for the current Codex-first operating mode then exposed a narrower observability seam: when runtime classified a failure as reconnect/network, proxy-config, auth, or Kiro subscription, the logs still lacked enough operator guidance to tell whether the real blocker was relay reachability, proxy mode, or provider access/quota.
- Runtime now emits targeted guidance for those classified failure families, includes a proxy-mode summary with the authoritative project/global config paths, and documents `inherit` / `disabled` / `explicit` proxy modes directly in the runtime config template without changing the default mode.
- Canonical `develop` replay still exposed one narrower reconnect-exhaustion seam after that guidance landed: when Codex exhausted its own reconnect loop and ended with upstream `502 Bad Gateway`, monitor/runtime still persisted `tool_runtime_failure`, which incorrectly widened recovery into generic tool/slot fallback.
- Runtime now passes a dedicated network marker from `monitor-ai-cli` into the supervisor loop, writes that marker only for real network evidence, and reclassifies reconnect-exhaustion `502` exits back onto the bounded `execution_network_transient` / `execution_network_persistent` path while keeping Codex 429 on the immediate tool-failure path.
- Canonical `develop` replay for the retained dirty blocker lane then exposed one narrower launchability family inside the same owner: daemon patrol could still emit `printf: write error: Broken pipe` while computing worktree summary, and manager launch / exit-contract validation still required the target worktree to pre-exist even when continuity had already selected a governed sibling lane that should be materialized on demand.
- The same replay family also showed a retirement overreach: once a branch tip was merged, runtime could still misclassify a merged-tip lane as retire-ready cleanup even though the latest authoritative continuity still carried an active `edit` prompt for that lane, which would erase real ownership instead of letting the selected task continue.
- This followthrough now makes `worktree_summary_for_project()` consume `git worktree list --porcelain` without the pipe-fragile `awk` stage, tolerates downstream closed-pipe consumers, allows prompt-governed missing sibling worktrees to be materialized before manager launch, and blocks both absorbed/retire-ready merged classification whenever authoritative continuity still grants active `edit` or `promotion` ownership to that lane.
- Canonical replay after the manager/source-runtime rebind then exposed one more same-owner closeout seam: cached worktree and continuity discovery helpers still emitted multi-line output through bare `printf`, so lawful early-return consumers could raise `Broken pipe` under `set -euo pipefail` and strand manager/worker supervision after AI exit before `ai_cycle_finished` closeout truth was fully consumed.
- Cached `git worktree list --porcelain` and manager continuity producers now emit through a bounded helper that traps `PIPE`, ignores `SIGPIPE`, and returns success when the downstream consumer has already found the first needed record.
- The remaining completion work is guarded promotion into `develop`, canonical `develop` self-host task completion, and temporary lane retirement.

## 2026-04-24 17:05 PDT Existing Stale Worker Bootstrap Followthrough

- `FAIL`: canonical `develop` daemon replay moved past the missing-worktree materialization seam, but the next selected cleanup lane could still point at a sibling worktree directory that already existed with copied `.freely/config.env` while lacking `.freely/run` baseline state and rematerialized tooling; runtime treated that half-bootstrap directory as an already-ready worker and never repaired it into a launchable workcell.
- `PASS`: manager launch now repairs such existing authoritative worker worktrees before delegation by re-running managed tooling sync when bootstrap surfaces are missing, and runtime writes baseline workcell state on config-present lanes that still lack `.freely/run/workcell-state.env`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-repairs-existing-stale-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `PASS`: protected premerge replay on `test-pre-merge-20260424-worker-launch-bootstrap-repair` reran the same stale-existing-worktree bootstrap regression plus the adjacent missing-worktree materialization and sync-tooling regressions without widening owner scope.
- `PENDING`: guarded `develop` merge and fresh canonical daemon replay still must prove the retained receipt-closeout lane both launches from an existing stale worktree and advances the self-host loop to the next scan-selected task instead of stopping after manager selection.

## 2026-04-22 07:09 PDT Reconnect Exhaustion 502 Network Marker Followthrough

- `FAIL`: direct `codex exec` was healthy again, but the same invocation through `monitor-ai-cli.sh` still reproduced `ERROR: Reconnecting... 1/5 ... 5/5` followed by upstream `502 Bad Gateway`; runtime persisted that exit as `tool_runtime_failure`, which reopened generic cross-tool fallback instead of staying on the bounded execution-network path.
- `PASS`: `monitor-ai-cli.sh` now writes `network_failure` only for real network evidence, `runtime/freely` passes and consumes a dedicated network marker, and exhausted Codex reconnect `502` exits now fall back through runtime network classification rather than generic tool failure.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-reconnect-exhaustion-as-network-failure`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-defers-codex-reconnect-until-retries-exhaust`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-429-rate-limit`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `PENDING`: absorb this same-owner repair into canonical `develop`, rerun daemon self-host supervision, and verify Freely can advance past reconnect-exhaustion truth into real task completion instead of widening into cross-tool fallback.

## 2026-04-23 23:25 PDT Worker Materialization And Pipe-Safe Summary Followthrough

- `FAIL`: canonical `develop` fleet replay narrowed to one retained dirty blocker lane, but daemon/log consumers could still hit `printf: write error: Broken pipe` inside `worktree_summary_for_project()`, which is enough to degrade patrol/live-status even though the task source was already present.
- `FAIL`: the same replay family then showed manager could choose a worker prompt from continuity/scan and still reject it as non-launchable when its governed sibling worktree did not already exist, even though the prompt already contained lawful `Worktree:` and `Branch:` metadata under the canonical `*-worktrees` root.
- `FAIL`: once such a lane existed and its branch tip was merged, runtime could still misclassify it as retire-ready cleanup despite the latest authoritative continuity still carrying an active `edit` prompt for that same lane, which would throw away real selected-task ownership instead of letting the worker continue.
- `PASS`: `worktree_summary_for_project()` now iterates the porcelain output directly and writes its summary through a pipe-tolerant block, removing the broken-pipe seam without changing worktree counting semantics.
- `PASS`: manager exit-contract validation and worker launch now treat governed missing sibling worktrees as materializable runtime truth, materialize them before launch, and refresh discovery so scan-selected worker prompts can actually become live workers instead of stalling in launchability repair.
- `PASS`: merged-tip absorbed/retire-ready classification now checks the latest authoritative continuity for active non-cleanup prompt ownership, so an `edit`/`promotion` lane is not reclaimed into cleanup just because its branch is already merged.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-multi-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-allows-materializable-missing-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-keeps-fresh-materialized-worker-with-authoritative-edit-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `PENDING`: replay this same-owner repair through fresh protected premerge and guarded `develop`, then rerun canonical `freely daemon start` until Freely both closes the retained cleanup lane and advances to the next scan-selected task.

## 2026-04-22 06:05 PDT Proxy Guidance Followthrough

- `FAIL`: canonical `develop` replay under the current Codex-first setup still left network-facing failures too opaque; once runtime classified reconnect/network, proxy-config, auth, or Kiro subscription errors, the operator-visible logs did not say whether to check relay/base_url reachability, proxy mode, or provider access/quota next.
- `PASS`: runtime now emits targeted failure guidance for `execution_network_*`, `proxy_config_invalid`, `auth_failure`, `kiro_monthly_request_limit`, and `kiro_subscription_status_service_error`, and it logs the effective proxy mode together with the authoritative project/global config paths.
- `PASS`: the runtime config template now documents proxy mode semantics inline at `FREELY_NETWORK_PROXY_MODE` so the relevant control surface is visible where operators actually edit it.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-runtime-failure-guidance`
- `PENDING`: absorb this same-owner followthrough into canonical `develop`, then rerun daemon self-host supervision until Freely completes one real task, merges upward, retires the temporary lane, and advances to another task.

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
- `PENDING`: absorb this same-owner followthrough into canonical `develop`, then rerun `freely daemon start` until a real task completes, the corresponding worktree is lawfully closed, and the daemon proceeds to another task.

## 2026-04-21 09:25 PDT Develop Push Followthrough Tracking Refresh Verification

- `FAIL`: canonical `develop` self-host replay showed `pr-merge-guarded` had already pushed successfully, but local branch truth still reported `develop...origin/develop [ahead 73]`; manager therefore kept surfacing `develop_push_followthrough_state=push_pending` and never cleared that gating fact before cleanup sequencing.
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

## 2026-04-25 14:05 PDT Worker Runtime Rebind Guard Verification

- `FAIL`: canonical `develop` self-host replay had already moved past prompt generation and worker materialization. Manager wrote real continuity, worker prompt, and exit-contract artifacts, and the delegated worktree produced real owner evidence, but runtime immediately re-opened that same worker lane through `manager_worker_runtime_control_plane_rebind` because it compared versioned runtime-script files instead of the live worker process source. At the same time, `active_running_worker_count` could stay falsely elevated because cached hints overrode live process discovery.
- `PASS`: `worker_runtime_control_plane_needs_manager_source_rebind()` now prefers live worker supervisor/AI runtime source truth. When the active delegated lane already runs from the authoritative manager/source project, manager skips rebind and requests plain local continuation instead of stop/restart churn.
- `PASS`: `manager_semantic_loop_active_worker_count_for_project()` now returns live discovered worker count whenever process inspection is available, falling back to cached hints only on degraded hosts.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-skips-rebind-when-active-runtime-already-uses-manager-source`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-rebinds-stale-active-runtime-control-plane`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-active-worker-count-prefers-live-processes`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
- `PENDING`: replay this repair through protected premerge, merge into canonical `develop`, restart daemon replay, and verify the delegated worker no longer loops on repeated rebind/stop while Freely advances toward merge, retire, and next-task followthrough.

## 2026-04-25 12:50 PDT Control-Plane Helper Argv Contract Verification

- `FAIL`: after merge commit `a63f37e1` removed the worker runtime rebind loop, a fresh canonical `develop` daemon replay still stalled before manager AI launch. Supervisor `11693` stayed alive, but `.freely/run/interruption-dispatcher.pid` and `.freely/run/manager-watchdog.pid` remained absent, runtime never emitted `interruption_dispatcher_relaunch_ready`, and `live-status` reported `activity_state: stalled_without_runtime` with `last_exit_reason: starting`.
- `PASS`: direct process inspection showed the helper children were actually alive under that supervisor, but they were launched as `bash .../docs/system/workspace/scripts/runtime/freely ensure-interruption-dispatch ...` and `bash ... ensure-manager ...`, while runtime readiness only accepts commands carrying the `runtime/freely ...` argv contract.
- `PASS`: `launch_interruption_dispatcher()`, `launch_manager_watchdog()`, and `launch_manager_control_plane_recheck()` now use `exec -a 'runtime/freely ...'` so the background helpers advertise the same process identity contract that runtime pid discovery already validates.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-control-plane-launch-argv-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`
- `PENDING`: promote this repair through protected premerge, merge into canonical `develop`, restart daemon replay, and verify manager reaches AI launch instead of stalling behind invisible helper processes.

## 2026-04-22 08:05 PDT Materialized Cleanup Worker Selected-Tool Followthrough

- `FAIL`: canonical `develop` self-host replay advanced to manager-selected cleanup followthrough for `I-20260421-1200-A`, but the materialized cleanup worker prompt omitted `selected_tool`, so the retained cleanup worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-runtime-daemon-self-loop-blocker` kept relaunching on stale local `AI_TOOL=\"cc-use-codex-cli\"` and immediately re-entered runtime failure instead of closing the owner cleanup lane.
- `PASS`: `materialize_cleanup_worker_prompt_from_manager_continuity_if_needed()` now reads the authoritative tool from manager continuity first and falls back to current project tool truth only when continuity lacks it, then writes `- selected_tool: \`...\`` into the generated cleanup worker prompt.
- `PASS`: existing launch/recovery paths already honor `selected_tool`, so the narrow repair keeps cleanup materialization aligned with the same prompt contract manager launch and worker verification contract recovery already consume.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-materialized-cleanup-worker-applies-selected-tool`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-applies-selected-tool`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
- `PASS`: `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-cleanup-worker-prompt-selected-tool --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `PASS`: `./bin/governance-check`
- `PENDING`: promote through fresh protected premerge, merge into canonical `develop`, then restart daemon replay and verify the retained cleanup lane actually relaunches as `codex`, retires lawfully, and Freely advances to the next task.

## 2026-04-21 17:55 PDT Codex Resume Add-Dir Followthrough

- `FAIL`: after hygiene cleared, canonical `develop` replay finally reached manager continuity resume, but `tool_run_direct_from_prompt_file()` still passed `--add-dir` through `codex exec resume`; current Codex CLI rejects that form and the daemon looped on `ai_exit_rc_2` instead of resuming followthrough.
- `PASS`: fresh Codex launches still pass `--add-dir`, but resume launches now omit it so `codex exec resume --skip-git-repo-check <session>` matches the actual CLI contract.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-cleans-disposable-pycache-residue`
- `PENDING`: absorb this launcher repair into canonical `develop`, then rerun daemon self-host acceptance and verify resume no longer collapses into `ai_exit_rc_2`.

## 2026-04-22 09:10 PDT Empty Codex Session Resume Followthrough

- `FAIL`: canonical `develop` self-host replay progressed into cleanup governance for `I-20260421-1200-A`, but manager continuity still pointed at a persisted Codex session whose jsonl file existed at `/Users/zhaoyu/.codex/sessions/2026/04/22/rollout-2026-04-22T06-57-47-019db57b-8fe9-7cc3-81c3-36058a79c5c4.jsonl` with size `0`; runtime treated `-f` as sufficient resume evidence and the next manager launch failed immediately with `thread/resume failed: failed to load rollout ...jsonl: empty session file`.
- `PASS`: `docs/system/workspace/scripts/runtime/freely` now requires Codex rollout/session jsonl evidence to be non-empty before it can be reused as persisted resume truth, both when resolving a prior launch target and when accepting an observed post-cycle session id.
- `PASS`: the same helper now keeps recorded worker resume-evidence checks aligned with that stricter Codex truth, so a zero-byte `LAST_TOOL_JSONL_PATH` no longer advertises resumable state elsewhere in the runtime.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `PASS`: `./bin/governance-check`
- `PENDING`: replay this owner through fresh protected premerge, merge into canonical `develop`, restart `freely daemon start`, and verify cleanup governance falls back away from the empty Codex session file, retires the blocker cleanup lane, and advances to the next task.

## 2026-04-22 09:48 PDT Empty Repair Resume Target Followthrough

- `FAIL`: after the zero-byte session-file fix landed, canonical `develop` self-host replay advanced one step further but still forced `launch_kind=resume` for `manager_exit_contract_repair` even when `LAST_TOOL_RESUME_TARGET=""`; monitor preflight then failed immediately with `[ERROR] codex resume requires --tool-resume-target`, so daemon replay still could not reach the retained cleanup worker.
- `PASS`: `select_launch_kind()` now preserves exit-contract repair resumes only when the resolved pre-launch target is non-empty and the current tool still has verified resume evidence; otherwise the repair handoff downgrades to `fresh_with_handoff` with `missing_resume_evidence`.
- `PASS`: verified repair resumes still stay on `resume` when Codex has a real persisted rollout file for the recorded target, so this followthrough narrows only the empty-target case rather than regressing the earlier same-session repair contract.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `PENDING`: promote through fresh protected premerge, merge into canonical `develop`, restart `freely daemon start`, and verify this owner finally clears cleanup followthrough, retires the temporary blocker lane, and continues to another task instead of stopping at monitor preflight.

## 2026-04-23 07:18 PDT Cleanup Followthrough Resume Extraction

- `FAIL`: canonical `develop` still reached `cleanup_governance`, but manager exit-contract replay could accept `EXIT_KIND=resume_manager` and relaunch manager before executing the already-selected cleanup followthrough, leaving continuity pinned to the same retained merged-lane closeout instead of retiring it and advancing patrol.
- `FAIL`: when that cleanup path failed during replay, runtime only degraded into generic invalid-resume behavior without persisting an exact manager blocker that explains cleanup-followthrough failure as the real seam.

## 2026-04-24 01:05 PDT Nonlaunchable Cleanup Prompt Autofill

- `FAIL`: after the blocked recorded-owner repair merged to canonical `develop` as `1f3fbe2a`, a fresh daemon replay starting at `2026-04-24 00:47:41 PDT` finally proved manager was reading scan JSON first and selecting the retained dirty cleanup lane. The new blocker was narrower: manager wrote continuity plus `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-004759-worker-runtime-cleanup-followthrough-hygiene-codex.txt`, but that AI-written hygiene prompt lacked verification metadata, so `worker_prompt_launchable_for_manager_project()` rejected it for the already-merged retained lane and runtime looped on `manager_exit_contract_invalid details=WORKER_PROMPTS_NOT_LAUNCHABLE`.
- `PASS`: cleanup-governance retirement handoff detection and prompt materialization now look for an actually launchable prompt instead of treating any existing prompt path as sufficient. When continuity already contains only a nonlaunchable retained-lane prompt, runtime now appends the authoritative verification-bound cleanup prompt from owner continuity/issue truth and rewrites the delegate-workers contract to that launchable set.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-canonical-cleanup-continuity`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`
- `PENDING`: replay this repair through guarded premerge and guarded `develop` merge, then rerun canonical daemon replay until the retained cleanup worker actually launches, produces a lawful closeout/blocker result, and Freely returns to the next scan-selected task.

## 2026-04-24 03:15 PDT Current-Shape Continuity Autofill From Worker Verification Truth

- `FAIL`: a later fresh daemon replay starting at `2026-04-24 03:15:17 PDT` showed the nonlaunchable cleanup fix was still too tied to older continuity shape. Manager again selected the retained cleanup lane from scan truth and wrote `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260424-031528.md` plus `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-031528-worker-runtime-cleanup-followthrough-resume-hygiene-codex.txt`, but that continuity carried top-level `route_kind`, `## Worker Dispatch` inline `worker_prompt`, and no legacy `issue_truth` / `selected_cleanup_lane` fields. Runtime therefore could not recover the authoritative cleanup followthrough prompt even though the retained target worktree already held verification truth, and it stopped again on `manager_exit_contract_invalid details=WORKER_PROMPTS_NOT_LAUNCHABLE`.
- `PASS`: cleanup-governance recovery now accepts current continuity shape as sufficient truth. Runtime can read top-level `route_kind`, parse inline `worker_prompt:` entries from `## Worker Dispatch` / queue sections, infer the retained cleanup target from those prompt paths, and materialize a launchable authoritative cleanup prompt from the target worker's existing verification-bound prompt/contract when legacy continuity fields are absent.
- `PASS`: this keeps the launch gate strict. Runtime still refuses impossible `delegate_workers` contracts; it only recovers by inheriting verification metadata from already-authoritative worker truth for the same retained cleanup lane.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-from-worker-verification-truth`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `PENDING`: promote this compatibility repair through guarded premerge and canonical `develop`, then replay daemon start again to confirm runtime launches the cleanup worker instead of dying at prompt launchability repair.

## 2026-04-24 05:30 PDT Auth-Failure Timestamp False Positive Followthrough

- `FAIL`: canonical `develop` replay advanced far enough to let manager write fresh continuity plus a launchable worker prompt for the retained cleanup lane, but the next manager cycle still exited with `last_exit_reason=auth_failure` before consuming that queued worker prompt. Replay evidence showed the only extracted runtime error line was `apply_patch verification failed ... manager-exit-contract.env: No such file or directory`, yet `log_has_auth_failure()` still matched because the timestamp fragment `.401071Z` satisfied the old bare `401` regex branch.

## 2026-04-24 17:52 PDT Dispatch-State Cleanup Source-Prompt Fallback

- `FAIL`: a later fresh daemon replay starting at `2026-04-24 17:52:10 PDT` proved the current cleanup autofill repair still had one narrower continuity seam. Manager wrote `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260424-175210.md` with `route_kind=cleanup_governance` plus `## Dispatch State` `worker_prompt_paths:`, but no legacy `issue_truth`. The only referenced prompt was `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-175210-worker-runtime-lifecycle-receipt-closeout-reconcile-codex.txt`, an already-merged retained-lane `edit` prompt whose verification metadata still described the right owner surfaces even though the lane itself was no longer launchable as `edit`.
- `FAIL`: runtime could not parse `## Dispatch State` `worker_prompt_paths:` as launchable continuity truth for cleanup rematerialization, and when it did find that source prompt, it still lacked a fallback path that treated the continuity-carried prompt as metadata source only. The result was another `manager_exit_contract_invalid details=WORKER_PROMPTS_NOT_LAUNCHABLE` loop even though the retained lane already had enough owner metadata to mint a lawful cleanup prompt.
- `PASS`: continuity prompt discovery now parses `## Dispatch State` `worker_prompt_paths:` alongside the earlier current-shape sections, so cleanup-governance autofill can see the exact retained-lane prompt list that fresh replay produced.
- `PASS`: cleanup prompt rematerialization now falls back from legacy `issue_truth` and worker-local authoritative prompt truth to the continuity-carried source prompt for the same retained worktree, rebases owner/pre-tests/verification paths into that worker worktree, and rewrites `## Dispatch State` to the fresh cleanup prompt so the stale merged-lane `edit` prompt is not re-advertised as launchable authority.
- `PASS`: launchability stays strict. Runtime still rejects impossible `delegate_workers` contracts, and merged-lane `edit` / `promotion` prompts under cleanup governance remain non-owning once their branch is already merged into `develop`; they only serve as metadata source for the fresh cleanup prompt when that is the last authoritative verification truth left.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autofills-cleanup-prompt-from-continuity-source-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`
- `PENDING`: promote this narrower cleanup-governance fallback through protected premerge and guarded `develop` merge, then rerun canonical daemon replay to verify the retained receipt-closeout lane launches as cleanup followthrough instead of stopping at launchability repair.
- `PASS`: narrowed auth-failure detection to auth-specific phrases (`unauthorized`, `auth failed`, `authentication failed`, token/login/subscription phrases, and explicit `402 payment required` / `403 forbidden`) instead of treating any bare `401` substring in the error excerpt as an auth seam.
- `PASS`: strengthened `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter` with the real replay shape: a timestamped non-auth `ERROR` line whose fractional seconds contain `401`, proving runtime no longer converts ordinary file/update errors into `auth_failure`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-log-has-auth-failure-ignores-codex-apikey-oauth-refresh-noise`
- `PASS`: `./bin/governance-check`
- `PENDING`: replay this repair through guarded premerge and canonical `develop`, then rerun `freely daemon start` on `develop` to verify manager keeps the continuity/queued-worker truth alive, consumes the retained cleanup lane handoff, and resumes the larger self-host closeout loop instead of stopping on a fake `auth_failure`.

## 2026-04-24 01:18 PDT Retained Cleanup Self-Intent Relaunch Boundary

- `FAIL`: canonical `develop` replay after `c82592d5` advanced one seam further. Manager now repaired `delegate_workers`, parsed the queued cleanup prompt, and validated that prompt as launchable, but the selected worker still never launched. Logs and direct helper probes showed the failure sat exactly between `manager_exit_contract_delegate_workers` and `launch_worker_from_manager_prompt_if_needed`: manager preloaded `selected_intent_signatures_csv` from recorded worker ownership, and the retained merged cleanup lane then self-conflicted on its own stale recorded cleanup signature, leaving the prompt perpetually in `queued_worker_prompts` with no blocker text.
- `PASS`: manager launch selection now allows a bounded reclaim path only for cleanup prompts with verification metadata whose target is the same retained merged lane already represented by that recorded signature. This keeps ordinary duplicate-owner blocking intact while letting the canonical retained cleanup worker relaunch instead of self-queuing forever.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-retained-merged-cleanup-self-intent`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`
- `PENDING`: replay this repair through protected premerge and guarded `develop`, then rerun canonical daemon replay until the retained cleanup worker truly launches, returns cleanup truth, and Freely advances to the next scan-selected task.
- `PASS`: `manager_runtime_handle_exit_contract_after_ai_cycle()` now checks the active continuity for cleanup-followthrough intent before honoring `resume_manager`, runs that cleanup step first, and emits explicit `manager_exit_contract_cleanup_followthrough_begin` / `manager_exit_contract_cleanup_followthrough` receipts on success.
- `PASS`: when `run_cleanup_followthrough` fails on that path, runtime now writes a same-owner repair handoff, records `LAST_EXIT_REASON=manager_exit_contract_cleanup_followthrough_failed`, emits `manager_exit_contract_cleanup_followthrough_failed`, and returns `resume_invalid` instead of silently resuming broader patrol.

## 2026-04-24 05:45 PDT Recorded Self-Intent Relaunch Boundary

- `FAIL`: canonical `develop` replay after the auth-failure timestamp fix proved continuity-first delegation was working and the retained owner-rebind worker prompt was launchable, but manager still re-entered another manager round instead of consuming that prompt. Live runtime state showed `QUEUED_WORKER_PROMPTS` held the delegated prompt with `ACTIVE_RUNNING_WORKER_COUNT=0` and no ownership blocker summary, while direct helper probes proved `launch_worker_from_manager_prompt_if_needed()` itself succeeded for the same prompt.
- `PASS`: the remaining seam was narrower than the retained cleanup case. The delegated prompt carried `intent_kind=edit` with signature `edit@<target_worktree>`, and `manager_runtime_launch_workers_from_latest_handoff()` preloaded `selected_intent_signatures_csv` from recorded worker ownership, so the target lane self-conflicted on its own soft-stale recorded edit signature before launch.
- `PASS`: `manager_prompt_may_reclaim_recorded_self_intent()` now allows manager to reclaim that recorded self-intent whenever the prompt targets the same stopped worktree/signature, the target lane is only `soft_stale`, and no other worker plus no queued/frozen prompt still holds that signature. The older retained-cleanup merged followthrough reclaim path remains intact as a stricter subset.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-recorded-self-intent`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-retained-merged-cleanup-self-intent`
- `PASS`: protected replay on `test-pre-merge-20260424-recorded-self-intent` reran the recorded-self-intent relaunch regression, retained cleanup self-reclaim regression, duplicate cleanup recorded-owner queue regression, stale queued relaunch regression, `./bin/pretests-gate`, and `./bin/governance-check` without widening ordinary ownership blocking.
- `PENDING`: guarded `develop` merge still needs to land this repair and canonical daemon replay still must prove the delegated retained owner-rebind worker launches automatically, returns lawful cleanup / blocker truth, and Freely continues to the next task source instead of restarting manager patrol.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-cleanup-followthrough-failure-materializes-blocker`
- `PENDING`: rerun guarded premerge and canonical `develop` replay to verify cleanup followthrough now retires the retained blocker lane, clears `cleanup_governance`, and lets Freely continue toward the next task.

## 2026-04-23 08:05 PDT Codex OAuth Refresh Network Classification

- `FAIL`: latest worker replay still widened one real transport seam into generic runtime failure: Codex logged `Failed to refresh token: error sending request for url (https://auth.openai.com/oauth/token)`, and runtime surfaced that exit as `tool_runtime_failure` instead of bounded `execution_network_*`.
- `PASS`: tightened the existing same-owner network classifier so request-send failures on the Codex OAuth refresh path are treated as transport/network evidence, while explicit auth-denied evidence remains outside the network path.
- `PASS`: preserved the prior auth boundary by keeping OAuth refresh `401 Unauthorized` noise non-network, so auth/config problems do not masquerade as real device / wifi / hotspot instability.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-execution-network-failure-classification`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-ignores-codex-apikey-oauth-refresh-401`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-classifies-codex-oauth-refresh-request-error-as-network-failure`
- `PASS`: `./bin/governance-check`
- `PENDING`: refresh protected premerge with this owner evidence in diff, merge lawfully into `develop`, then restart canonical `develop` daemon replay and confirm the same failure family now lands on `execution_network_*` instead of `tool_runtime_failure`.

## 2026-04-23 16:05 PDT Project-Explicit Proxy Global Fallback

- `FAIL`: latest canonical `develop` daemon replay was no longer blocked on real network truth; it was blocked on proxy resolution precedence. Runtime repeatedly exited with `proxy_config_invalid` because project config set `FREELY_NETWORK_PROXY_MODE="explicit"` but left proxy values blank, while global config still had valid explicit proxy values.
- `FAIL`: the previous resolver treated project `explicit` as authoritative even when every project proxy field was empty, so an empty project block masked the usable global proxy and kept manager stuck in `network_recovery_gate_active`.
- `PASS`: proxy resolution now keeps `project` precedence but applies it field-by-field under `explicit`, so blank project proxy fields fall back to the corresponding global explicit values instead of turning into a false misconfiguration.
- `PASS`: this preserves the intended boundary: `disabled` still disables outright, `inherit` still keeps ambient shell proxy behavior unless config overrides it, and `explicit` still lets project config override individual fields such as `NO_PROXY`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-network-proxy-resolver`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-proxy-self-heal`
- `PASS`: `./bin/governance-check`
- `PENDING`: replay this same-owner resolver fix through protected premerge and guarded `develop`, then rerun canonical `develop` daemon replay and verify manager gets past `proxy_config_invalid`, resumes cleanup followthrough, and advances toward the next real task cycle.

## 2026-04-23 23:40 PDT Explicit Daemon Stop Boundary Refresh

- `FAIL`: fresh canonical restart observation proved startup was generating a new `manager-task-source-scan-latest.json`, but patrol still surfaced the older cleanup continuity because the manager freshness boundary had not moved with `operator_daemon_stop`.
- `FAIL`: this let the next startup round re-anchor on pre-stop cleanup continuity instead of letting the new scan-selected queue decide the next highest-leverage task source.
- `PASS`: `stop_project_runtime()` now refreshes the manager operator-stop boundary for both `operator_stop` and `operator_daemon_stop`, preserving the existing explicit-stop semantics while keeping runtime-owned restarts out of this path.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-stop-refreshes-manager-operator-boundary`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-pre-stop-manager-continuity-focus`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
- `PENDING`: promote this same-owner repair through protected premerge and guarded `develop`, rerun canonical `freely daemon start`, and verify startup patrol now discards pre-stop continuity, picks from fresh scan JSON, and continues through lawful task closeout instead of re-entering the stale cleanup anchor.

## 2026-04-23 23:58 PDT Queue State Worker Prompt Launch Followthrough

- `FAIL`: canonical `develop` replay got past the pre-stop delegated-continuation seam, but the retained dirty cleanup lane could still relaunch indefinitely after a lawful `worker_blocked` exit because recorded-owner recovery read the latest worker AI prompt instead of the authoritative delegated source prompt preserved in `worker-verification-contract.env`.
- `FAIL`: in the real runtime shape, that latest worker AI prompt may omit machine-readable `Worktree:` / `Branch:` dispatch headers, so ownership signature collapsed to empty, manager considered the same cleanup target unowned, and startup kept re-delegating the lane instead of consuming the blocker and advancing.
- `PASS`: `project_current_blocking_intent_signature()` now resolves intent from `status_intent_prompt_file_for_project()`, which already prefers the verification-contract `SOURCE_PROMPT_FILE` over later worker-local prompt artifacts.
- `PASS`: a focused regression now proves duplicate cleanup prompts queue behind the blocked recorded owner even when the latest worker AI prompt lacks dispatch headers, matching the retained cleanup-lane runtime shape from canonical `develop`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
- `PASS`: `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-cleanup-worker-blocked-consumption-boundary --issue /Users/zhaoyu/Downloads/code/my-freely/freely/docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `PASS`: `./bin/governance-check`
- `PENDING`: promote this same-owner repair through fresh protected premerge, merge into canonical `develop`, then rerun `freely daemon start` until the retained cleanup lane stays blocked/consumed instead of relaunching and the manager advances to the next scan-selected task.

- `FAIL`: after the stale pre-stop continuity was fenced off, canonical replay re-delegated the retained cleanup lane with `EXIT_KIND=delegate_workers`, but `manager-worker-launch-state.env` still showed `LAST_MANAGER_WORKER_PROMPTS_GENERATED=""`, `QUEUED_WORKER_PROMPTS=""`, and `LAUNCHED_WORKER_PROMPTS=""`.
- `FAIL`: the manager continuity was lawful and launchable, but runtime only parsed direct `## Worker Delegation` handoffs; the current `## Queue State` continuity shape with bare `worker_prompts:` was treated as prompt-empty, so the selected worker was never queued or launched.
- `PASS`: `manager_worker_prompt_paths_from_continuity_by_mode()` and the queue-state parser now accept both direct and bare `worker_prompts:` entries under `## Queue State`, preserving the same launchability truth that `delegate_workers` contract validation already enforced.
- `PASS`: focused regressions now cover both continuity parsing and post-AI-cycle launch under that exact queue-state handoff shape.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `PASS`: `bash -lc 'source docs/system/workspace/scripts/runtime/freely; latest_manager_worker_prompt_csv_from_continuity /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260423-235503.md'`
- `PENDING`: rerun protected premerge, merge into canonical `develop`, restart daemon replay, and verify the retained cleanup lane actually launches, returns cleanup readiness or exact blocker truth, retires lawfully, and lets manager move on to the next scan-selected task.

## 2026-04-24 00:41 PDT Pre-Stop Delegated Continuation Boundary Followthrough

- `FAIL`: after the queue-state worker prompt parser repair merged, fresh canonical restart still consumed `20260423-080027-p0-cleanup-supervision-latest-wo` as current delegated continuation even though `daemon stop` had already recorded a newer operator-stop boundary and startup had produced a fresh scan JSON.
- `FAIL`: delegated-continuation freshness only anchored to continuity truth; once pre-stop continuity was correctly fenced off, the floor collapsed to zero and older delegated continuation history leaked back into prompt/live-status scope.
- `PASS`: delegated-continuation freshness now takes the later of continuity truth and `manager-operator-stop-boundary.env`, while still allowing newer post-stop delegated continuation handoffs to remain eligible.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-ignores-pre-stop-delegated-continuation-after-operator-stop`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-pre-stop-delegated-intake-after-operator-stop`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-filters-stale-delegated-continuations`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-ignores-pre-stop-continuity`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-task-source-scan-ignores-pre-stop-continuity-anchor`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-live-status-ignores-stale-delegated-continuation-intake`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-stop-refreshes-manager-operator-boundary`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-filters-pre-stop-manager-continuity`
- `PENDING`: replay through guarded premerge and canonical `develop`, then verify startup no longer re-consumes stale cleanup continuation and can return to scan-selected next-task patrol once retained cleanup truth settles.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
3. `bash docs/system/workspace/scripts/tests/test-freely-daemon-stop-refreshes-manager-operator-boundary`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
5. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
6. `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
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
- `PASS`: replayed `feature/manager-followthrough-handoff-resume-20260421 -> test-pre-merge-20260421-manager-followthrough-handoff-resume` through `freely pr-merge-guarded`; the protected test lane stayed green on the representative same-owner regressions.
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

1. Replay `feature/manager-exit-contract-expected-worker-guard-20260421 -> test-pre-merge-20260421-manager-exit-contract-expected-worker-guard -> develop` through `freely pr-merge-guarded` with this refreshed owner evidence included.
2. On canonical `develop`, run `freely daemon start` until one task completes to the current-project success standard, its temporary worktree closes lawfully, and the daemon proceeds to the next task.
3. Retire the temporary feature/test-pre-merge lanes for this stop-guard followthrough after canonical replay succeeds.

## 2026-04-21 23:10 PDT Ordinary Manager Stall Recovery Followthrough

- `FAIL`: canonical `develop` self-host replay advanced past the retired absorbed-cleanup lane, but a fresh manager `codex` round with no delegated continuation, no new intake, and no new runtime artifacts could still sit on one ordinary prompt indefinitely; existing stall recovery only covered pending-intake and delegated-continuation shapes, so autonomy could stop making progress without triggering a repair handoff.
- `PASS`: runtime now treats a manager round with an ordinary prompt, no pending intake, no delegated continuation, and no runtime log progress beyond the stall threshold as recoverable stalled manager work, and forces the same local continuation reentry path already used by the narrower stall classes.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery-without-runtime-progress`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-stall-recovery`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
- `PENDING`: replay this followthrough through guarded promotion, then rerun canonical `develop` daemon self-host acceptance until Freely completes one task, retires the corresponding temporary lane lawfully, and advances to another task.

## 2026-04-21 23:35 PDT Worker Restart Selected-Tool Followthrough

- `FAIL`: canonical `develop` self-host replay still could not clear the cleanup worker followthrough because a freshly restarted expected-running worker came back with `tool=cc-use-codex-cli` instead of the delegated prompt's `selected_tool=codex`, immediately re-entered `tool_runtime_failure`, and kept the same owner lane in recovery loop.
- `PASS`: worker startup now reads the authoritative delegated tool back from `worker-verification-contract.env` `SOURCE_PROMPT_FILE` and reapplies that `selected_tool` before launch whenever the worker is being restarted from fresh runtime state.
- `PASS`: this keeps worker restart truth aligned with the delegated prompt contract instead of whatever fallback tool a previous failed attempt happened to persist.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-restart-reapplies-selected-tool-from-verification-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-applies-selected-tool`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-tool-runtime-failure-uses-unified-auto-recovery-path`
- `PASS`: `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-manager-exit-contract-expected-worker-guard --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `PASS`: `./bin/governance-check`
- `PENDING`: replay this same-owner continuation through fresh test-pre-merge and guarded `develop` merge, then rerun canonical `develop` self-host acceptance until Freely completes one task, closes that temporary worktree, and continues to the next task without falling back into the stale-tool worker restart loop.

## 2026-04-22 00:44 PDT Non-Launchable Delegate Contract Followthrough

- `FAIL`: canonical `develop` self-host replay advanced further, but manager could still exit with `EXIT_KIND=delegate_workers` after generating only a cleanup prompt for an already absorbed `retire_ready` merged worker lane; the contract claimed delegation succeeded even though the same runtime launch gate would refuse to launch that prompt.
- `PASS`: manager exit-contract validation now requires `WORKER_PROMPTS_CSV` to contain at least one prompt that `worker_prompt_launchable_for_manager_project()` would actually launch; otherwise runtime records `WORKER_PROMPTS_NOT_LAUNCHABLE` and forces same-session manager repair via `resume_invalid`.
- `PASS`: added `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt` to reproduce the exact absorbed+merged+retire-ready cleanup-lane contradiction and prove runtime rejects the impossible delegate contract.
- `PASS`: reran `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`.
- `PASS`: reran `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-blocks-stop-with-unresolved-worker`.
- `PASS`: reran `./bin/governance-check`.
- `PASS`: replayed the same three runtime regressions plus `./bin/governance-check` on fresh protected lane `test-pre-merge-20260421-manager-exit-contract-expected-worker-guard-v2`; all passed there as well.
- `PENDING`: rerun guarded `develop` merge with this owner evidence in the diff, then restart canonical `develop` runtime and continue self-host replay until Freely completes one task to the current-project success standard, closes that lane lawfully, and proceeds to the next task.

## 2026-04-22 03:15 PDT Repair Handoff Relaunch Verification

- `FAIL`: canonical `develop` self-host replay progressed to `manager_exit_contract_invalid`, but the next manager round relaunched as `fresh rotation_reason=initial_start`; that reopened broad patrol and allowed newer intake to supersede the repair round before a valid exit contract existed.
- `PASS`: launch-kind selection now treats persisted `manager_exit_contract_repair` / `worker_exit_contract_repair` handoffs as resume-only relaunches and refuses to classify a restart with existing handoff/resume evidence as a true first launch.
- `PASS`: the supervisor loop now flips `FIRST_ROUND=false` immediately after the first AI cycle, so same-process `resume_invalid` / `resume_manager` loops cannot regress into `initial_start` before the repair path completes.
- `PASS`: `tool_has_resume_evidence()` now resolves resume evidence against the actual project root instead of an unbound local `project` variable during repair relaunch selection.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-forces-resume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-new-intake-reentry`
- `PASS`: replayed the same three regressions plus `bash -n docs/system/workspace/scripts/runtime/freely` on protected lane `test-pre-merge-20260422-manager-repair-handoff-intake-supersede`.
- `PENDING`: rerun guarded `develop` merge with this refreshed owner evidence, then restart canonical `develop` daemon replay and verify the repair handoff now stays on same-context resume long enough to finish one task, retire the temporary lane, and continue to the next task.

## 2026-04-22 03:44 PDT Daemon Recovery Preserves Control Plane

- `FAIL`: canonical `develop` daemon replay then exposed one narrower same-owner seam: after `tool_runtime_failure`, supervisor cleanup correctly kept `desired_state=running`, but later manager recovery relaunched `start --project` foreground supervisors and broke daemon-mode single-control-plane semantics.
- `PASS`: `workcell-state.env` now persists the authoritative control-plane entrypoint mode as `LAST_ENTRYPOINT_MODE`, with daemon/foreground truth preserved across later state writes even after the original supervisor exits.
- `PASS`: manager supervisor relaunch now consumes that persisted entrypoint truth and uses `daemon-run --project` for daemon-owned recovery while leaving foreground-owned recovery on `start --project`.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-reuses-live-supervisor-without-relaunch`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
- `PENDING`: absorb this daemon-preservation repair into canonical `develop`, rerun `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and continue supervision until Freely finishes a real task, merges upward, retires that lane, and autonomously selects the next task.

## 2026-04-24 07:05 PDT Superseded Frozen Prompt Reclaim

- `FAIL`: canonical `develop` still stalled after the recorded self-intent reclaim repair. The authoritative retained-lane prompt `20260424-054822` stayed in `QUEUED_WORKER_PROMPTS` with `ACTIVE_RUNNING_WORKER_COUNT="0"` because older same-lane frozen prompts were still treated as stronger ownership blockers than the newer authoritative prompt that explicitly superseded them.
- `PASS`: runtime now parses the prompt-level `This prompt supersedes...` history and excludes superseded frozen prompts from blocking-intent ownership, frozen-signature preloading, and frozen-owner worktree claims.
- `PASS`: this keeps continuity-first intact. Manager still reuses the same authoritative retained-lane prompt instead of widening scope into fresh scan selection, but runtime can now consume that prompt instead of queueing forever behind stale frozen history.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-recorded-self-intent`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-superseded-frozen-self-intent`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `PENDING`: guarded premerge replay is green, but canonical `develop` replay still must prove the retained cleanup lane relaunches from the authoritative prompt, writes bounded followthrough truth, and then Freely advances to the next task source instead of looping on frozen-owner queue residue.

## 2026-04-24 06:38 PDT Active Authoritative Worker Prompt Consumption Reconcile

- `FAIL`: canonical `develop` continuity-first replay progressed one step further, but manager could still leave the current authoritative retained-lane prompt in `QUEUED_WORKER_PROMPTS` even while the exact target worker was already active on that same prompt. The result was repeated supervision/launch churn instead of waiting on the running worker and then continuing the selected followthrough.
- `PASS`: runtime now recognizes when a manager prompt matches the active worker lane's authoritative prompt and treats that prompt as already consumed/launched rather than as an unconsumed queued item.
- `PASS`: the repair stays narrow. Workers that are merely busy with delegated continuation still remain queued; only the exact active authoritative prompt is auto-consumed.
- `PASS`: `manager_continuity_has_unconsumed_launchable_worker_prompt()` now skips those active authoritative prompts, `manager_continuity_waiting_on_active_busy_worker()` now waits on them, and `manager_runtime_launch_workers_from_latest_handoff()` records them into consumed launch state instead of trying to relaunch.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-authoritative-worker-consumes-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-busy-worker-queue`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `PENDING`: guarded promote and canonical `develop` daemon replay still need to prove the retained runtime-cleanup lane finishes, merges/retires lawfully, and Freely then returns to scan-selected backlog instead of spinning on same-prompt supervision.

## 2026-04-24 06:55 PDT Queued-Owner Self-Block Boundary

- `FAIL`: canonical `develop` continuity-first replay still showed the retained 05:48 worker prompt in `QUEUED_WORKER_PROMPTS` with `blocked_by=<same prompt> state=queued-owner`. This was not a scan-json routing regression; root continuity still chose the retained cleanup-followthrough lane first.
- `PASS`: the narrower seam sat in queued-owner bookkeeping for current `## Worker Delegation` continuity. `latest_queued_manager_worker_prompt_paths_from_continuity()` was still treating direct/launchable worker-delegation prompt paths as queued-owner candidates, so the exact authoritative prompt could block itself.
- `PASS`: queued-owner parsing now only accepts explicit `queue` subsection entries for `## Worker Delegation`; direct/launchable prompt paths remain launchable truth and no longer self-register as queued owners.
- `PASS`: direct worker-delegation launch still works, active authoritative workers still consume/wait on the exact prompt, and real earlier queued-owner blockers still surface for true duplicate queued prompts.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-authoritative-worker-consumes-prompt`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-explainability-queued-owner`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `PASS`: `bash -n docs/system/workspace/scripts/runtime/freely`
- `PENDING`: run owner gates on this feature lane, stage protected premerge evidence, merge back to canonical `develop`, and rerun `freely daemon start` until the retained lane closes lawfully and runtime advances to the next scan-selected task.

## 2026-04-24 07:26 PDT Worker Exit Contract Wins Over Network Transient

- `FAIL`: canonical `develop` continuity-first replay advanced past queued-owner self-block, and the retained worker lane then wrote a valid `worker-exit-contract.env` with `EXIT_KIND="worker_done"`, but runtime still recorded the same AI cycle as `execution_network_transient` and immediately relaunched the lane. That left manager stuck waiting on the active retained worker forever even though the worker had already emitted machine-readable completion truth.
- `PASS`: the seam was in `worker_runtime_handle_exit_contract_after_ai_cycle()`. Worker exit contracts were only consumed when `exit_reason=ai_exit_rc_0`, so any reconnect-classified exit that happened after the contract file landed would bypass the contract and fall straight into proxy/self-heal retry.
- `PASS`: runtime now lets a valid worker exit contract override `execution_network_transient`, `execution_network_persistent`, and `proxy_config_invalid` only when the contract file already exists and validates. Missing or malformed contracts still stay on bounded network recovery instead of being misclassified as repair-needed completion.
- `PASS`: this keeps continuity-first intact. The retained lane still resumes directly from its authoritative continuity instead of broad scan patrol, but once the worker has already written lawful `worker_done` truth, network reconnect noise no longer forces the same lane back into infinite relaunch.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-overrides-network-transient`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-does-not-override-network-transient`
- `PASS`: `bash -n docs/system/workspace/scripts/runtime/freely`
- `PENDING`: run owner gates on this feature lane, stage protected premerge evidence, merge to canonical `develop`, and rerun `freely daemon start` until the retained cleanup lane closes, promotes/cleans up lawfully, and runtime returns to the next scan-selected task source.

## 2026-04-24 07:44 PDT Manager-Owned Worker Runtime Source Rebind

- `FAIL`: canonical `develop` continuity-first replay advanced past the worker-exit-contract seam, but the retained worker lane still stayed under a supervisor started at `2026-04-24 06:35:03 PDT` from that worktree's own runtime script. The lane had already written lawful `EXIT_KIND="worker_done"` truth, yet manager supervision kept depending on stale worktree-local runtime code instead of the current canonical manager runtime.
- `PASS`: this is a control-plane seam, not a scan-json or manager-role seam. Root continuity still selected the retained cleanup-followthrough lane first, but worker relaunch/reentry could keep inheriting the target worktree's older runtime implementation after later fixes were absorbed into `develop`.
- `PASS`: `start_workcell_supervisor_async()` now uses the manager/source project's runtime bin whenever manager is launching or relaunching a distinct worker worktree, so canonical `develop` remains the authoritative control plane for retained worker supervision.
- `PASS`: active-worker launch reconciliation now detects when a still-running worker worktree is on stale runtime code relative to the manager source runtime, requests a local runtime-handoff stop, and relaunches that worker control plane under the manager/source runtime instead of doing plain local continuation reentry.
- `PASS`: this stays continuity-first. The retained lane is still the first task to finish; the repair only rebinds who supervises that same lane so the already-merged closeout fixes on `develop` can finally govern it.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-uses-source-runtime-bin`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-rebinds-stale-active-runtime-control-plane`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `PASS`: `bash -n docs/system/workspace/scripts/runtime/freely`
- `PENDING`: run owner gates on this feature lane, promote through protected premerge into canonical `develop`, then prove real daemon replay rebinds the retained worker control plane, consumes its existing `worker_done` closeout, retires/advances that lane lawfully, and only then returns to scan-selected backlog.

## 2026-04-24 15:03 PDT SIGPIPE Supervisor Closeout Guard

- `FAIL`: canonical replay after the runtime-source rebind still stranded supervisor closeout. Runtime evidence showed `ai_launch_begin` with no matching `ai_cycle_finished`, stale `ai.pid` truth, and repeated `printf: write error: Broken pipe` lines while daemon patrol and continuity scanning were still resolving retained cleanup followthrough.
- `PASS`: the narrower seam sat in cached discovery producers, not in task selection. `project_worktree_list_porcelain_cached()` and `manager_continuity_files_desc_for_project()` were still writing with bare `printf`, so early-return consumers in continuity selection and PID/worktree discovery could abort the supervising shell under `set -euo pipefail`.
- `PASS`: both cached producers now emit through a bounded helper that traps `PIPE`, ignores `SIGPIPE`, and returns success when the consumer exits after finding the first useful record.
- `PASS`: this stays continuity-first and same-owner. No worker-launch policy, prompt shape, or exit-contract semantics changed; runtime simply no longer dies because the producer side treats a lawful early consumer exit as fatal.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-continuity-discovery-tolerates-closed-pipe`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-ignores-pre-stop-continuity`
- `PASS`: replayed the same focused regression set on protected lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-runtime-sigpipe-supervisor-closeout` after a lawful `freely pr-merge-guarded` merge from `feature/runtime-sigpipe-supervisor-closeout-20260424`.
- `FAIL`: the next guarded merge into canonical `develop` is blocked only by missing same-owner lifecycle materialization in the diff, not by code or test failure.
- `PENDING`: rerun guarded promote into `develop`, then replay canonical `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` to confirm retained cleanup closeout is consumed without another SIGPIPE stall and runtime continues to the next task source.

## 2026-04-24 16:05 PDT Daemon Entrypoint Mode Preservation Followthrough

- `FAIL`: after the SIGPIPE repair proved supervisor closeout could reach `ai_cycle_finished`, the same current canonical replay window beginning at `2026-04-24T22:09:45Z` exposed a narrower ownership seam. Daemon supervisor `39611` reached `L041 ai_launch_observed child_pid=40603`, but watchdog later recorded `L223 manager_idle_supervisor_restart`, and `runtime-events.log` then showed `2026-04-24T22:20:33Z event=user_start_command_received` for foreground supervisor `54468`.
- `PASS`: root cause was bounded and same-owner. `monitor-ai-cli.sh` rewrote `.freely/run/workcell-state.env` to `LAST_EXIT_REASON="ai_launch_in_flight"` but dropped `LAST_ENTRYPOINT_MODE`, so any later `project_control_plane_entrypoint_mode()` read fell back to `foreground` and `launch_manager_supervisor()` selected `start --project` instead of `daemon-run --project`.
- `PASS`: `monitor-ai-cli.sh` now preserves the previously recorded entrypoint mode when writing launch-in-flight state, so daemon-owned manager recovery keeps daemon ownership semantics across AI launch observation.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-failure-recovery-preserves-daemon`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`
- `PENDING`: replay this repair through fresh protected premerge and canonical `develop`, then rerun `freely daemon start` until runtime completes one task lawfully, retires that lane, and advances to the next task instead of drifting back into foreground ownership.

## 2026-04-25 11:20 PDT Manager / Worker Self-Loop Recovery Absorption

- `FAIL`: canonical `develop` dogfooding still exposed one bounded same-owner chain after the earlier cleanup/continuity repairs. `freely daemon start` did launch and keep writing manager continuity, but delegated targets could still fall back to manager-mode behavior because runtime kept trusting branch/worktree role hints over authoritative worker verification truth. When that happened on `test-pre-merge-*` or other manager-default targets, the delegated lane stayed stuck at `LAST_EXIT_REASON=starting` with no `ai.pid`, the parent launch slot stayed occupied, and manager kept regenerating the same prompt instead of letting the worker close out, retire, and advance to the next task.
- `PASS`: runtime now derives effective delegated-worker role from the authoritative worker verification contract, reclaims delegated targets that remain `starting` past the existing grace without valid `ai.pid`, and reconciles stale launched-worker state on the dispatch-critical path before deciding whether another worker prompt is launchable.
- `PASS`: the same repair keeps manager supervision alive during between-round relaunch grace and while expected-running workers are still active, preserves terminal worker exit truth through cleanup/closeout instead of relaunching finished workers, normalizes authoritative worktree-path comparisons, and clears stale launch/discovery residue after cleanup followthrough.
- `PASS`: this confirms the project architecture the dogfooding evidence implied. AI role is not assigned by a bare `agent` / `skill` / free-text prompt label. Manager/worker handoff is artifact-driven: manager writes machine-readable delegation artifacts and continuity, runtime consumes those artifacts as the control plane, launches the next manager or worker AI, and later consumes worker/manager exit contracts to decide whether to continue, review, delegate again, clean up, retire, or patrol the next task.
- `PASS`: feature-local regressions passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-daemon-autonomous-existing-worktree-review-merge-retire-next-task-loop`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-active-stall-recovery-from-manager-watchdog`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
  - `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `PASS`: protected replay already accepted this same implementation onto `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-test-pre-merge-runtime-lifecycle-followthrough` as merge commit `08129972ab13aa9672521f1167feba279a32ec66`, and focused premerge regressions there passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-runtime-effective-worker-role-from-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-worker-starting-stuck-reclaim`
- `FAIL`: the previous attempt to merge protected replay into `develop` was blocked by governance because the diff still carried this repair as candidate-only material instead of explicit owner-linked issue/progress/review evidence for `I-20260421-1200-A`.
- `PENDING`: absorb this repair into the canonical owner docs, rerun guarded promotion with the new owner-linked artifact, merge into `develop`, restart daemon replay on canonical `develop`, and keep looping until Freely proves select -> finish -> merge upward -> retire -> next task without manual intervention.

## 2026-04-25 13:05 PDT Terminal Handoff Slot Collapse

- `FAIL`: after the manager/worker role + `starting`-stuck repair merged into canonical `develop` as `2fd905c9`, real daemon replay still exposed one narrower same-owner seam. Root runtime no longer mis-launched the delegated `test-pre-merge` target, but after that target emitted terminal `EXIT_KIND="worker_handoff_needed"` and materialized a fresh local followthrough prompt, root `manager-worker-launch-state.env` still held `ACTIVE_RUNNING_WORKER_COUNT="1"` with `LAST_MANAGER_WORKER_PROMPTS_CONSUMED=none` and no surviving launched prompt.
- `FAIL`: the stale count came from the semantic-loop hint itself, not from a still-running worker. `manager_worker_launch_state_reconcile_prompt_liveness()` correctly pruned the old outer launched prompt because the delegated target was terminal, but then recomputed active workers through `manager_semantic_loop_active_worker_count_for_project()`, which preferred the old hinted count over discovered reality even though the current continuity's launched prompt set had already collapsed to empty.
- `PASS`: this seam still belongs to `I-20260421-1200-A`. The runtime control plane remains artifact-driven: manager/worker identity is operationally assigned by verification/delegation artifacts and exit contracts, while runtime is the middleman that decides whether to keep the manager alive, delegate another worker, or consume worker handoff/closeout followthrough. The remaining bug was stale launch-state bookkeeping after a terminal handoff, not confusion over agent/skill/prompt taxonomy.
- `PASS`: `manager_worker_launch_state_reconcile_prompt_liveness()` now collapses `ACTIVE_RUNNING_WORKER_COUNT` back to the actually discovered worker count when the current continuity's launched prompt set has been fully pruned. This keeps the old hint behavior for genuinely active delegated lanes, but stops a terminal or reclaimed slot from pinning the parent manager in false wait state forever.
- `PASS`: focused regressions passed for the new seam and adjacent recovery surface:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `FAIL`: the current owner pre-tests had drifted into falsely advertising canonical develop acceptance as already `pass`. That status is now corrected back to `pending` until real daemon replay proves the full success standard: select task -> finish -> merge upward -> retire worktree -> continue to next task.
- `PENDING`: commit this same-owner continuation, replay it through fresh protected premerge and guarded `develop`, then rerun canonical `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` until Freely either meets the full autonomous-loop success standard or exposes the next bounded same-owner seam with fresh evidence.

## 2026-04-25 16:20 PDT Manager / Worker Terminal Followthrough Materialization

- `PASS`: the current worker lane stayed within `I-20260421-1200-A`. The dirty runtime/tests diff is a same-owner continuation covering three artifact-quality seams only: Codex explicit resume now requires effective output evidence instead of token-count-only jsonl presence, manager `ai_exit_rc_0` rounds without effective output now fall back to continuity/repair instead of stale auto-resume, and terminal worker exit contracts now materialize a delegated manager continuation intake with idempotent content.
- `PASS`: the delegated handoff's focused `feature-local` set passed in this worktree:
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-empty-success-falls-back`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-missing-continuity-autoresumes`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-overrides-network-transient`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-invalid-does-not-override-network-transient`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-delegated-continuation-not-active-intake`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-materializes-worker-done-continuation`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-materializes-worker-blocked-continuation`
  - `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-terminal-followthrough-materialization-idempotent`
  - `./bin/governance-check`
- `PASS`: owner-linked evidence for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-worker-terminal-followthrough-materialization-verification.md`, so manager no longer needs to infer this repair from candidate-only diff state.
- `PENDING`: manager should consume the parked clean premerge lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-runtime-target-worker-role-and-starting-stuck-recovery` next as the first guarded-merge adequacy surface; if that parked evidence is judged stale against current diff, request a fresh protected replay instead of promoting directly from feature-local evidence.

## 2026-04-25 17:30 PDT Manager Post-AI-Cycle Finalize Grace

- `FAIL`: real canonical `develop` daemon evidence still exposed one narrower same-owner seam after the previous followthrough repairs landed. The root lifecycle trace showed `L041 ai_launch_observed` for the live manager supervisor, then within a few seconds watchdog emitted `L223 manager_idle_supervisor_restart trigger=supervisor_alive_ai_missing_after_grace`, and only later would the same round have been expected to write `L042 ai_cycle_finished`.
- `FAIL`: this meant Freely was not fundamentally confused about task selection or manager/worker taxonomy. The runtime middleman had simply not modeled the post-launch / pre-finalize transition, so a manager that was still materializing terminal closeout or delegated followthrough could be mistaken for an idle orphan and restarted mid-closeout.
- `PASS`: the bounded fix stays inside `I-20260421-1200-A`. `ensure_manager_once()` now recognizes a dedicated finalize window when the current `supervisor_pid` has observed `L041` but not yet emitted later terminal checkpoints (`L042`, `L090`, `L091`, `L092`) and keeps that supervisor alive for `FREELY_MANAGER_POST_AI_CYCLE_FINALIZE_GRACE_SECS` instead of triggering `supervisor_alive_ai_missing_after_grace`.
- `PASS`: focused `feature-local` verification passed for the new seam and adjacent closeout surfaces:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-overrides-network-transient`
  - `./bin/governance-check`
- `PASS`: a fresh guarded replay on `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-manager-worker-terminal-followthrough-materialization` absorbed the same owner commit and reran the same focused suite successfully, so this bounded repair now carries explicit issue/progress/pre-tests/review evidence rather than code-only diff state.
- `PASS`: owner-linked verification for this seam is staged in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-post-ai-cycle-finalize-grace-verification.md`.
- `PENDING`: rerun guarded merge into `develop`, then stop the root daemon, restart it from merged `develop`, and keep watching real lifecycle/runtime evidence until Freely either proves the full autonomous loop or surfaces the next bounded same-owner seam.

## 2026-04-25 18:05 PDT Terminal Handoff Followthrough Absorb

- `FAIL`: real canonical `develop` replay then exposed one more narrower same-owner seam after finalize grace. Manager did write a newer authoritative followthrough prompt for the delegated retained lane, but that target worktree still held an older terminal `worker-exit-contract.env` with `EXIT_KIND="worker_handoff_needed"`. `manager_runtime_launch_workers_from_latest_handoff()` saw the stale terminal contract first, treated the lane as already terminal, and skipped relaunching the new prompt.
- `FAIL`: this is the precise manager/worker handoff seam the current dogfooding evidence points at. The architecture is still artifact-driven: manager writes authoritative continuity and worker prompt artifacts, runtime is the middleman that consumes them, and worker exit contracts are just one artifact family. The bug was that stale terminal truth outranked the newer authoritative followthrough prompt for the same lane.
- `PASS`: the fix stays inside `I-20260421-1200-A`. `manager_runtime_launch_workers_from_latest_handoff()` now absorbs `worker_handoff_needed` terminal truth when the same lane already has a newer authoritative followthrough prompt, launches that prompt, clears the stale terminal exit contract after successful launch, records `worker_exit_contract_handoff_absorbed`, and refreshes launched/active bookkeeping so manager can keep the same lane moving instead of redelegating or idling forever.
- `PASS`: focused `feature-local` verification passed for the exact seam and adjacent launch-state surface:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-workers-absorbs-terminal-handoff-followthrough`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-absorbs-terminal-handoff-followthrough`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
- `FAIL`: guarded `develop` promotion was still blocked after the code patch because the merge diff lacked explicit same-owner lifecycle materialization for this continuation. The blocker was governance evidence, not code/test failure.
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-terminal-handoff-followthrough-absorb-verification.md`.
- `PENDING`: replay this updated owner through protected premerge, merge into canonical `develop`, restart the root daemon, and keep watching until Freely either completes one task with lawful merge/retirement and advances to the next task or exposes the next bounded seam with fresh evidence.

## 2026-04-25 18:55 PDT Delegated Continuation Pending-State Contradiction

- `FAIL`: another same-owner seam showed up after terminal followthrough absorb. Root runtime session-state persisted the same delegated continuation ids in both `LAST_DELEGATED_CONTINUATION_PENDING_IDS` and `LAST_DELEGATED_CONTINUATION_CONSUMED_IDS` even though the active manager prompt already carried `Delegated continuation handoff:` for those ids.
- `FAIL`: this was not a task-selection defect and not a role-taxonomy problem. The manager/worker/runtime contract remained artifact-driven and already had the correct delegated target. The blocker was contradictory runtime bookkeeping: `append_manager_consumed_continuity_resume_focus_if_needed()` only narrows the prompt when pending count is zero, so the stale pending surface could keep manager looping as if backlog were still waiting.
- `PASS`: this continuation stays inside `I-20260421-1200-A`. `start_project_runtime()` now clears delegated pending ids/count before writing `session-state.env` whenever the current active prompt already contains the delegated continuation handoff block, while preserving the same ids as consumed truth.
- `PASS`: focused feature-local verification passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-session-state-clears-pending-on-active-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
- `PASS`: protected replay was staged on `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-delegated-continuation-pending-state-fix`, and the same focused regressions passed there as well.
- `FAIL`: the first attempt to bring that protected replay into canonical `develop` was rejected by governance because the diff still lacked explicit same-owner issue/progress/review materialization for this continuation. The blocker is owner evidence, not the code path or regression set.
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-delegated-continuation-pending-state-verification.md`.
- `PENDING`: rerun guarded promote with the refreshed owner evidence, merge into canonical `develop`, restart root daemon replay, and verify manager now executes the absorbed delegated followthrough instead of re-exposing the same ids as pending backlog.

## 2026-04-25 18:05 PDT Manager Resume Prompt-Build Grace

- `FAIL`: after the finalize-gap repair, the same canonical replay still exposed one narrower watchdog seam. The live manager supervisor could already write a new `L020 prompt_build_begin` for the resumed round after `L042 ai_cycle_finished`, yet `ensure-manager` still fell through to `L223 manager_idle_supervisor_restart` once the generic between-rounds grace expired before prompt build completed.
- `PASS`: this confirms the runtime architecture boundary more sharply. The blocker is not that manager failed to choose work or that worker/manager roles are conceptually wrong; runtime already had the next round and the next continuity handoff. The middleman simply was not treating resumed prompt-build startup lifecycle as authoritative keepalive truth.
- `PASS`: `ensure_manager_once()` now reuses `supervisor_startup_lifecycle_in_flight()` directly when the same supervisor is already inside `L010|L020|L021|L022` for the next round, so watchdog keeps that supervisor alive across slow resumed prompt builds instead of spawning a redundant replacement control plane.
- `PASS`: focused `feature-local` verification passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-resume-prompt-build`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup`
- `PASS`: owner-linked feature-local verification for this seam is staged in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-resume-prompt-build-grace-verification.md`.
- `PASS`: protected `premerge-integration` replay passed at `2026-04-25 17:46 PDT` on `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-manager-worker-terminal-followthrough-materialization-r2`:
  - `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-resume-prompt-build`
  - `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-between-rounds-relaunch-grace`
  - `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
  - `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-pre-prompt-startup`
  - `./bin/test-lane premerge-integration -- ./bin/governance-check`
  - `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-manager-worker-terminal-followthrough-materialization-r2 --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md --require-adequacy --target-lane premerge-integration --promotion-gate develop_merge`
- `PENDING`: merge this protected lane lawfully into `develop`, restart the root daemon from merged `develop`, and keep observing whether Freely now continues through select -> finish -> merge upward -> retire -> next task rather than stuttering at manager round boundaries.

## 2026-04-25 19:05 PDT Post-L042 Followthrough Keepalive

- `FAIL`: after the earlier `post-L041/pre-L042` finalize repair and the resumed prompt-build keepalive repair, canonical `develop` replay still exposed one narrower watchdog seam. The live manager supervisor could already record `L042 ai_cycle_finished`, but `ensure-manager` still treated that same supervisor as terminal/idle and emitted `L223 manager_idle_supervisor_restart` before exit-contract replay or delegated-followthrough materialization wrote any later `L090|L091|L092` truth.
- `PASS`: this stays inside `I-20260421-1200-A`. The architecture remains artifact-driven: manager writes continuity/delegation/exit-contract artifacts, runtime is the middleman that consumes them, and the bug is that watchdog misclassified `L042` as “already done” instead of “same supervisor still finalizing followthrough”.
- `PASS`: `manager_supervisor_post_ai_cycle_finalize_in_flight()` now treats same-supervisor `L042` as keepalive evidence for `FREELY_MANAGER_POST_AI_CYCLE_FINALIZE_GRACE_SECS` unless a later terminal checkpoint has already been written, so watchdog no longer restarts the live manager in the narrow post-cycle followthrough window.
- `PASS`: the top-level keepalive regression now feeds `L041 -> L042` into `ensure_manager_once()` directly, so the bounded fix is locked at the real `L042 -> no L223` control-plane seam rather than only at the helper layer.
- `PASS`: focused feature-local verification passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-overrides-network-transient`
- `PASS`: protected replay passed on `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260425-test-pre-merge-post-l042-followthrough-keepalive-grace` with the same focused regressions:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-during-post-ai-cycle-finalize-grace`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-overrides-network-transient`
- `FAIL`: the first attempt to merge that protected replay into canonical `develop` was rejected by governance because the diff still lacked explicit same-owner issue/progress/review materialization for this continuation.
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-post-l042-followthrough-keepalive-verification.md`.
- `PENDING`: rerun guarded promote with this owner-linked evidence, merge into canonical `develop`, restart root daemon replay, and keep observing whether Freely now advances through select -> finish -> merge upward -> retire -> next task rather than stalling at the post-`L042` boundary.

## 2026-04-25 20:15 PDT Manager Exit-Contract Repair Prompt Narrowing

- `FAIL`: after `L042` keepalive was fixed, canonical `develop` daemon replay still exposed one narrower same-owner seam. Root runtime could now keep the live manager supervisor through post-cycle followthrough, but when a manager round exited `rc=0` without `manager-exit-contract.env`, repair selection downgraded correctly to `fresh_with_handoff` on `missing_resume_evidence` and then still rebuilt the full broad startup prompt.
- `FAIL`: the result was another empty-success manager round instead of bounded repair. Real runtime evidence showed repeated `manager_empty_success_cycle_detected details=missing_file`, `last_launch_kind: fresh_with_handoff`, and `last_rotation_reason: missing_resume_evidence` while `latest_manager_continuity_generated` stayed stale. This confirms the blocker is still the runtime middleman prompt contract, not scan task choice or role taxonomy.
- `PASS`: `build_prompt()` now narrows only this exact repair surface. When role truth is manager, `session-handoff.txt` says `rotation_reason=manager_exit_contract_repair`, `LAUNCH_KIND_SELECTED=fresh_with_handoff`, and `LAUNCH_ROTATION_REASON=missing_resume_evidence`, runtime bypasses the broad `start-lead-agent.sh` startup prompt and emits a bounded repair prompt that requires:
  - first read only `AGENTS.md`, `session-handoff.txt`, `live-status`, current scan json, and latest manager continuity
  - first write a new manager continuity
  - then write `manager-exit-contract.env`
  - avoid broad patrol, full milestones reread, or generic fleet survey before continuity/contract closeout
- `PASS`: the narrowed prompt keeps the existing `manager continuity 文件：\`...\`` contract so `materialize_required_manager_continuity_startup_stub()` and the existing continuity materialization path remain compatible.
- `PASS`: focused feature-local verification passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
  - `./bin/governance-check`
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-prompt-narrowing-verification.md`.
- `PENDING`: rerun guarded feature/premerge verification with the owner-linked evidence, merge into canonical `develop`, restart root `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and watch whether the next repair/fresh-with-handoff manager round now produces continuity + exit contract instead of looping on `manager_empty_success_cycle_detected`.

## 2026-04-25 20:58 PDT Manager Repair Handoff Preservation

- `FAIL`: root replay still exposed one more control-plane seam after prompt narrowing. `select_launch_kind()` correctly recognized `manager_exit_contract_repair` and downgraded to `fresh_with_handoff` on `missing_resume_evidence`, but the runtime main loop then overwrote `session-handoff.txt` with a generic rotation handoff before `build_prompt()` consumed it.
- `FAIL`: this meant the new bounded repair prompt was logically present but unreachable in the real loop. The bug was not task choice and not prompt text quality; it was that the runtime middleman erased its own repair signal between launch selection and prompt build.
- `PASS`: runtime now preserves an existing `manager_exit_contract_repair` or `worker_exit_contract_repair` handoff when `fresh_with_handoff` was chosen only because resume evidence is missing, so repair-specific prompt and directive logic still receive the intended handoff contract.
- `PASS`: the fix is intentionally narrow. Non-repair `fresh_with_handoff` rotations such as `context_compacted`, route-only, dirty-budget, and resume-streak paths still rewrite handoff through the generic writer.
- `PASS`: focused feature-local verification passed:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-missing-resume-evidence-preserves-repair-handoff`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
  - `./bin/governance-check`
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-manager-exit-contract-repair-handoff-preservation-verification.md`.
- `PENDING`: rerun protected `premerge-integration` verification, guarded promote into canonical `develop`, restart root daemon replay, and confirm the next repair/fresh-with-handoff manager round preserves repair handoff truth long enough to write continuity + exit contract and continue toward the overall autonomy loop.

## 2026-04-25 20:25 PDT Resume Incremental Output Evidence Verification

- `FAIL`: canonical `develop` replay advanced past the repaired `fresh_with_handoff` repair prompt, but the next `resume` cycle still returned `rc=0` without writing new continuity or `manager-exit-contract.env`; runtime accepted it anyway because `manager_cycle_has_effective_output_evidence()` trusted assistant output anywhere in the reused Codex session jsonl, including output from earlier cycles.
- `PASS`: Codex `resume` cycles now require effective output evidence at or after the current prompt boundary, so reused session history cannot satisfy the success check for a new empty manager round.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-resume-cycle-does-not-reuse-stale-output-evidence`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-empty-success-cycle-does-not-autoresume`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-missing-resume-evidence-preserves-repair-handoff`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-missing-continuity-autoresumes`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-fresh-with-handoff-prompt-narrowing`
- `PASS`: `./bin/governance-check`
- `PASS`: owner-linked verification for this continuation is now explicit in `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260425-runtime-daemon-self-loop-followthrough-resume-incremental-output-evidence-verification.md`.
- `PENDING`: promote this followthrough through protected premerge, merge into canonical `develop`, restart daemon replay, and verify Freely either writes a real post-repair manager continuity / worker handoff or re-enters `manager_empty_success_cycle_detected` instead of silently auto-resuming on stale session history.
