# PRD: runtime-human-readable-time-display-governance

## Goal

Make Freely's human-readable runtime status time output consistent: stored truth remains stable and comparable, while user-facing status surfaces render in the host system timezone with timezone label.

## Requirements

1. Human-facing runtime status timestamps use host-local display time.
2. Stored truth remains RFC3339 / ISO / epoch.
3. Display formatting must not rewrite backup naming or governance sort keys.
4. Runtime status, `freely ai`, and watchdog human text follow the same display rule.

## Product Rules

1. Display truth and machine truth stay separate.
2. Human-readable fields may add sibling `*_human` outputs rather than mutating raw truth fields.
3. Invalid or unavailable timestamps pass through unchanged instead of fabricating a local value.

## Exit Criteria

1. `freely live-status`, `baseline-status`, intake status, and `develop-push status` all show local display timestamps.
2. `freely ai status` preserves raw truth while also surfacing local display text.
3. Focused tests cover both runtime status output and ai/watchdog display behavior.
