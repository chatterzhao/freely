# Verification: memark-protected-root-bootstrap-followthrough-governance

- issue_id: `I-20260416-0448-A`
- issue_path: `docs/B2-docs/config/packaging/raw-20260402-0403issues/memark-protected-root-bootstrap-followthrough-governance.md`
- branch: `feature/memark-init`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init`
- verification_date: `2026-04-16`
- verifier: `codex`

## Scope Verdict

- `PASS`: the change is correctly classified as a narrow bootstrap followthrough under the fresh-project/bootstrap family.
- `PASS`: canonical Freely root `.gitignore` now includes `.memark/` and `corpus/`.
- `PASS`: linked worktree MemArk usage still works through `memark status` and `memark context`.
- `PASS`: root readiness is improved without claiming protected-root runtime-state writes are now allowed.

## Commands

1. `git diff --check`
2. `rg -n '^\\.memark/$|^corpus/$' .gitignore`
3. `/Users/zhaoyu/.memark/venv/bin/memark init /Users/zhaoyu/Downloads/code/my-freely/freely --no-auto --json`
4. `/Users/zhaoyu/.memark/venv/bin/memark status --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --json`
5. `/Users/zhaoyu/.memark/venv/bin/memark context --workspace /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-memark-init --project freely --no-refresh`
6. `./bin/governance-check`

## Notes

- Root `memark init` is still expected to stop before direct runtime-state setup on protected Freely root; this owner only proves the ignore prerequisite is now present.
- The usable MemArk execution surface for active Freely work remains the linked writable worktree.

## Implementation Decision Note

- decision: `Add the missing root ignore entries and carry the minimum lifecycle evidence needed for guarded develop promotion.`
- why_this: `The new MemArk guidance made the missing root ignore contract explicit, and the linked worktree path was already healthy.`
- alternatives_considered: `Silently keep using the linked worktree only; bypass the merge gate; widen into broader MemArk runtime integration.`
- boundary_non_goals: `No protected-root write-policy change and no claim that canonical root now directly hosts MemArk runtime state.`
- residual_risk: `Canonical root may still reject direct init for governance reasons unrelated to ignore coverage; that boundary is intentional and remains outside this owner.`
