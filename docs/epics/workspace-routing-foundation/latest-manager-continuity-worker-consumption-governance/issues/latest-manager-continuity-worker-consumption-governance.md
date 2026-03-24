# Issue: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `latest-manager-continuity-worker-consumption-governance`
- issue-name: `latest-manager-continuity-worker-consumption-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/candidates.md#c-20260322-0445-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`

## Why

真实狗粮已经证明：

- `freely chat -> interruption resolution -> manager continuation` 已可达
- 主管可以产出合理的最新 worktree disposition
- 最新 worker prompt set 也能随最新 continuity 生成

但 runtime 仍可能继续消费更早一轮 delegated continuation。`manager-worker-launch-state.env` 也会停在旧 continuity，导致“主管已经给出更新监督结论，但 worker 没切到最新一轮执行输入”。

当前缺的不是新的 triage 语义，而是一个更硬的 runtime contract：

- latest manager continuity generated
- latest worker prompt set generated
- latest continuity / prompt set consumed by worker launch or reentry

## Scope

1. 定义 manager worker launch state 中 generated/consumed 的 canonical 字段。
2. 让 manager watchdog 在主管已运行时也持续尝试消费最新 continuity，而不是只在某些恢复路径才触发。
3. 让 worker launch / local reentry 始终以最新 continuity 派生的 prompt set 为准，而不是沿用旧 consumed marker。
4. 把这层 generated/consumed truth 暴露到 baseline/live status。
5. 补脚本级 integration tests，覆盖：
   - stale launch-state -> latest continuity consumption
   - manager watchdog already-running path 也会触发最新 continuity 消费
6. worker prompt contract 必须保持 runtime-launchable：
   - manager handoff 默认写 machine-readable `Worktree:` / `Branch:` header
   - runtime 在兼容期内也要能解析当前自然语言句式 `You are the worker for ... in ...`
7. 若同一 continuity 的 prompt 曾被记录为 consumed，但对应 worker 当前并未运行，runtime 必须把它视为 stale consumed state，并允许重新 launch / reentry，而不是要求先生成一轮新的 continuity。
8. 当 delegated continuation 已被当前活跃 prompt 吸收时，runtime 必须在 cycle completion 之前就把 consumed truth 写入 session state / live-status，并从实时 pending 视图中剔除这些 ids；但若当前 AI 已退出，这些 ids 必须重新回到 pending 视图，供 recovery 继续接管。

## Acceptance

- 新 continuity 生成后，即使主管 supervisor 已在运行，watchdog 也会尝试消费最新 continuity。
- `manager-worker-launch-state.env` 记录：
  - latest continuity generated
  - latest continuity consumed
  - latest worker prompt set generated
  - latest worker prompt set consumed
- 若 worker 已活跃，reentry 走最新 prompt；若 worker 未运行，launch 走最新 prompt。
- 若 worker 已停止，但当前 continuity / prompt set 仍是最新真相，runtime 会忽略 stale consumed marker 并重新 launch。
- 若 delegated continuation 已进入当前活跃 prompt，`live-status` 会立刻显示 consumed ids，并且不会再把同一批 ids 同时显示为 pending；当前 AI 停止后，这些 ids 会重新回到 pending 视图。
- 若 latest manager continuity 把 lane 明确放进 `Frozen Queue` / `desired-frozen`，runtime 不会再把该 prompt 计入 launchable generated/consumed inventory，也不会因 stale-consumed 或 worker local `DESIRED_RUNTIME_STATE=running` 而把该 lane 自动 relaunch / recovery。
- 若旧 launch-state csv 里还残留同一 continuity 下已被冻结的 prompt，下一轮 reconcile 会先按当前 continuity 的 launchable prompt set 清掉这些 stale frozen entries，再决定是否对仍 launchable 的 prompt 做 relaunch。
- `baseline-status` / `live-status` 能显示上述 generated/consumed truth。
- regression tests 覆盖：
  - stale continuity state 被更新到最新 continuity
  - `ensure_manager_once` 在 supervisor 已运行时仍会触发最新 continuity 消费
  - frozen-only prompt 不进入 launch/relaunch inventory
  - same-continuity stale frozen prompt 会从 launch-state consumed/launched csv 中被清掉
  - manager recovery 不会复活 latest continuity 已冻结的 worker lane

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-natural-language-contract-compat`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
- `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `./bin/governance-check`

