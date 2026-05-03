# Candidates: ACP Bridge Path Sync

## C-20260503-0115-A

- candidate_id: `C-20260503-0115-A`
- title: fix: sync acp-bridge hash-based socket paths across bash and Python
- status: promoted
- priority: P0
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/acp-bridge-path-sync/issues/I-20260503-0115-A.md`
- why_now: ACP bridge socket/path mismatch prevents daemon from launching AI. Commit `805b6d67` introduced hash-based paths in acp-bridge.py but didn't sync the three bash scripts, breaking the daemon's ACP bridge.
