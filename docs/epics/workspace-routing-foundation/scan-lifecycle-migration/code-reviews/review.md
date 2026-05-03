# Code Review — Scan Lifecycle Migration

- issue_id: `I-20260503-0200-A`
- issue_path: `docs/epics/workspace-routing-foundation/scan-lifecycle-migration/issues/I-20260503-0200-A.md`
- review_date: `2026-05-03`
- reviewer: `ai`
- verdict: `approved`

## Changes Reviewed
- `task-lifecycle-scan.py`: chain trace, chat inbox, governance
- `freely`: prompt builder rewritten
- `acp-bridge.py`: hash-based socket path
- `wt-create`: fixed regex, test-pre-merge support
- `pre-push.sh`: branch naming gate
- `.githooks/post-checkout`: auto pre-init-runtime

## Implementation Decision Note
- Chain trace replaces flat scan: 12 mandatory + 2 optional stations
- Branch naming no longer exempts legacy
- AF_UNIX socket uses SHA256 hash for short path
