# Progress: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- branch: `feature/manager-launch-state-consumed-truth-reconcile-20260324`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-consumed-truth-reconcile`
- issue_path: `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- session_refs:
  - {tool: codex, session_id: "019d220d-ce3c-7b42-a5b1-a5ed6b44b905", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T15-53-43-019d220d-ce3c-7b42-a5b1-a5ed6b44b905.jsonl", role: "closeout-writeback"}
  - {tool: codex, session_id: "019d220f-37e7-7212-9346-55708074bb27", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/24/rollout-2026-03-24T15-55-15-019d220f-37e7-7212-9346-55708074bb27.jsonl", role: "context_compacted_handoff_source"}
  - {tool: codex, session_id: "019d1e52-ccb2-7612-9538-87fd9df4eea5", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/23/rollout-2026-03-23T22-30-36-019d1e52-ccb2-7612-9538-87fd9df4eea5.jsonl", role: "context_compacted_handoff_source"}
  - {tool: codex, session_id: "019d1e4e-709f-7571-a958-b79828dc38f4", jsonl_path: "/Users/zhaoyu/.codex/sessions/2026/03/23/rollout-2026-03-23T22-25-50-019d1e4e-709f-7571-a958-b79828dc38f4.jsonl", role: "fresh_with_handoff_source"}
- summary: same-family canonical replay on 2026-03-26 confirms the reopened continuity parser gap is resolved on `develop`. `manager-worker-launch-state.env` and `freely status` now agree on latest continuity/prompt generated and consumed truth for the same round, so this issue closes as completed canonical writeback rather than staying in `in_verification`.
- verification:
  - `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `freely fleet-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `./bin/governance-check`

## 2026-03-26 Canonical Develop Recheck

- Replayed the same truth surfaces after merged same-family fixes landed on canonical `develop`:
  - `freely status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- Current canonical evidence:
  - `LAST_MANAGER_CONTINUITY_GENERATED == LAST_MANAGER_CONTINUITY_CONSUMED == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260326-064827.md`
  - `LAST_MANAGER_WORKER_PROMPTS_GENERATED == LAST_MANAGER_WORKER_PROMPTS_CONSUMED == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260326-064827-worker-i-20260318-1630-closeout-followthrough-codex.txt`
  - `freely status` surfaces the same generated/consumed truth
  - `test-freely-latest-manager-continuity-worker-consumption` passes
- Current judgement:
  - close `I-20260322-0445` as `completed`
  - keep future queue/frozen/reentry evolution in their own issue families rather than reopening this one

## 2026-03-27 Same-Family Regression Repair

- Canonical `develop` later exposed a same-family runtime regression during manager patrol:
  - latest generated continuity advanced through `manager-continuity-20260327-164618.md`
  - `latest_manager_continuity_consumed` stayed pinned to `manager-continuity-20260327-140745.md`
  - retained prompt `20260327-145324-worker-testing-evidence-closeout-codex.txt` remained unconsumed while the manager loop kept rewriting near-identical continuity
- Root cause:
  - `a125064` added a guard that blocks relaunch of merged clean worker worktrees
  - the guard treated a newly created but never-runtime-initialized clean worker worktree as retire-ready simply because its branch had no divergence from `develop`
  - the retained verification lane `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-feature-testing-evidence-closeout-governance` matched that shape, so runtime marked the prompt non-launchable and fell back to stale consumed truth
