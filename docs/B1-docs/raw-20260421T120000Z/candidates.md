# Candidates - 20260421-1200--runtime-daemon-self-loop-followthrough

## Context
- Source brainstorm: `docs/B1-docs/raw-20260421T120000Z/brainstorms.md`
- Status: `promoted`
- Route: `materialize-daemon-self-loop-followthrough-owner-and-replay-through-guarded-develop`

## Candidates

### C-20260421T120000Z-A: legacy issue
- candidate_format_version: `v2`
- title: `Runtime daemon self-loop followthrough governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260421T120000Z-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- problem: Dogfooding proved a remaining runtime-control blocker: daemon-mode Freely could stop self-looping after a patrol round because an unexpected `TERM` was recorded as `operator_stop`, and a lone dispatcher/watchdog residue could also falsely block the next `start` or `daemon start`.
- followthrough_update: Guarded replay then exposed two same-owner seams on canonical `develop`: runtime could not consume the current `## Worker Delegation` continuity shape into worker launches, and after that repair it could still auto-recover a `merged-clean` blocker worktree instead of routing it to cleanup followthrough retirement.
- followthrough_update_2: The same autonomous-loop owner then exposed one more control-plane seam: manager and worker AI rounds could exit without a machine-checkable closeout contract, so runtime had no reliable way to distinguish `stop_ai`, `resume_manager`, `delegate_workers`, `worker_done`, `worker_blocked`, and `worker_handoff_needed`, nor to force a precise same-session repair when the artifact was missing.
- followthrough_update_3: Canonical `develop` replay then exposed a narrower cleanup-handoff retirement seam: manager could select a real cleanup-governance task and materialize a lawful worker prompt, but the worker worktree was still auto-settled as `retire_ready_merged_worker` before it could execute the external cleanup surfaces named in that prompt.
- followthrough_update_4: The cleanup-handoff seam turned out to be more specific on live runtime truth: the worker worktree often had no local `prompt-*.txt`, and the authoritative cleanup prompt only remained reachable via `worker-verification-contract.env` `SOURCE_PROMPT_FILE`, so merged-lane settle/reclaim had to fall back to contract truth instead of assuming a local prompt artifact existed.
- followthrough_update_5: A second live replay then showed the worker could also generate a fresh local reentry prompt that was not the authoritative cleanup handoff prompt; merged-lane settle/reclaim therefore had to prefer `SOURCE_PROMPT_FILE` over any later worker-local bootstrap prompt.
- followthrough_update_6: Canonical `develop` replay then exposed one more bounded recovery seam: `monitor-ai-cli` treated Codex `ERROR: Reconnecting... x/5` as an immediate runtime failure, so pure reconnect evidence could trigger cross-tool switching before the tool exhausted its own retry loop, and one exhausted fallback episode could leave the project pinned on the last fallback tool instead of returning to the original tool for the next bounded retry.
- followthrough_update_7: The same network-recovery owner then exposed a narrower Codex-auth seam on live worker truth: an OAuth refresh transport failure (`error sending request for url (https://auth.openai.com/oauth/token)`) was still falling through as generic `tool_runtime_failure` instead of the bounded `execution_network_*` path, so real device / wifi / hotspot instability could be misclassified before autonomous recovery had a chance to continue.
- followthrough_update_8: Latest canonical `develop` replay then exposed a proxy-resolution seam rather than a real network outage: project config carried `FREELY_NETWORK_PROXY_MODE=explicit` with empty proxy values, global config still held a valid explicit proxy, and resolver precedence treated the empty project explicit block as authoritative, so manager repeatedly stalled on `proxy_config_invalid` before self-work could resume.
- followthrough_update_9: After the fleet narrowed to one retained dirty blocker lane, canonical replay still exposed two same-owner launchability seams: project worktree summary could throw a broken pipe during daemon patrol, and manager could legally choose a worker prompt from scan/continuity but fail to materialize a missing sibling worktree or wrongly retire a fresh merged-tip edit lane whose authoritative prompt still carried active `edit` ownership.
- followthrough_update_10: Fresh restart observation then exposed one more same-owner patrol-freshness seam: `daemon stop` only wrote `operator_daemon_stop`, but the manager continuity staleness boundary refreshed only for plain `operator_stop`, so startup patrol could still reuse pre-stop cleanup continuity instead of the new scan-selected queue.
- followthrough_update_11: Fresh canonical replay then exposed a narrower handoff-parser seam: manager could write cleanup followthrough in the current `## Queue State` shape with `worker_prompts:`, but runtime still parsed that continuity as prompt-empty, so `delegate_workers` exited cleanly while no worker was ever queued or launched.
- why_now:
  - this blocker prevents Freely from autonomously selecting, finishing, and closing tasks on canonical `develop`
  - the fix is already implemented and focused regressions are green in the blocker worktree, but guarded develop promotion still needs lawful owner evidence
  - the newest repair must preserve cleanup-handoff workers that carry full verification metadata plus external cleanup scope, otherwise canonical `develop` still cannot finish even its first real selected task
  - the final acceptance surface is not "daemon stayed up once" but "Freely continued self-work end-to-end and then moved to the next task"
