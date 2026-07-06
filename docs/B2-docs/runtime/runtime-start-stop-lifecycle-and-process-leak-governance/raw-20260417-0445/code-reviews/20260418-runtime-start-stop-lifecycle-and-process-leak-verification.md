# Verification: runtime-start-stop-lifecycle-and-process-leak-governance

- issue_id: `I-20260417-0445-A`
- issue_path: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- verification_date: `2026-04-18`
- verifier: `codex`

## Scope Verdict

- `PASS`: repeated user-facing `freely start` and `freely daemon start` now reject while an authoritative same-project runtime is already active.
- `PASS`: start-lock handling now stays lawful across self-owned lock reuse, orphaned ai hints, stale active-owner cleanup, and launch-failure cleanup.
- `PASS`: `freely stop --project` now terminates discovered same-project watchdog and interruption-dispatcher processes instead of leaving relaunch-capable remnants behind.
- `PASS`: local `.iflow` state failures are now classified as runtime failures and `monitor-ai-cli.sh` terminates the full AI descendant tree on failure.
- `PASS`: bounded interruption-manager fast-path and lifecycle-trace regressions stayed green, so the added observability remains inside this owner’s runtime seam.
- `PASS`: the disposable `test-pre-merge-runtime-lifecycle-20260417` batch already reran the focused regression set plus `./bin/governance-check`, so this owner now carries explicit `premerge-integration:develop_merge` adequacy evidence.

## Commands

1. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-precheck-ignores-self-owned-start-lock`
2. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-rejects-when-runtime-already-running`
3. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
4. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-interruption-manager-fast-path-control-validation`
5. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-lifecycle-trace-log`
6. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-stalled-active-owner`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-self-owned-start-lock`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-rejects-when-runtime-already-running`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-releases-start-lock-when-startup-fails`
11. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-discovered-watchers-and-dispatchers`
12. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-codex-session-permission-failure`
13. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-iflow-local-state-failure`
14. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-iflow-descendants-on-runtime-failure`
15. `./bin/test-lane premerge-integration -- ./bin/governance-check`
16. `git diff --check`

## Implementation Decision Note

- decision: `Freeze a CLI-first repeated-start contract while tightening same-project start-lock truth, relauncher cleanup, and AI failure containment inside one bounded runtime lifecycle owner.`
- why_this: `The field evidence showed the restart storm was one cross-cut seam rather than isolated leftovers: repeated user starts, stale start-lock truth, same-project watcher leakage, and local fast-exit storms all reinforced each other.`
- alternatives_considered: `Keep attach/reuse as the default repeated-start behavior; rely on pid-file cleanup alone; kill only the direct AI child and treat local .iflow failures as ordinary exits; split lifecycle tracing into a separate owner before the start/stop seam was closed.`
- boundary_non_goals: `This owner does not redesign manager continuity, generic process-management architecture, or slot/auth recovery policy.`
- residual_risk: `Canonical develop still needs one short post-merge followthrough replay so the protected worktree proves the same bounded runtime contract before the disposable premerge lane is retired.`
