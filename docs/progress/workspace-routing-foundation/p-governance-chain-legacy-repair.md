# Progress: governance-chain-legacy-repair

- issue_id: `I-20260403-1100-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/issues/governance-chain-legacy-repair.md`
- title: `Governance chain legacy repair for develop push unblock`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `develop`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-merge-sandbox-develop`
- updated_at: `2026-04-03`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner is now the canonical umbrella lane for the current legacy governance-chain unblock batch.
- The immediate repair is not only legacy file backfill; it also includes fixing the governance of the current repair itself.
- The active child slices are `1200`, `1201`, `1202`, and `1203`. Their current canonical state is “parent-linked child slice in pre-brainstorm”, not independent promoted owner.
- These slices are governance children of `1100`, but git-sibling branches sharing merge-base `0f97fc0227bba66b2552a57a7611c482b19ec150`; the explicit map lives in `docs/epics/workspace-routing-foundation/governance-chain-legacy-repair/child-slice-status.md`.
- The canonical writeback did not merge from `feature/governance-chain-legacy-repair-20260403-1100` directly. That source lane carried unrelated stale history, so the develop-safe landing path was the fresh replay branch `feature/governance-chain-legacy-repair-promote-20260403-175428`, merged into `develop` as `de93a83`.
- The original `1100/1200/1201/1202/1203` local worktrees are now retired. Their coordinates remain historical provenance only; any future execution must reopen from current `develop`.

## Current Batch Risks

1. The child-slice routing truth is now canonical, but the actual legacy artifact backfill work is still pending.
2. Any later legacy field repair must reopen from current `develop` in a fresh feature worktree, not from the retired sibling research lanes.
3. The retained remote research refs (`origin/feature/governance-chain-legacy-repair-20260403-1100`, `origin/feature/verification-artifact-dir-repair-20260403-1200`, `origin/feature/implementation-decision-note-repair-20260403-1201`) can still confuse route ownership if they are treated as live mutate roots instead of historical evidence.
4. Unrelated dirty trees still exist in the broader fleet and must remain explicitly excluded from this owner's cleanup decisions.

## Next Action

1. Reopen any remaining legacy field backfill as a fresh feature worktree from current `develop`, and bind it explicitly to `I-20260403-1100-A` before coding.
2. Keep the child-slice docs aligned with the current truth: local research worktrees retired, remote research refs retained-with-reason, and parent routing decided by `I-20260403-1100-A`.
3. Continue verification without weakening `governance-merge-gate`.

## Fleet Hygiene Snapshot

- Current `./bin/wt-fleet-status` shows only repo-root `develop` as unrelated dirty, four `.cursor` scratch worktrees as dirty scratch surfaces, and the merge-sandbox `develop` worktree as clean protected-branch reference.
- `de93a83` records the guarded develop writeback for the canonical governance-chain repair, `9c9138c` records cleanup disposition, and `61beab2` refreshes the fleet snapshot after local retirement.
- File-level governance repair and commit recording are complete for the original `1100/1200/1201/1202/1203` research branches, and the resulting canonical docs were replayed safely through the promotion lane.
- Retired in this session:
  - `feature/hook-bypass-breakglass-governance-20260402-0020`
  - `feature/hook-bypass-breakglass-closeout-20260402-0235`
  - `feature/protected-branch-merge-receipt-hardening-20260402-1912`
  - `feature/frontend-probe-milestone-closeout-20260402-frontend`
- Also retired in this session after guarded merge:
  - `feature/frontend-probe-v0-closeout-20260402-frontend`
  - `feature/frontend-runtime-baseline-lifecycle-alignment-20260402-frontend`
- Also merged to canonical `develop` and retired after writeback:
  - `feature/governance-chain-legacy-repair-promote-20260403-175428`
  - `feature/hook-bypass-break-glass-governance-20260402-1719`, whose follow-on pre-brainstorm candidate now lives in `docs/pre-brainstorms/20260402-1719--hook-bypass-break-glass-governance/`
- Research writeback completed and retired locally:
  - `feature/governance-chain-legacy-repair-20260403-1100`
  - `feature/verification-artifact-dir-repair-20260403-1200`
  - `feature/implementation-decision-note-repair-20260403-1201`
  - `feature/candidate-touched-repair-20260403-1202`
  - `feature/issue-id-key-repair-20260403-1203`
- Ignored as scratch/non-canonical in this round:
  - `/Users/zhaoyu/.cursor/worktrees/freely/c3tIe`
  - `/Users/zhaoyu/.cursor/worktrees/freely/E95vZ`
  - `/Users/zhaoyu/.cursor/worktrees/freely/LSbgu`
  - `/Users/zhaoyu/.cursor/worktrees/freely/yLI9P`
- Keep and investigate separately from this owner:
  - repo-root `develop`, which currently carries a large staged documentation batch outside the `1100` repair scope
  - `.cursor/worktrees/freely/{c3tIe,E95vZ,LSbgu,yLI9P}`, which all show the same repeated scratch diff pattern and should not be treated as canonical owner truth
  - remote `origin/feature/governance-chain-legacy-repair-20260403-1100`
  - remote `origin/feature/verification-artifact-dir-repair-20260403-1200`
  - remote `origin/feature/implementation-decision-note-repair-20260403-1201`
    because those remote refs are not direct `develop` ancestors even though their canonical content has been replayed and absorbed through the promotion lane

## Execution Constraint

- The canonical owner truth now lives on `develop`; this progress file must not treat retired sibling worktrees as active mutate roots.
- Future execution must branch from current `develop`; the old sibling research containers are historical provenance only.