- Same-family repair:
  - narrow the retire-ready guard so it only applies after the target worker worktree has runtime history (`.freely/config.env`)
  - keep previously merged-and-clean initialized workers protected from pointless relaunch
  - add regression coverage for both initialized merged-clean workers and uninitialized clean bootstrap workers
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-merged-clean-worker-handoff-guard`
  - `bash docs/system/workspace/scripts/tests/test-freely-uninitialized-clean-worker-handoff-launchable`
  - `./bin/governance-check`
- Current judgement:
  - this is a same-family repair inside `I-20260322-0445` runtime launch/consumption scope, not a new milestone issue
  - after the repair, the retained prompt is launchable again and `latest_manager_continuity_file_for_project` resolves to the latest generated continuity instead of the stale consumed snapshot

## 2026-03-27 Semantic Loop Suspicion Signal

- Followthrough judgement:
  - the repaired bootstrap-launch regression explained the immediate patrol loop, but it also exposed a monitoring gap
  - existing watchdog signal surfaces covered restart storm / process churn and stalled AI, not manager-owned semantic repetition where continuity keeps changing timestamps while launchable worker progress stays unchanged
- Conservative implementation:
  - add a read-only semantic-loop detector to `freely live-status` / `freely fleet-status`
  - only suspect a loop when the latest manager continuity keeps repeating the same launchable worker prompt family for at least 3 consecutive continuity files, runtime still has zero active workers, and capacity is still available
  - do not auto-kill or auto-restart from this signal; it stays a supervision hint for manager/human judgement
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- Current judgement:
  - this remains same-family monitoring followthrough inside `I-20260322-0445`
  - the surfaced reason is `manager_continuity_rewrite_without_state_advance`
  - the signal is intentionally conservative so normal waiting states like active worker execution or zero available slots do not trigger it

## 2026-03-27 Consumed Continuity Resume Drift

- Followthrough judgement:
  - a later canonical `develop` replay showed a second same-family gap after cleanup followthrough had already converged
  - delegated backlog was absorbed, latest manager continuity advanced and was consumed, stale worker prompt references were cleared, but the still-running manager resumed into generic first-hop patrol instead of continuing from the consumed continuity's owner chain
- Why this is same-family:
  - this is not a new product surface and not a new milestone issue
  - it is another contract gap inside latest manager continuity consumption: after runtime proves which continuity is current truth, manager resume still needs to stay anchored to that truth until contradiction or fresh intake appears
- Repair direction:
  - inject a manager-only resume narrowing contract when `LAUNCH_KIND_SELECTED=resume`, no fresh delegated continuation is pending, and the latest consumed continuity still matches latest generated truth
  - scope the narrowing to manager-owned `completion_verification` / `cleanup_governance` closeout chains so ordinary discovery patrol is not suppressed
  - immediately fall back to full patrol when fresh delegated continuation appears, authoritative fleet truth contradicts the consumed continuity, or the restart point has already been closed
- Verification target:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`
  - regression rechecks around `live-status` / session rotation / prompt composition after the narrowing lands
- Current judgement:
  - absorb pre-brainstorm `C-20260327-1845-A` as supporting evidence into `I-20260322-0445`
  - keep this worktree scoped to the current runtime prompt/routing repair only; merge-gate lifecycle policy remains outside the scope of this branch
- Residual verification note:
  - `bash docs/system/workspace/scripts/tests/test-freely-session-rotation` still fails in both this worktree and pristine `develop`, at the existing `context_usage_threshold` subcase before the new manager-only narrowing is even consulted
  - treat that failure as a pre-existing unrelated gap unless a later reduced reproduction shows otherwise

## 2026-04-04 Same-Family Missing Run-Dir Guard

- Runtime supervision on canonical root `develop` stayed healthy after stale slot-switch cleanup, but patrol exposed a narrower same-family status/parser defect:
  - sibling worktrees without `.freely/run` caused `live-status` / `fleet-status` to leak `find: ... No such file or directory`
  - the failure path ran through the shared helper family for latest manager continuity, latest launchable continuity, semantic-loop repeat state, and latest prompt lookup
- Execution in this batch:
  - branch: `feature/runtime-status-missing-run-dir-guard-20260404-2120`
  - worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-2120-feature-runtime-status-missing-run-dir-guard`
  - runtime root supervised: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- Repair:
  - add `run_dir` existence guards before every `.freely/run` scan in `docs/system/workspace/scripts/runtime/freely`
  - add the same existence guard to `latest_cycle_log_for_project()` for the analogous missing `.freely/logs` path
  - add focused regression `docs/system/workspace/scripts/tests/test-freely-status-silences-missing-sibling-run-dir`
  - extend `docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface` so the semantic-loop monitoring path proves stderr stays empty with a sibling worktree lacking `.freely/run`
  - replay real-root `live-status` / `fleet-status` with the patched CLI to confirm stderr stays clean
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-status-silences-missing-sibling-run-dir`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
  - `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
  - `freely fleet-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- Current judgement:
  - absorb this as a same-family repair inside `I-20260322-0445`
  - do not widen `C-20260404-1545-A`; that candidate still owns the separate blocked-intake / websocket / slot-switch supervision contract question

## 2026-04-07 Same-Family Retire-Ready Recovery Guard Followthrough

- Followthrough judgement:
  - a later local replay exposed another same-family gap in the latest manager continuity consumption family
  - runtime already knew not to launch retire-ready merged-clean worker prompts from continuity parsing, but the expected-running recovery path still relaunched the same merged-clean worker worktree after supervisor exit
  - the same replay also showed the worker prompt dispatch metadata parser still assumed inline `key: value` headers, even though current manager prompts can emit multiline list-form headers such as `dispatch_priority:` followed by `- \`P0\``
