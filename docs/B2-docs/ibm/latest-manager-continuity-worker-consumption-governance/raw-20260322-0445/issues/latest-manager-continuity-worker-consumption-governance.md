# Issue: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `latest-manager-continuity-worker-consumption-governance`
- issue-name: `latest-manager-continuity-worker-consumption-governance`
- pre_tests_path: docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/raw-20260322-0445/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/raw-20260322-0445/code-reviews
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322T071500Z/candidates.md#c-20260322-0445-a`
- source_brainstorm: `docs/B1-docs/raw-20260322T071500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/ibm/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
  - `docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`

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
- `docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-natural-language-contract-compat`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-multiline-dispatch-metadata`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
- `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`
- `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-multiline-dispatch-metadata`
- `./bin/governance-check`
- `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/code-reviews/20260420-latest-manager-continuity-worker-consumption-delegated-freshness-verification.md`

## Verification Summary

- The same-family reopen condition from 2026-03-26 is no longer present on canonical `develop`.
- Current canonical runtime truth now shows aligned continuity and prompt consumption for the same round:
  - `LAST_MANAGER_CONTINUITY_GENERATED == LAST_MANAGER_CONTINUITY_CONSUMED == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260326-064827.md`
  - `LAST_MANAGER_WORKER_PROMPTS_GENERATED == LAST_MANAGER_WORKER_PROMPTS_CONSUMED == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260326-064827-worker-i-20260318-1630-closeout-followthrough-codex.txt`
- `freely status --project /Users/zhaoyu/Downloads/code/my-freely/freely` now surfaces the same generated/consumed truth in the canonical status surface.
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption` passes on canonical `develop`, proving the current `## Worker Prompts` / queue parsing contract is consumed correctly while the supervisor is already running.
- The repair is already present in `develop` through same-family commit `c80cb34` (`fix: reconcile latest manager continuity prompt parsing`), so this issue should close as canonical writeback, not reopen as new implementation work.

## 2026-04-04 Same-Family Missing Run-Dir Guard Repair

- Canonical root runtime supervision on `develop` exposed another same-family parser/status regression:
  - `freely live-status` and `freely fleet-status` stayed functionally usable
  - but shared continuity/prompt lookup helpers leaked `find: .../.freely/run: No such file or directory` when sibling worktrees existed without initialized `.freely/run`
  - the noise came from the same helper family that resolves latest continuity, latest launchable continuity, semantic-loop evidence, and latest prompt truth across worktrees
