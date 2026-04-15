# Verification: freely-start-auto-recovery-rootcause-governance

- issue_id: `I-20260414-0255-A`
- issue_path: `docs/epics/workspace-routing-foundation/freely-start-auto-recovery-rootcause-governance/issues/freely-start-auto-recovery-rootcause-governance.md`
- verification_date: `2026-04-14`
- verifier: `codex`

## Scope Verdict

- `PASS`: the owner now states the corrected root cause precisely: codex after-failure recovery was skipping saved slots because it reused a cache-filtered ready-slot selector.
- `PASS`: the implementation stays within the intended design boundary: one unified switch method, many failure triggers, same-tool inner loop first, then cross-tool outer loop.
- `PASS`: focused feature-local regressions passed for cache-skip prevention, forward-only slot selection, manager next-slot routing, and same-tool-before-cross-tool order.
- `PASS`: the disposable `test-pre-merge-20260414-freely-start-auto-recovery-rootcause` batch reran the same focused regressions plus `./bin/governance-check`, so this owner now carries explicit `premerge-integration:develop_merge` adequacy evidence.
- `PASS`: real feature-lane dogfood proved the repaired runtime can traverse bad codex slots in order, recover onto the current usable slot, and continue doing work by producing `.freely/run/healthcheck14.txt` and `.freely/run/healthcheck15.txt`.
- `PASS`: runtime was explicitly stopped after the replay, so this verification did not leave Freely idling and burning tokens.

## Commands

1. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-codex-after-failure-next-slot-ignores-availability-cache`
2. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-codex-select-next-slot-does-not-wrap`
3. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-codex-after-failure-uses-next-slot-not-probe`
4. `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
5. `git diff --check`
6. `./bin/merge-guarded test-pre-merge-20260414-freely-start-auto-recovery-rootcause feature/freely-start-auto-recovery-rootcause-20260414`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-codex-after-failure-next-slot-ignores-availability-cache`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-codex-select-next-slot-does-not-wrap`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-codex-after-failure-uses-next-slot-not-probe`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
11. `./bin/governance-check`

## Real-Environment Evidence

- ordered bad-slot traversal: `worahe1000 -> worahe1001 -> worahe1002 -> worahe1012 -> a1018-1 -> a1018-2 -> a1019-1`
- usable-slot replay: `a1020-1`
- task evidence:
  - `.freely/run/healthcheck14.txt` = `ok`
  - `.freely/run/healthcheck15.txt` = `ok`
- stop discipline:
  - runtime manually stopped after proof to avoid idle token burn

## Residual Followthrough

- develop guarded promote is still pending at the time of this verification note; the current artifact exists to satisfy owner-bound lifecycle and adequacy truth before replaying `test-pre-merge-* -> develop`.
- after develop absorbs this owner, one short post-merge followthrough replay remains: confirm the canonical `develop` worktree still runs correctly on the current usable slot, then stop it and retire both temporary worktrees.
