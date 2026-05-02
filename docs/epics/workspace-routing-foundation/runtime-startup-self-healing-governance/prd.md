# PRD: runtime-startup-self-healing-governance

## Problem

Freely startup can leave machine-owned runtime truth in a contradictory state before manager launch: stale pid files remain, workcell state still claims `running/up/starting`, and launch-state continuity anchors may still reference missing worktrees or stale continuity files.

## Requirements

1. Startup must self-heal only machine-provable stale runtime facts before any manager-owned recovery logic runs.
2. Self-heal must respect the existing attach/reuse and restart contracts instead of reinterpreting them as implicit restore-work.
3. Self-heal must downgrade unrecoverable stale startup truth into canonical stopped/down state after a bounded grace period rather than leaving fake liveness behind.
4. Launch-state refresh must persist corrected continuity/prompt references even when capacity numbers stay unchanged.
5. The owner must prove the repair with focused regressions and a protected-root replay.

## Out Of Scope

1. Manager semantic recovery or continuation routing
2. Generic runtime/fleet redesign
3. Automatic reopening or retirement of issue/worktree lifecycle owners
