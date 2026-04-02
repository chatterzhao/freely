# PRD: cc-acp-init-autonomy-consent-test-followthrough-governance

## Goal

Keep canonical `develop` aligned with the already-frozen activation-consent contract by repairing one stale `cc:auto + adapter=acp` init fixture and writing the minimum lifecycle evidence needed to replay that repair into `develop`.

## Requirements

1. The followthrough must remain attached to the tool autonomy policy materialization family.
2. The fix must not alter runtime behavior.
3. The focused regression and governance checks must pass in the feature lane.

## Non-Requirements

1. No new ACP runtime behavior.
2. No new `cc` configuration surface.
3. No broader test sweep than the directly affected regression plus governance proof.

