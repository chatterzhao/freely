# Candidates - 20260420-1130--manager-task-source-scan-replan-boundary

- Source brainstorm: `docs/pre-brainstorms/20260420-1130--manager-task-source-scan-replan-boundary/brainstorms.md`

### C-20260420-1130-A

- candidate_format_version: `v2`
- title: `Manager task-source scan idle/replan boundary governance`
- source_class: `discovery`
- route_kind: `ibm`
- phase_state: `todo_ibm`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `Freely manager needs a structured way to find work after startup and after closeout, but the current patrol layer lacks a runtime-owned trigger contract. Without it, stale delegated continuation can hijack the lane, while broad patrol can also re-scan too often and derail in-flight worker continuity.`
- why_now:
  - recent self-host replay shows manager can miss valid follow-on work when stale delegated handoff stays active
  - once milestone patrol seeds are exposed, runtime still needs a clear answer for when scan should regenerate versus when existing continuity should remain primary
  - the user explicitly requires both capabilities at once: startup autonomous patrol and interruption-driven task completion
- proposed_scope:
  - freeze task-source scan as an idle/replan step rather than an every-cycle step
  - define the first bounded trigger set for regeneration and suppression
  - materialize a machine-readable scan json and scan-state artifact for manager patrol
  - keep raw durable family naming (`human interruption`, `external issue`) separate from standing surfaces (`milestone`, `pre-brainstorm`, `progress`, `recovery`, `delegated continuation`)
- non_goals:
  - shipping full GitHub/Gitee provider automation in this owner
  - collapsing all standing surfaces into a new raw-source family schema
  - broad runtime/fleet redesign outside the manager patrol trigger seam
- acceptance_criteria:
  - a new pre-brainstorm freezes the idle/replan trigger boundary and the distrust-stale-state rule
  - runtime regenerates `manager-task-source-scan-latest.json` only on bounded idle/replan triggers
  - prompt-time broad patrol is suppressed while active workers are stably running
  - prompt-time patrol seed remains available for idle manager rounds, using existing scan json when no new regeneration is needed
  - scan json records trigger reason plus per-surface reconcile/trust hints for milestone / pre-brainstorm / progress patrol seeds
  - focused tests prove startup generation, active-worker suppression, idle-after-continuity regeneration, stale delegated intake filtering, and unresolved pre-brainstorm/progress surfacing
- promotion_gate:
  - keep the first patrol surface set bounded to `human interruption`, delegated continuation, active milestone queue, active pre-brainstorm queue, and active progress queue
  - do not widen this owner into external issue provider automation, generic watchdog redesign, or project-wide fleet closure
  - prove the runtime slice with focused startup/prompt/launch regressions before considering IBM materialization
- open_questions:
  - whether `recovery` should join the machine-readable patrol snapshot or stay ad hoc until a narrower owner absorbs it
  - whether the same stale-pid protection should be frozen as an explicit cross-watcher contract for `ensure-interruption-dispatch`, rather than only traveling as a mirrored bootstrap guard in the current runtime patch
