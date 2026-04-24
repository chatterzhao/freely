# Verification: runtime-closeout-selfhost-validation-exit-contract-repair-focus

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`

## Scope Verdict

- `PASS`: canonical `develop` replay isolated a real same-owner seam, not a new owner: exit-contract repair resumes were still entering the broad lead-agent body before the exact repair contract, which let retained cleanup followthrough emit a no-op `worker_done` receipt instead of a bounded blocker contract.
- `PASS`: runtime now prepends a repair-first override for both `worker_exit_contract_repair` and `manager_exit_contract_repair`, preserving the existing runtime-owned launch boundary while forcing the resumed lane to write the missing contract first.
- `PASS`: the new focused regression proves the repair override appears before `你现在进入 Freely 的首跳闭环。`, so repair instructions no longer get buried under the normal first-hop preamble.
- `PASS`: existing exit-contract regressions still pass, so the narrow repair does not weaken the broader contract directive or the rule that invalid worker contracts force precise resume repair.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
2. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
4. `./bin/governance-check`
5. `test-pre-merge-20260424-worker-exit-contract-repair-focus: bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
6. `test-pre-merge-20260424-worker-exit-contract-repair-focus: bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
7. `test-pre-merge-20260424-worker-exit-contract-repair-focus: bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
8. `test-pre-merge-20260424-worker-exit-contract-repair-focus: ./bin/governance-check`

## Real Replay Evidence

- Canonical `develop` generated cleanup worker prompt `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-015330-worker-runtime-cleanup-followthrough-resume-hygiene-codex.txt` for retained worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260422-feature-runtime-cleanup-followthrough-resume`.
- Before this repair landed in a clean lane, retained runtime replay showed repeated `launch_kind=resume` cycles that wrote `EXIT_KIND="worker_done"` with summary `Repaired the missing worker exit contract... no additional cleanup work was performed`, proving the resumed lane was satisfying the minimal repair shape without re-entering the real cleanup classification task.
- The root cause matched prompt ordering, not responsibility drift: runtime still launched the worker, but the worker session saw the broad lead-agent body before the explicit repair contract and therefore took the easiest contract-valid exit.
- Guarded premerge replay in `test-pre-merge-20260424-worker-exit-contract-repair-focus` reran the same three regressions plus `./bin/governance-check`; all passed against the receipt-bearing premerge branch, so the owner now has fresh `premerge-integration` evidence for develop absorption.

## Implementation Decision Note

- decision: `Prepend an explicit repair-first override inside runtime prompt construction.`
- why_this: `The failure was about execution ordering inside an already-correct runtime-owned repair path. Narrow prompt ordering repair fixes the seam without moving task-source scan, manager artifact writing, or worker launch ownership across components.`
- alternatives_considered: `Let manager retry the same worker indefinitely; move worker launch responsibility into manager artifacts; broaden cleanup worker scope to infer repair intent from historical context.`
- boundary_non_goals: `This change does not classify mixed-scope retained residue, consume worker_blocked contracts, or retire the retained cleanup worktree by itself.`
- residual_risk: `Canonical success still requires a real daemon replay after merge to prove the retained cleanup lane now returns a bounded blocker or retirement contract and the manager then advances to the next scan-selected task.`
