# Brainstorms: runtime-loop-log-timezone-label-followthrough

The runtime time-display owner is already canonical for status and CLI surfaces, but the loop log header still printed local wall-clock time without a timezone label. That leaves one human-readable display surface out of policy even though the underlying time is already host-local.

This should reopen as a narrow followthrough rather than stretching the completed owner:

1. keep storage and naming truth untouched,
2. add the timezone abbreviation only to the loop log header display string, and
3. prove it with a focused regression that observes `loop.log` directly.
