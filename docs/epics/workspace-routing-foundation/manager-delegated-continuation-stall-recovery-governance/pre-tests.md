# Pre-Tests - manager-delegated-continuation-stall-recovery-governance

## Pre-merge acceptance

1. Lawful active-busy wait does not recover
- setup:
  - current manager prompt already contains delegated continuation
  - latest continuity points only to active busy worker prompts
- expect:
  - `recover_stalled_manager_ai_if_needed` stays idle-safe
  - no restart / preemption side effects are emitted

2. Mixed busy and launchable continuity still recovers
- setup:
  - latest continuity contains one active-busy worker prompt and one still-launchable worker prompt
- expect:
  - manager stall recovery still triggers

3. Older continuity cannot suppress current recovery
- setup:
  - current prompt is newer than a still-busy older continuity
- expect:
  - recovery follows the current prompt, not the older continuity

4. Busy worker plus stale prompt target still recovers
- setup:
  - latest continuity mixes one active busy worker prompt with one stale / missing target
- expect:
  - busy-wait helper fails conservatively
  - manager stall recovery still triggers

5. Stale queued worker prompt relaunch
- setup:
  - launch-state still queues a worker prompt, but the target worker is no longer running
- expect:
  - prompt becomes launchable again and is relaunched

## Post-merge acceptance

1. Keep `develop` runtime stopped until merge/writeback is finished
- expect:
  - no live dogfood restart happens from the pre-fix stalled state

2. After merge, resume a focused dogfood round
- expect:
  - `same-lane busy` no longer causes repeated `local_continuation_reentry`
  - genuinely stale queued prompts or launchable followthrough still recover
