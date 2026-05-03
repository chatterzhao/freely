# Pre-tests: scan-pr-platform-config

- issue: `I-20260501-0000-A`
- lane: `governance-check`
- status: `pass`
- waiver: `hotfix — no dedicated test suite; acceptance verified by governance-check`

## Waiver

This hotfix adds a PR scan surface and config variable to the `freely` runtime script.
Standard test lanes do not cover runtime script hotfixes at this stage.
Governance: `./bin/governance-check` verifies no regressions.

- type: `lawful_non_test_waiver`
- lane: `governance-check`
- reason: `hotfix runtime script change — governance-check is the canonical quality gate`
- evidence: `governance-check PASS on merge commit`
