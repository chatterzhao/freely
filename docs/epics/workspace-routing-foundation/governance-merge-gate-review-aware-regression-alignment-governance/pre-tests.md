# Pre-tests

## Pre-merge acceptance

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
   - expectation: the mixed unresolved-candidate implementation case stages a complete review artifact and then passes, while same-file borrowed-owner regressions still fail
2. `git diff --check`
   - expectation: the refreshed fixture and lifecycle docs stay whitespace-clean
3. `./bin/governance-check`
   - expectation: the narrow reopen lifecycle is complete and merge-ready

## Post-merge acceptance

1. Canonical `develop` keeps `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` green after replay.
2. The follow-on keeps merge-gate semantics aligned with existing law: unresolved metadata repairs remain allowed with same-line owner evidence, and same-file borrowed-owner regressions remain blocked.
