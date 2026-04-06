# Tasks: governance-check-protected-merge-history-source-policy-governance

1. Reproduce the false negative with nested `test-pre-merge-*` merge ancestry.
2. Restrict protected-branch receipt auditing to first-parent merge history.
3. Add and pass a focused regression.
4. Replay `./bin/governance-check` on canonical `develop`.