- Narrow repair:
  - guard every helper that scans `.freely/run` with an explicit `[[ -d "$run_dir" ]]` check before invoking `find`
  - guard the sibling cycle-log helper the same way for the analogous missing `.freely/logs` shape
  - preserve the existing empty-result semantics so status surfaces stay truthful and quiet when a sibling worktree has never initialized runtime state
  - add a focused regression that reproduces a sibling worktree lacking `.freely/run` and proves both `live-status` and `fleet-status` no longer leak stderr
  - extend the semantic-loop status regression so the shared monitoring path also stays quiet when another sibling worktree lacks runtime state
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-status-silences-missing-sibling-run-dir`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-live-status`
  - `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- Current judgement:
  - this remains inside `I-20260322-0445` because the defect sits on the same shared continuity/prompt parser helpers already owned by latest generated/consumed truth
  - it does not widen the issue into the separate blocked-intake/websocket supervision contract family

## 2026-04-08 Worker Intent Fallback Absorption

- Review of stale mixed branch `feature/manager-continuity-gap-and-worker-recovery-guard-20260408` confirmed it should not materialize as its own issue or merge lane.
- Current `develop` had already absorbed that branch's retire-ready merged-clean recovery guard and multiline dispatch-metadata parsing repairs through the same-family `I-20260322-0445` surface.
- The only residual delta worth carrying forward is a worker status fallback: when the worker-local prompt lacks machine-readable intent metadata, `live-status` and `fleet-status` should resolve the authoritative worker prompt from manager continuity and surface intent from that authoritative prompt instead of reporting `none`.
- The fallback also normalizes the target worktree path before matching against the manager prompt's resolved target so real-path worker directories still match continuity-authored worktree headers.
- Decision:
  - keep this residual fallback in the same latest-continuity / worker-prompt consumption family
  - do not split a new `manager-continuity-gap-and-worker-recovery-guard` issue
  - do not widen `I-20260407-0215-A`, whose bounded scope stays on continuity-gap status truth rather than worker prompt intent consumption

## 2026-04-20 Delegated Continuation Freshness Guard

- Real dogfood on canonical `develop` exposed another same-family prompt-consumption gap after runtime startup became healthy:
  - the manager prompt still replayed delegated continuation items that were older than the latest generated manager continuity
  - those delegated items also remained duplicated in the front-door `Human chat intake queue`
  - a fresh governance interruption about `成功标准` therefore got bundled behind an older `runtime-lifecycle-validation` continuation and the manager kept following the stale lane instead of routing the new work
- Why this remains same-family:
  - the defect still sits on the latest continuity / delegated prompt-consumption seam already owned by `I-20260322-0445`
  - no new interruption taxonomy is required; the missing contract is freshness about which delegated handoffs still belong to the current supervision round
- Narrow repair:
  - front-door `Human chat intake queue` excludes `STATUS="delegated"` items, because they have already left the claim queue and should not be re-presented as untriaged chat
  - local delegated continuation prompt injection only includes handoffs newer than the latest generated manager continuity for the same project
  - older delegated items remain durable intake history until explicitly absorbed or re-claimed, but they no longer hijack the current manager lane by default
- Success criteria:
  - fresh delegated governance interruptions enter the current manager prompt without being bundled behind older continuation backlog
  - delegated items older than the latest manager continuity do not auto-reenter the current manager lane unless a newer continuity or fresh claim carries them forward
  - front-door intake queue only shows not-yet-delegated chat items
  - a real replay can route the new governance task first instead of silently reusing the older runtime-lifecycle-validation lane
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-filters-stale-delegated-continuations`
  - `bash docs/system/workspace/scripts/tests/test-freely-human-chat-intake`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-consumed-continuity-resume-focus`

## 2026-04-24 Same-Family Plain Worker Prompt List Parsing Repair

- Canonical replay after the cleanup-followthrough chain repairs exposed another same-family launch-consumption gap:
  - the manager produced a fresh continuity and worker prompt for the retained cleanup lane
  - the continuity wrote that prompt under `## Worker Prompts` as a plain bullet list
  - runtime launch-state consumption only treated `launched:` and `queue:` subsections as launchable
  - result: `manager_exit_contract_delegate_workers` fired, but `LAST_MANAGER_WORKER_PROMPTS_GENERATED` stayed empty and the retained cleanup worker never launched
- Why this is same-family:
  - the defect sits exactly on the latest continuity -> worker prompt consumption seam already owned by `I-20260322-0445`
  - no new task-source taxonomy, recovery authority, or supervisor role split is needed
  - runtime remains the launcher; manager/worker AI still only materialize artifacts
- Narrow repair:
  - treat plain bullets directly under `## Worker Prompts` as launchable prompts, the same as `launched:` / `queue:` entries
  - keep `Frozen Queue` / frozen-only prompts non-launchable
  - update the parser regression and latest-continuity consumption regression so the current continuity format is exercised explicitly
- Verification:
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
  - `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
  - `./bin/governance-check`
- Current judgement:
  - absorb this as a same-family repair inside `I-20260322-0445`
  - do not split a new lifecycle, because the broken seam is still continuity prompt consumption rather than a new runtime architecture owner

## Retirement Audit

- audit_date: `2026-03-24`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-consumed-truth-reconcile`
- worktree_state: `dirty`
- classification: `retained-with-reason`
- cleanup_gate: `retained-with-reason`
- why_not_verified_retirable:
  - current worktree still owns canonical closeout writeback for this issue family; writeback must be absorbed through the develop-facing path before branch/worktree cleanup
  - current closeout lane itself is dirty because this writeback is still uncommitted; it cannot truthfully claim cleanup-readiness yet
  - same-family worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-active-worker-launch-state-reconcile` remains active, so this issue family is completed but not yet fully retired as a fleet unit
  - separate worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-test-pre-merge-lifecycle-management-followthrough` remains `runtime-owned` recovery and must stay outside this issue's cleanup claim
- local_branch_disposition: `retained-with-reason`
- local_branch_reason: keep the branch/worktree until canonical issue-family writeback is absorbed and supervisor/runtime runs the normal cleanup followthrough; do not delete from this worker round
- remote_branch_disposition: `not_checked`
- remote_branch_reason: remote cleanup is outside this worker's closeout-writeback scope
- revisit_trigger:
  - current docs-only closeout writeback is absorbed by the develop-facing path
  - supervisor/runtime re-enters cleanup followthrough for this worktree
