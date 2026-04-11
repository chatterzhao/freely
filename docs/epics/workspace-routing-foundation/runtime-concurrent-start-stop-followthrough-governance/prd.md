# PRD: runtime-concurrent-start-stop-followthrough-governance

## Problem

The remaining unabsorbed portion of `C-20260408-0231-A` is not a status read-path problem anymore. It is a bounded runtime followthrough problem:

- duplicate same-project supervisors can still survive if stop only targets the pid-file owner
- degraded process inspection can still destabilize bootstrap attach/reuse
- stop-marker cleanup can mis-report project intent while another same-project supervisor is alive

## Product requirement

Freely must keep same-project runtime ownership truthful during bootstrap and stop followthrough:

1. bootstrap grace preserves attach/reuse under degraded inspection
2. stop is project-scoped, not pid-file scoped
3. stop intent persists until the last same-project supervisor exits

## Out of scope

- generated continuity truth in status/fleet surfaces
- broader watchdog or worker recovery redesign
- generic checkpoint-risk prediction or stale-lane preflight guidance
