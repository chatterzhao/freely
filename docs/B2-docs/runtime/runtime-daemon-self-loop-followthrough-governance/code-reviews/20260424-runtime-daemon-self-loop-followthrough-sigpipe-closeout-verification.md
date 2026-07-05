# Verification: runtime-daemon-self-loop-followthrough-governance SIGPIPE supervisor closeout guard

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/runtime-sigpipe-supervisor-closeout-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-sigpipe-supervisor-closeout`

## Scope Verdict

- `FAIL`: canonical replay after the manager/source-runtime rebind still stranded supervisor closeout. Runtime evidence showed `ai_launch_begin` with no matching `ai_cycle_finished`, stale `ai.pid` truth, and repeated `printf: write error: Broken pipe` lines while daemon patrol and continuity scanning were still resolving retained cleanup followthrough.
- `PASS`: the blocker is narrow and same-owner. Cached discovery producers were still writing with bare `printf` into process-substitution and early-return consumers, so a lawful short-circuit in continuity selection or PID/worktree discovery could abort the supervising shell under `set -euo pipefail`.
- `PASS`: `project_worktree_list_porcelain_cached()` and `manager_continuity_files_desc_for_project()` now emit cached multi-line output through a bounded helper that traps `PIPE`, ignores `SIGPIPE`, and returns success when the downstream consumer stops after finding the first needed record.
- `PASS`: the repair stays continuity-first. It does not widen task-selection policy, relax worker launchability, or bypass exit-contract truth; it only prevents producer-side closed-pipe exits from killing manager/worker supervision before closeout can consume the already-written artifacts.
- `PENDING`: guarded promote into canonical `develop` and a fresh `freely daemon start` replay still need to prove this seam is the last blocker on retained cleanup closeout and next-task continuation.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`
2. `bash docs/system/workspace/scripts/tests/test-freely-discover-supervisor-pid-sigpipe-guard`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-continuity-discovery-tolerates-closed-pipe`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-ignores-pre-stop-continuity`

## Implementation Decision Note

- decision: `Guard cached runtime discovery producers against SIGPIPE instead of weakening the early-return consumers that already encode the right continuity and patrol semantics.`
- why_this: `Replay evidence showed closeout was failing after AI exit, not because consumers chose the wrong continuity or worker, but because the producer side treated lawful early consumer exit as a fatal shell error.`
- alternatives_considered: `Remove early returns from continuity selection; wrap every consumer call site in custom pipe handling; demote the seam to operator-only replay and manually restart stranded supervisors.`
- boundary_non_goals: `No broader patrol redesign, no runtime-event schema change, no worker prompt contract change, and no claim that canonical develop is fully green before protected replay confirms retained cleanup closeout.`
- residual_risk: `Canonical replay may still expose another producer-side closed-pipe seam outside the two cached helpers patched here, but the previously observed continuity-selection and worktree-summary closeout path should no longer strand the supervisor on SIGPIPE alone.`