- acceptance_criteria:
  - `start` and `daemon start` no longer reject because of orphaned watchdog/dispatcher residue when no authoritative supervisor exists
  - daemon supervisor ignores unexpected `TERM` without `stop.marker` and still honors explicit daemon stop
  - runtime consumes current `## Worker Delegation` continuity into worker launches instead of stalling after manager selection
  - `merged-clean` / `retire-ready` blocker worktrees are settled toward cleanup followthrough retirement rather than being auto-recovered as edit workers
  - cleanup-handoff workers that still need to reconcile external owner surfaces are not reclaimed or auto-settled merely because their branch is already merged into `develop`
  - every manager / worker AI cycle now leaves exactly one valid exit contract artifact, or runtime reuses the precise resume target to repair that artifact before doing broader work
  - reconnect-in-progress output such as `ERROR: Reconnecting... x/5` stays on the bounded execution-network retry path until the current tool actually exits, instead of triggering monitor-level live kill or immediate cross-tool switch
  - once one bounded cross-tool recovery episode exhausts every configured fallback, Freely restores the original tool selection for the next retry instead of remaining pinned to the last failed fallback
  - Codex OAuth refresh request-send failures are classified onto the same bounded `execution_network_*` path as other verified transport failures, while auth-denied noise such as OAuth `401 Unauthorized` stays off the network-recovery path
  - project-level `explicit` proxy mode no longer turns into a false `proxy_config_invalid` merely because its proxy value fields are blank while global explicit proxy values are still present; explicit config resolves by field override, not by empty-value shadowing
  - daemon patrol no longer emits a broken-pipe failure while computing project worktree summary for live-status / startup followthrough
  - manager launch/exit-contract validation can treat a prompt-targeted missing sibling worktree as materializable runtime truth, and a merged-tip lane with an authoritative `edit` prompt is not misclassified as retire-ready cleanup residue
  - explicit `daemon stop` refreshes the same startup freshness boundary used by patrol continuity filtering, so post-stop startup patrol cannot reuse pre-stop manager continuity as current queue truth
  - current `## Queue State` continuity with `worker_prompts:` remains launchable runtime truth, so manager `delegate_workers` cannot silently drop the selected worker handoff on canonical replay
  - guarded `feature/* -> test-pre-merge-* -> develop` replay succeeds with concrete owner evidence
  - on canonical `develop`, `freely daemon start` autonomously selects at least one task, completes it to the current-project success standard, closes the temporary worktree, and continues to another task
- promotion_gate:
  - keep scope on the runtime self-loop blocker and its bounded governance followthrough only
  - do not widen into general scan/task-picking redesign in this owner
  - require final develop-side self-host acceptance before declaring completion
- open_questions:
  - whether future start-mode UI affordances should expose scan item ids directly now that runtime selection can be parameterized
  - whether unexpected daemon signals need a broader observability taxonomy later
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The field blocker is runtime-control-plane specific. The smallest truthful owner is a followthrough lane that repairs orphan precheck truth, ignores unexpected daemon TERM without stop intent, and proves canonical develop self-host continuity.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260421T120000Z-A` remains the canonical owner for the daemon self-loop followthrough, the guarded-replay-discovered continuity/retirement seams, final self-host acceptance on `develop`, and retirement of the temporary blocker worktree and test-pre-merge branch.
- revisit_trigger: Re-open only if canonical `develop` still falls out of autonomous looping after this bounded repair, or if another blocker shows the self-loop boundary needs a larger dedicated runtime owner.
- decision_reason: `This is a concrete post-architecture runtime blocker with already-bounded code changes. A narrow followthrough owner is safer and more truthful than reopening the broader runtime architecture lanes.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