- Why this is same-family:
  - both defects live inside the same manager continuity / worker prompt consumption contract already owned by `I-20260322-0445`
  - neither defect widens into tracked-root continuity-gap status truth or the broader research-only continuity fallback / authoritative replacement boundary
- Repair:
  - factor a shared `worker_project_is_retire_ready_merged_clean()` helper and reuse it from both prompt-launchability checks and `manager_runtime_recover_workers_if_needed()`
  - skip expected-running recovery for merged-clean worker worktrees that already have runtime history and are therefore genuinely retire-ready
  - extend `worker_prompt_dispatch_metadata_value()` so it accepts both inline headers and multiline list-form manager prompt headers
  - add focused regressions for retire-ready recovery skip and multiline prompt metadata parsing
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-multiline-dispatch-metadata`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-intent-metadata`
  - `./bin/governance-check`
- Current judgement:
  - absorb this as a same-family repair inside `I-20260322-0445`
  - do not widen `I-20260407-0215-A`; tracked-root status truth stays in its own bounded owner

## 2026-04-08 Worker Intent Fallback Absorption

- Followthrough judgement:
  - the stale mixed branch `feature/manager-continuity-gap-and-worker-recovery-guard-20260408` should not survive as its own owner or merge lane
  - after re-aligning that branch with current `develop`, only one same-family residual remained worth carrying forward
- What current `develop` had already absorbed:
  - retire-ready merged-clean worker recovery guard behavior
  - multiline list-form worker prompt dispatch metadata parsing
- Residual repair carried forward:
  - worker `live-status` and `fleet-status` should derive authoritative intent from manager continuity when the worker-local prompt file exists but lacks machine-readable intent headers
  - normalize the target worktree path before comparing it against the manager prompt's resolved/effective target so symlinked or relative worker paths do not suppress the fallback match
  - add focused regression `test-freely-live-status-worker-intent-falls-back-to-manager-continuity`
- Boundary decision:
  - absorb this residual into `I-20260322-0445` as a helper-level continuity/prompt consumption repair
  - do not split `manager-continuity-gap-and-worker-recovery-guard` into a new issue
  - do not widen `I-20260407-0215-A`; that owner remains on continuity-gap status truth rather than worker prompt intent consumption
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status-worker-intent-falls-back-to-manager-continuity`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-multiline-dispatch-metadata`
  - `./bin/governance-check`
- Current judgement:
  - retire the stale mixed lane as a standalone tracking concept
  - keep only this narrowed fallback repair as a same-family absorption lane

## 2026-04-24 Same-Family Plain Worker Prompt List Parsing Repair

- Followthrough judgement:
  - canonical `daemon start` replay after the worker closeout / recovery fixes showed the manager could now select the retained cleanup lane again and emit a fresh worker prompt
  - the new break was later in the chain: runtime did not launch that prompt because the latest continuity wrote `## Worker Prompts` as a plain bullet list, while the parser only considered `launched:` and `queue:` subsections launchable
  - evidence on canonical root showed `manager_exit_contract_delegate_workers` fired, but `manager-worker-launch-state.env` still reported `LAST_MANAGER_WORKER_PROMPTS_GENERATED=""` and `LAUNCHED_WORKER_PROMPTS="none"`
- Execution in this batch:
  - branch: `feature/manager-continuity-worker-prompt-plain-list-parser-20260424`
  - worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-continuity-worker-prompt-plain-list-parser`
  - retained worker prompt that should have launched: `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-025646-worker-runtime-cleanup-followthrough-resume-hygiene-codex.txt`
- Repair:
  - widen `manager_worker_prompt_paths_from_continuity_by_mode()` so plain bullets under `## Worker Prompts` are treated as launchable prompts
  - preserve frozen prompt exclusion and queue parsing semantics
  - extend `test-freely-manager-continuity-current-worker-prompt-parsing` with an explicit plain-list prompt
  - rewrite `test-freely-latest-manager-continuity-worker-consumption` to use the same plain-list continuity shape seen in canonical replay
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `./bin/governance-check`
- Current judgement:
  - keep this repair in `I-20260322-0445` as another same-family continuity/prompt consumption fix
  - after merge, canonical replay must prove the runtime actually launches the retained cleanup prompt and resumes autonomous closeout before this batch can be considered complete
