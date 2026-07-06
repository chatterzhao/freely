# Brainstorm: governance-check-protected-merge-history-source-policy-governance

## Decision

- Treat this as a narrow governance-check follow-on instead of reopening the CLI wrapper owner.
- Fix branch-history selection, not receipt trailers.

## Boundary

- The minimal correct history for protected-branch receipt auditing is the branch's first-parent merge chain.
- Nested batch merges remain auditable on their own `test-pre-merge-*` branch; they should not be reinterpreted as direct `develop` merges.