- acceptance_reviews:
  - reviewer: `codex-first-hop-audit`
    verdict: `still_pre_brainstorm`
    note: `Current repo truth keeps the lane inside candidate-owned boundary freeze. The runtime/script/test batch now proves the idle/replan scan seam, launch-time prompt consumption, and the narrow stale-pid bootstrap guard needed for startup re-entry, but the owner is still not IBM-ready because its patrol contract and provider/follow-on boundaries remain candidate-level only.`
  - reviewer: `codex-continuity-refresh-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `HEAD already contains the bounded runtime/doc/test checkpoint series for this patrol-scan seam, and the current replay reran the focused patrol regressions plus runtime syntax check without reopening implementation. Current worktree truth no longer justifies another in-scope implementation checkpoint; the remaining action is candidate-side continuity/evidence refresh and a clean hold until a new bounded delta appears.`
  - reviewer: `codex-fresh-session-continuity-refresh-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `A fresh session resumed from the `019dabd6-26d2-7952-979e-59315886567e` context-compacted handoff and revalidated the narrow patrol seam with passing milestone-seed, idle-regeneration, active-worker suppression, stale-delegated-intake, and runtime syntax checks. Current repo truth stays narrowly dirty only in candidate-side continuity writeback, so this owner remains in pre-brainstorm without reopening implementation or forcing a new checkpoint commit.`
  - reviewer: `codex-handoff-reconcile-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabd9-6821-7860-85f2-1e69f20f4bac` context-compacted handoff, reran the same focused patrol regressions plus `bash -n docs/system/workspace/scripts/runtime/freely`, and confirmed the bounded patrol-scan slice is still owned entirely by this candidate. Current repo truth already started with a narrow candidate-owned continuity diff, while the older `I-20260326-1835` manager/source-patrol owner is already completed and does not absorb the newer idle/replan scan-trigger seam. The route therefore stays in pre-brainstorm, and any follow-on checkpoint remains limited to these continuity artifacts only.`
  - reviewer: `codex-fresh-session-reconcile-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the `019dabe0-2381-7aa1-9636-c3b242e02904` context-compacted handoff, reconfirmed the milestone candidate placement, and reran the focused patrol checks for milestone-seed inclusion, idle regeneration, active-worker suppression, stale delegated continuation filtering, plus `bash -n docs/system/workspace/scripts/runtime/freely`. All checks still pass without reopening implementation, so the owner remains a bounded pre-brainstorm candidate and the only remaining hygiene delta is a two-file continuity/doc checkpoint if the worktree needs to return to clean hold.`
  - reviewer: `codex-fresh-session-reconcile-2026-04-20-second-rotation`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabe3-8e3a-7ad1-a5a9-69e57689b9b3` context-compacted handoff, rechecked milestone placement and current dirty-tree ownership, and reran the same focused patrol regressions plus `bash -n docs/system/workspace/scripts/runtime/freely`. Repo truth still shows only a two-file candidate-owned continuity batch, so this owner stays in pre-brainstorm and the remaining hygiene action is still limited to one narrow doc checkpoint if the worktree must return to clean hold.`
  - reviewer: `codex-fresh-session-reconcile-2026-04-20-third-rotation`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabe6-3b10-7d02-bc6b-7122d800fb6b` context-compacted handoff, reran the same focused patrol regressions plus `bash -n docs/system/workspace/scripts/runtime/freely`, and reconfirmed that no stronger `docs/epics/**`, `docs/progress/**`, or `docs/recovery/**` owner absorbs this idle/replan patrol seam. The lane therefore remains a bounded pre-brainstorm candidate, and the only in-scope closure is this two-file continuity/doc checkpoint back to a clean hold.`
  - reviewer: `codex-fresh-session-clean-hold-reconcile-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabe9-21c2-7041-94f2-f6df2dec59c6` context-compacted handoff, rechecked milestone placement, confirmed the current worktree started clean (`git status --short`, `git diff --stat`, `./bin/checkpoint-guard`, `freely baseline-status --project ...`), reran the same focused patrol regressions, and reconfirmed that the older completed `I-20260326-1835` source-patrol owner does not absorb the newer idle/replan scan-trigger seam. The candidate therefore remains in pre-brainstorm on a clean hold, with this continuity refresh as the only new bounded delta.`
  - reviewer: `codex-fresh-session-context-compacted-reconcile-2026-04-20`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabed-a4b3-7921-b039-8319b70d784b` `fresh_with_handoff` restart after `context compacted`, re-ran `git status --short`, `git diff --stat`, `./bin/checkpoint-guard`, and `freely baseline-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`, then reran the same focused patrol-seam checks plus `bash -n docs/system/workspace/scripts/runtime/freely`. Repo truth still starts clean, the focused patrol slice still passes without reopening implementation, and no stronger issue/progress/recovery owner absorbs this bounded idle/replan scan-trigger seam. The candidate therefore remains on a clean hold in pre-brainstorm, with this continuity/evidence refresh as the only in-scope delta.`
  - reviewer: `codex-fresh-session-context-compacted-reconcile-2026-04-20-followup`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabf3-2ce5-7c01-be02-2183ac142d4d` `fresh_with_handoff` restart after `context compacted`, reconfirmed the current worktree started clean with `git status --short`, `git diff --stat`, `./bin/checkpoint-guard`, and `freely baseline-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`, then reran the bounded patrol checks for milestone-seed inclusion, idle regeneration, active-worker broad-patrol suppression, stale delegated continuation filtering, plus `bash -n docs/system/workspace/scripts/runtime/freely`. The older completed `I-20260326-1835` owner still does not absorb this newer idle/replan scan-trigger seam, so this candidate remains entirely in pre-brainstorm and the explicit next action remains a clean hold rather than another implementation checkpoint.`
  - reviewer: `codex-fresh-session-context-compacted-reconcile-2026-04-20-post-rotation`
    verdict: `still_pre_brainstorm`
    note: `This fresh session absorbed the newer `019dabfa-babb-7a22-bca4-63ce4693ea81` `fresh_with_handoff` restart after `context compacted`, audited the actual narrow dirty tree (`git status --short`, `git diff --stat`, `./bin/checkpoint-guard`, and `freely baseline-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260420-feature-startup-task-source-patrol-and-reconcile`), reran the focused patrol checks for milestone-seed inclusion, idle regeneration, active-worker broad-patrol suppression, stale delegated continuation filtering, plus `bash -n docs/system/workspace/scripts/runtime/freely`, and reconfirmed that the older completed `I-20260326-1835` owner still does not absorb this newer idle/replan scan-trigger seam. The only live delta was a two-file candidate-owned continuity/evidence batch, so this round stayed in pre-brainstorm and closed with one narrow doc-only checkpoint commit that restored a clean hold instead of reopening implementation.`
