# Verification: runtime-daemon-self-loop-followthrough-governance superseded frozen prompt reclaim

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/manager-worker-launch-superseded-frozen-prompt-reclaim-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-worker-launch-superseded-frozen-prompt-reclaim`

## Scope Verdict

- `FAIL`: canonical `develop` still stalled after the recorded self-intent repair because older same-lane frozen prompts were still counted as active ownership blockers against the current authoritative retained-lane prompt.
- `PASS`: the actual seam was not scan-json routing and not worker bootstrap. The new prompt already carried explicit `This prompt supersedes...` history, but manager-side launch arbitration never consumed that supersession truth.
- `PASS`: runtime now parses prompt-level superseded prompt paths and excludes those older frozen prompts from `manager_frozen_blocking_intent_signatures_csv()`, `manager_frozen_prompt_for_blocking_intent_signature()`, and frozen-owner worktree ownership claims.
- `PASS`: the repair stays narrow. Frozen prompts that are not explicitly superseded remain blocking history, and the existing stale-frozen launch-state reconciliation behavior remains green.
- `PENDING`: canonical `develop` still needs guarded promote plus live daemon replay proving the authoritative retained-lane prompt actually launches, yields lawful followthrough truth, and lets Freely continue to the next task source.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-recorded-self-intent`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-superseded-frozen-self-intent`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`

## Implementation Decision Note

- decision: `Honor prompt-declared supersession when computing frozen ownership blockers for manager worker launch arbitration.`
- why_this: `The runtime already had the authoritative prompt and the retained lane stayed selected correctly; only stale frozen history prevented consumption. Consuming the prompt's own superseded list closes that seam without weakening continuity-first or broadening worker selection.`
- alternatives_considered: `Delete frozen history eagerly; ignore every frozen prompt when no worker is active; move worker launch ownership from runtime back into manager artifacts.`
- boundary_non_goals: `No scan-json source change, no new task routing rule, no relaxation for unrelated ownership conflicts, and no claim that canonical daemon acceptance is complete before live replay proves it.`
- residual_risk: `Canonical replay may still expose a later retained-lane closeout or retirement blocker, but the frozen-history queue wedge is now bounded and regression-covered.`