## Next

- 2026-03-24 latest canonical `develop` truth continued to move forward after the earlier `033747` queued snapshot and still did not reproduce a repo-side implementation gap. At `2026-03-24T12:15:17Z`, `live-status` and `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env` both align on continuity `20260324-034106`, with `latest_manager_worker_prompts_generated` and `latest_manager_worker_prompts_consumed` both set to `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt`, `queued_worker_prompts=none`, and `active_running_worker_count=1`.
- That refreshed surface tightens the same conclusion rather than reopening scope: the earlier `20260324-032208` / `20260324-033747` drift evidence was a time-sliced protected-environment snapshot while manager/worker state was still moving, not a fresh repo bug inside `docs/system/workspace/scripts/runtime/freely`.
- `fleet-status` at the same time still shows only one canonical same-family active worker lane for this issue family, while the separate stale-batch followthrough lane remains outside this issue's acceptance truth. The stale-batch lane is still owned by `C-20260322-1801-B` / runtime recovery and must not be used to reopen `I-20260322-0445`.
- Worker-side scope therefore stays unchanged: keep this feature tree as verification-only writeback, leave `I-20260322-0445` in `in_verification`, and hand canonical completion / cleanup judgement back to the manager-owned `develop` acceptance path once it records the final post-merge closeout artifact.
- 2026-03-24 fresh-session continuity refresh still did not reproduce a new repo-side implementation gap. The earlier drift remained a time-sliced `develop` acceptance snapshot from manager continuity `20260324-032208`; current truth at `2026-03-24T10:42Z` has `live-status` and `.freely/run/manager-worker-launch-state.env` aligned on continuity `20260324-033747`, with `latest_manager_worker_prompts_generated=/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt`, `latest_manager_worker_prompts_consumed=none`, `queued_worker_prompts` pointing to that same prompt, and `active_running_worker_count=2`.
- That newer surface means protected-environment acceptance is still actively in flight rather than closed: manager has refreshed the latest continuity, preserved the same canonical followthrough worker prompt, and kept worker slots saturated while the active same-family worker is still running.
- `fleet-status` still reports the dirty stale-batch worker `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-pre-test-merge-lifecycle-management-followthrough` as running with `launch=fresh_with_handoff`, but that lane remains separately owned by `C-20260322-1801-B` / runtime recovery. It is not new evidence that `I-20260322-0445` still misrecords latest continuity consumption truth.
- 2026-03-24 latest worker continuation absorbed one more runtime gap inside this same issue family: continuity parser previously treated every `worker-prompts/*.txt` path in manager continuity as launchable inventory, so prompts listed only under `Frozen Queue` / `desired-frozen` could stay in launched state and be relaunched via stale-consumed or expected-running recovery. Runtime now filters those prompts out of launchable generated/consumed/queued state, purges stale frozen prompt remnants from same-continuity launch-state csv during reconcile, and skips manager auto-recovery for worktrees explicitly frozen by the latest continuity.
- Canonical closeout remains on the same issue family: this branch is `merge-ready` for the absorbed frozen-queue runtime fix plus verification writeback, but not `delete-ready`.
- Remaining blocker is unchanged: one real post-merge `develop` acceptance via `freely chat` in the application-native real environment, confirming workers consume the newest manager continuity round and that active pending vs consumed delegated ids stay aligned.
- Until that acceptance is recorded, keep this issue in `in_verification`, keep this feature tree scoped to doc-only closeout, and do not reopen implementation or research scope from this branch.
- 2026-03-24 the latest fresh session still stayed on `lead-agent -> constitution-guard -> laws-enforcer -> context-source-skill`, kept this same delegated continuation worker lane as the top pool, and selected the same in-session route: `source_class=continuation`, `route_kind=dev_loop`, `target_skill=dev-loop-execution`, `selected_tool=codex`.
- 2026-03-24 the worker reran the focused verification/writeback checks and all checks stayed green; `bash docs/system/workspace/scripts/tests/test-freely-live-status` passed, `./bin/governance-check` still reports only the same 10 legacy pre-brainstorm naming warnings, and `git diff --name-only` still only lists the same four issue-owned continuity docs.
- This issue therefore remains `in_verification` with unchanged remaining scope: one real post-merge `develop` acceptance.
- 2026-03-23 current fresh session first absorbed the queued delegated continuation handoff set (`20260323-224831`, `20260323-224818`, `20260323-224244`) and confirmed those intake ids still belonged to this same `I-20260322-0445` worker lane rather than any new discovery, IBM reroute, or project-level supervisor task.
- 2026-03-23 first-hop closure after that absorption still stayed on `source_class=continuation`, `route_kind=dev_loop`, `target_skill=dev-loop-execution`, and `selected_tool=codex`, so the correct action remained in-session verification work inside the current feature worktree.
- 2026-03-23 the worker reran the same targeted verification suite again:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `./bin/governance-check`
- 2026-03-23 no new implementation gap surfaced in that rerun either; this lane still remains verification-only and still needs only the protected-environment post-merge `develop` acceptance.
- 2026-03-23 fresh-session reentry after the recorded `context_compacted` handoff still followed the same first-hop closure in this feature worktree: the intake remained `source_class=continuation`, `route_kind=dev_loop`, `target_skill=dev-loop-execution`, and `selected_tool=codex`, so this lane continued in-session instead of handing execution back to runtime.
- 2026-03-23 that fresh session reran the full targeted verification suite inside the declared worker write scope:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `./bin/governance-check`
- 2026-03-23 no new implementation gap surfaced in that rerun; the lane remains verification-only and still needs only the protected-environment post-merge `develop` acceptance.
- 2026-03-23 latest worker continuation repeated the full first-hop closure in this feature worktree and stayed on the same route: `constitution-guard` kept execution in the current feature worktree, `laws-enforcer` kept the intake classified as a stable continuation, `context-source-skill` stayed on `source_class=continuation` / `route_kind=dev_loop`, and `selected_tool=codex` matched the active tool so the lane continued in-session instead of stopping at a handoff-only prompt.
- 2026-03-23 targeted verification was rerun again after that closure:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
  - `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
  - `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
  - `./bin/governance-check`
