# PRD: codex-real-exec-switch-and-after-failure-recovery-governance

## Objective

Keep Codex slot selection and runtime recovery aligned with real executable truth so Freely can keep moving forward after a live failure without mutating manual switch semantics or relying on stale inventory hints.

## Product Requirements

1. `freely start` uses the current slot directly and only enters automatic recovery after a real failure.
2. Automatic recovery skips the failed current slot, tests later saved slots in order, and stops on the first usable slot.
3. Manual `bin/ai switch codex` remains a full-sweep inventory command.
4. Slot-local network/certificate failures during testing cause immediate child termination and next-slot continuation.
5. Real command-surface validation and auth restoration are mandatory owner evidence.
