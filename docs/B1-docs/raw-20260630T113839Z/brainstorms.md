---
b1_id: B1-20260630T113839Z
phase_state: completed
source_raw: raw-20260630T113839Z39Z
produced_candidate: C-20260630T113839Z-A
---
# B1: daemon dirty check excludes .freely/run/ runtime files
## Problem
.freely/run/workcell-state.env is modified during daemon operation, then blocks restart.
## Decision
Add .freely/run/*, .freely/logs/*, .freely/*.db to disposable runtime residue.