- 2026-03-23 runtime truth-source recheck stayed aligned with acceptance: prompt build still persists `LAST_DELEGATED_CONTINUATION_CONSUMED_IDS`, active pending views still suppress those ids only while the same AI pid is alive, and the ids still return to pending once the active prompt exits.
- 2026-03-23 worker continuation re-ran the full targeted verification suite in the feature worktree and confirmed the scope is still verification-only; no new implementation gap surfaced.
- 2026-03-23 lead-agent first-hop closure revalidated the route as `continuation -> dev_loop`; because the selected tool remained `codex`, the worker continued in-session instead of emitting a handoff-only `next_prompt`.
- 2026-03-23 second-hop `dev-loop-execution` rechecked the runtime/test truth source for active-prompt visibility and reran the full verification suite; all checks stayed green, so the worktree remains limited to verification writeback rather than reopening implementation scope.
- 2026-03-23 runtime truth-source inspection confirmed the active-prompt visibility contract now matches acceptance: prompt build persists `last_consumed_delegated_continuation_ids`, active pending views suppress those same ids while the AI pid is still alive, and `live-status` shows them as pending again once the AI stops.
- 2026-03-23 a follow-up worker continuation reran the complete targeted suite from a clean worktree and reconfirmed the same route/result: `continuation -> dev_loop -> codex`, no new code delta inside the declared write scope, and the only remaining gap is protected-environment post-merge acceptance.
- 当前 pre-merge verification 已完成，并补上 delegated continuation active-prompt visibility 回归，确认 consumed ids 会在 AI 活跃期间立刻进入 live-status、停止后重新回到 pending。
- 仍需 merge 后在 `develop` 上做一次真实 `freely chat` post-merge acceptance，确认最新 manager continuity 会被 worker runtime 消费，且 active pending 视图与 consumed truth 保持一致。
