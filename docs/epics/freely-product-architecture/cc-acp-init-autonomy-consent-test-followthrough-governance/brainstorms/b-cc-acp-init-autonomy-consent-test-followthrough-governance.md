# Brainstorm: cc-acp-init-autonomy-consent-test-followthrough-governance

## Narrowing

The failing surface is already reproduced and already understood:

- test: `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- failing path: `cc:auto` plus `--tool-adapter acp`
- missing contract token: `--accept-default-autonomy`

This owner therefore does not need new product discovery. It only needs to freeze that this is:

1. a stale test fixture,
2. under the tool materialization family, and
3. narrow enough to close as soon as develop absorbs the test fix.

## Owner Boundary

This owner should absorb:

1. the one-line fixture repair
2. the candidate / issue / progress / verification evidence required by the develop merge gate

This owner should not absorb:

1. any runtime logic change
2. ACP adapter expansion
3. broader `cc` profile redesign

