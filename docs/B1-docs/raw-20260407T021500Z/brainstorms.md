# Brainstorms - 20260407-0215--runtime-selfhost-continuity-gap-and-status-truth

## Context

Canonical root `develop` can still generate a fresh manager prompt, but the prompt-required continuity file is not materialized and the previous continuity remains stale. Before this followthrough, `freely live-status` could also exit before its first line when PID hint validation returned non-zero under `set -e`, which made the self-host stall look like a blank status surface instead of a narrow runtime truth gap.

The currently active committed owner under the milestone is `cli-help-and-dry-run-contract-followthrough-governance`, but its progress explicitly keeps runtime supervision out of scope. This self-host regression therefore needs to route back through the runtime blocked-intake / continuity family rather than being absorbed into the CLI contract lane.

## Decision

Open one narrow followthrough owner under the existing `runtime-blocked-intake-and-continuity-truth` family that:

1. makes status reads robust when PID hint validation fails or local PATH lacks `rg`
2. surfaces the specific self-host truth that the latest prompt requires a new manager continuity path which has not been written yet
3. keeps the scope on runtime observability and continuity-writeback truth, not generic orchestration redesign

This is not a reopen of the completed websocket / blocked-supervision owner wholesale, and it is not a continuation of the CLI help / dry-run followthrough. It is a new self-host followthrough because canonical `develop` again shows prompt-visible supervision without continuity advancement, and the completed owner explicitly says that shape should reopen as a new owner when it reappears.
