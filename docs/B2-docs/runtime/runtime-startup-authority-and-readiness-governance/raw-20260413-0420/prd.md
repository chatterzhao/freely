# PRD: runtime-startup-authority-and-readiness-governance

## Goal

Make Freely startup truth come from runtime-published authority instead of PID/argv resemblance so foreground attach, daemon ready, and stop cleanup share one launch model.

## Product requirements

1. Freely runtime must publish supervisor startup authority in a durable project-local artifact.
2. Supervisor validation must reject fake argv processes that were never published by the runtime.
3. `daemon start` must wait for startup truth publication before reporting running.
4. Same-project start serialization must keep the critical section until startup truth is published.
5. Stop cleanup must only preserve stop intent when another authoritative supervisor remains.
6. Existing foreground/daemon shared-status behavior must remain compatible with the explicit authority model.

## Out of scope

1. manager-ready or first continuity materialization semantics
2. a full multi-phase launch state machine beyond startup authority/readiness
3. new UI or control-plane surfaces