- depends_on:
  - `docs/pre-brainstorms/20260407-0817--source-ledger-routing-and-manager-audit-boundary/candidates.md#c-20260407-0817-a`
  - `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- promoted_issue_id: `I-20260420-1130-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/manager-task-source-scan-idle-replan-boundary-governance/issues/manager-task-source-scan-idle-replan-boundary-governance.md`
- next_action: `Candidate mirror only. I-20260420-1130-A is now the canonical owner for manager idle/replan task-source scan regeneration, active-worker suppression, stale delegated filtering, and machine-readable patrol seed truth.`
- revisit_trigger: `Re-open only if provider automation, recovery-surface expansion, or a broader patrol transaction redesign can no longer stay outside this bounded owner.`
- session_refs:
  - {tool: `codex`, session_id: `current-codex-session-id-unavailable`, jsonl_path: `unavailable://fresh-session-current-id-not-exposed`, role: `author`}
  - {tool: `codex`, session_id: `019dabfa-babb-7a22-bca4-63ce4693ea81`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-40-29-019dabfa-babb-7a22-bca4-63ce4693ea81.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabf6-b205-7c90-bd92-94d7f8751f78`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-36-04-019dabf6-b205-7c90-bd92-94d7f8751f78.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabf3-2ce5-7c01-be02-2183ac142d4d`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-32-13-019dabf3-2ce5-7c01-be02-2183ac142d4d.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabed-a4b3-7921-b039-8319b70d784b`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-26-11-019dabed-a4b3-7921-b039-8319b70d784b.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabe9-21c2-7041-94f2-f6df2dec59c6`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-21-15-019dabe9-21c2-7041-94f2-f6df2dec59c6.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabe6-3b10-7d02-bc6b-7122d800fb6b`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-18-05-019dabe6-3b10-7d02-bc6b-7122d800fb6b.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabe3-8e3a-7ad1-a5a9-69e57689b9b3`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-15-10-019dabe3-8e3a-7ad1-a5a9-69e57689b9b3.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabe0-2381-7aa1-9636-c3b242e02904`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-11-26-019dabe0-2381-7aa1-9636-c3b242e02904.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabd6-26d2-7952-979e-59315886567e`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-00-31-019dabd6-26d2-7952-979e-59315886567e.jsonl`, role: `fresh_with_handoff_source`}
  - {tool: `codex`, session_id: `019dabd9-6821-7860-85f2-1e69f20f4bac`, jsonl_path: `/Users/zhaoyu/.codex/sessions/2026/04/20/rollout-2026-04-20T10-04-05-019dabd9-6821-7860-85f2-1e69f20f4bac.jsonl`, role: `fresh_with_handoff_source`}
- next_recommended_route: `doc-pre-brainstorm-execution`
- restart_point: `continuation`
- ownership: `worker-canonical-pre-brainstorm-writeback`
- checkpoint_decision: `clean-hold-after-continuity-refresh`
