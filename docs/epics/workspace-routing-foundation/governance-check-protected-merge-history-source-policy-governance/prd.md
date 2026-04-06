# PRD: governance-check-protected-merge-history-source-policy-governance

## Problem

Canonical `develop` can fail governance followthrough after a valid guarded promotion because `governance-check` audits nested batch merge ancestry with the wrong branch policy.

## User-visible outcome

- Valid `test-pre-merge-* -> develop` promotions stay green on `develop`.
- Invalid direct `feature/* -> develop` merges remain red.
