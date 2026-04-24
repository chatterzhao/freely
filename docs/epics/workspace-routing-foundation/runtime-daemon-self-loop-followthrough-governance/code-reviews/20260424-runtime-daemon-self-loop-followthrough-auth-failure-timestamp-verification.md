# Verification: runtime-daemon-self-loop-followthrough-governance auth-failure timestamp false positive

- issue_id: `I-20260421-1200-A`
- date: `2026-04-24`
- scope: `Feature-local verification for the canonical self-host seam where a timestamped non-auth error line was misclassified as auth_failure because the old detector matched bare 401 inside fractional-second log timestamps.`
- lane: `feature/auth-failure-timestamp-false-positive-20260424`

## Findings

- `PASS`: replay evidence from canonical `develop` isolated the false-positive seam precisely. `runtime_error_signal_excerpt` for `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/logs/cycle-20260424-045301.log` returned only `ERROR ... apply_patch verification failed ... manager-exit-contract.env: No such file or directory`, but the old `log_has_auth_failure()` still returned true because the timestamp fragment `.401071Z` matched the previous bare `401` branch.
- `PASS`: auth detection is now bounded to auth-shaped phrases instead of bare numeric substrings, so ordinary runtime errors with fractional-second timestamps no longer collapse the manager loop into fake `auth_failure`.
- `PASS`: adjacent Codex apikey OAuth-refresh filtering still behaves as designed; the narrowed auth matcher does not reopen the older benign-refresh-noise seam.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-runtime-auth-failure-signal-filter`
- `bash docs/system/workspace/scripts/tests/test-freely-log-has-auth-failure-ignores-codex-apikey-oauth-refresh-noise`
- `bash -lc 'source docs/system/workspace/scripts/runtime/freely; AI_TOOL=codex; if log_has_auth_failure /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/logs/cycle-20260424-045301.log; then echo TRUE; else echo FALSE; fi'`
- `./bin/governance-check`

## Status

- `PASS`: feature-local regression and real-log replay both show the timestamp-driven auth false positive is closed without weakening true auth-failure detection.
- `PENDING`: guarded premerge plus canonical `develop` daemon replay still need to prove manager now consumes the queued retained-cleanup worker followthrough instead of stopping at the former fake `auth_failure` seam.
