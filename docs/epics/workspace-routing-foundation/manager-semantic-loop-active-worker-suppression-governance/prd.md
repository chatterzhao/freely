# PRD: manager-semantic-loop-active-worker-suppression-governance

## Goal

Make the semantic-loop monitoring surface conservative again by suppressing the signal whenever runtime already has active-worker truth.

## Product Requirements

1. Preserve the current zero-worker semantic-loop suspicion behavior.
2. Suppress semantic-loop suspicion when worker execution is already active.
3. Allow persisted launch-state active-worker count to suppress the signal when process discovery briefly lags behind runtime-owned truth.
4. Do not widen the change into recovery automation or unrelated status semantics.
