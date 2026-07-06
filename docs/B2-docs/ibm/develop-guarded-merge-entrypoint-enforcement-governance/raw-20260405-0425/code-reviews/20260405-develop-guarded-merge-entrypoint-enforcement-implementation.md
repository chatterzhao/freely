# Implementation Decision Note: develop-guarded-merge-entrypoint-enforcement-governance

- issue_path: `docs/B2-docs/ibm/develop-guarded-merge-entrypoint-enforcement-governance/raw-20260405-0425/issues/develop-guarded-merge-entrypoint-enforcement-governance.md`
- branch: `feature/protected-merge-entrypoint-enforcement-20260405-0425`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-0425-feature-protected-merge-entrypoint-enforcement`

## Implementation Decision Note

- decision: `Treat guarded merge entrypoint enforcement as a narrow develop-bound pre-merge-commit contract: every develop merge commit must already carry canonical pr-merge-guarded state and completion marker before governance or promotion gates run.`
- why_this: `The recent failure mode was not that governance/promotion gates were missing; it was that raw git merge could still reach those gates and land if the staged content looked acceptable. Making the guarded handshake the first develop merge invariant closes the actual misuse path without redefining downstream policy.`
- alternatives_considered: `Relying on operator discipline around freely pr-merge-guarded was already proven insufficient. Reopening receipt/ledger owners would not stop raw merges at entry. A larger main/develop/test-pre-merge protected-branch rewrite is possible later, but it is wider than the concrete misuse reproduced here.`
- boundary_non_goals: `This change does not attempt server-side enforcement, does not widen break-glass semantics, and does not redesign receipt ledgers. It only ensures develop merges enter through the canonical guarded path.`
- residual_risk: `The hook remains a local client-side control and the narrower implementation currently targets develop only; if the same misuse becomes relevant on main or test-pre-merge branches, that should materialize as a separate follow-on rather than being silently assumed solved here.`
