# Brainstorm: runtime-startup-self-healing-governance

## Decision

Keep this owner narrow:

1. startup scripts may repair only machine-provable stale runtime state
2. manager AI may interpret continuity/governance meaning only after startup truth is canonical

## Frozen Boundary

Startup self-heal owns:

1. stale pid-file cleanup for runtime-owned roles
2. stale startup machine state downgrade after bounded grace
3. stale launch-state continuity/prompt writeback when status refresh discovers missing anchors

Startup self-heal does not own:

1. reviving or retiring interrupted issue/worktree lifecycle
2. semantic classification of stale delegated work
3. implicit restore-work during `restart`
