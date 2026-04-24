# Progress: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- runtime_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/operator-stop-delegated-continuation-boundary-20260424`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-operator-stop-delegated-continuation-boundary`
- updated_at: `2026-04-24 00:41 PDT`
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
- The remaining completion work is guarded promotion into `develop`, canonical `develop` self-host task completion, and temporary lane retirement.

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
- `PENDING`: replay this same-owner repair through fresh protected premerge and guarded `develop`, then rerun canonical `./bin/freely daemon start` until Freely both closes the retained cleanup lane and advances to the next scan-selected task.

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
- `PENDING`: replay this owner through fresh protected premerge, merge into canonical `develop`, restart `./bin/freely daemon start`, and verify cleanup governance falls back away from the empty Codex session file, retires the blocker cleanup lane, and advances to the next task.

## 2026-04-22 09:48 PDT Empty Repair Resume Target Followthrough

- `FAIL`: after the zero-byte session-file fix landed, canonical `develop` self-host replay advanced one step further but still forced `launch_kind=resume` for `manager_exit_contract_repair` even when `LAST_TOOL_RESUME_TARGET=""`; monitor preflight then failed immediately with `[ERROR] codex resume requires --tool-resume-target`, so daemon replay still could not reach the retained cleanup worker.
- `PASS`: `select_launch_kind()` now preserves exit-contract repair resumes only when the resolved pre-launch target is non-empty and the current tool still has verified resume evidence; otherwise the repair handoff downgrades to `fresh_with_handoff` with `missing_resume_evidence`.
- `PASS`: verified repair resumes still stay on `resume` when Codex has a real persisted rollout file for the recorded target, so this followthrough narrows only the empty-target case rather than regressing the earlier same-session repair contract.
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-avoids-initial-start`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-manager-repair-handoff-missing-resume-evidence-falls-back`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `PASS`: `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `PENDING`: promote through fresh protected premerge, merge into canonical `develop`, restart `./bin/freely daemon start`, and verify this owner finally clears cleanup followthrough, retires the temporary blocker lane, and continues to another task instead of stopping at monitor preflight.

## 2026-04-23 07:18 PDT Cleanup Followthrough Resume Extraction

- `FAIL`: canonical `develop` still reached `cleanup_governance`, but manager exit-contract replay could accept `EXIT_KIND=resume_manager` and relaunch manager before executing the already-selected cleanup followthrough, leaving continuity pinned to the same retained merged-lane closeout instead of retiring it and advancing patrol.
- `FAIL`: when that cleanup path failed during replay, runtime only degraded into generic invalid-resume behavior without persisting an exact manager blocker that explains cleanup-followthrough failure as the real seam.
- `PASS`: `manager_runtime_handle_exit_contract_after_ai_cycle()` now checks the active continuity for cleanup-followthrough intent before honoring `resume_manager`, runs that cleanup step first, and emits explicit `manager_exit_contract_cleanup_followthrough_begin` / `manager_exit_contract_cleanup_followthrough` receipts on success.
- `PASS`: when `run_cleanup_followthrough` fails on that path, runtime now writes a same-owner repair handoff, records `LAST_EXIT_REASON=manager_exit_contract_cleanup_followthrough_failed`, emits `manager_exit_contract_cleanup_followthrough_failed`, and returns `resume_invalid` instead of silently resuming broader patrol.
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
- `PENDING`: promote this same-owner repair through protected premerge and guarded `develop`, rerun canonical `./bin/freely daemon start`, and verify startup patrol now discards pre-stop continuity, picks from fresh scan JSON, and continues through lawful task closeout instead of re-entering the stale cleanup anchor.

## 2026-04-23 23:58 PDT Queue State Worker Prompt Launch Followthrough

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
- `PENDING`: absorb this daemon-preservation repair into canonical `develop`, rerun `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and continue supervision until Freely finishes a real task, merges upward, retires that lane, and autonomously selects the next task.
