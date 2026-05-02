# Brainstorms - 20260419-1505--runtime-supervisor-attach-reuse-followthrough

- date: `2026-04-19`
- status: `materialized`
- source: `checkpoint worktree continuation`

## Context

The checkpoint branch `feature/checkpoint-lifecycle-trace-debuggability-20260419` still carries bounded runtime behavior that is not represented by any canonical owner in the current repo docs:

1. `freely daemon start` should reuse a healthy same-project supervisor instead of relaunching another detached chain.
2. `freely start` should attach to the same live supervisor between AI cycles, including the narrower fallback where `ps` is unavailable but project ownership is still provable.
3. Claude launches should stay isolated under the project runtime home rather than inheriting a shared host HOME.

## Why This Needs Its Own Owner

1. These changes are concrete implementation truth that still lives only on the checkpoint branch.
2. Existing owners in this worktree mostly describe earlier memark or runtime closeout followthrough scope; they do not lawfully own this attach/reuse seam.
3. The preserved branch is too substantial to retire as archive-only state and too narrow to reopen broader runtime architecture work.

## Proposed Bounded Seam

1. Healthy supervisor reuse and attach behavior for repeated `daemon start` and foreground `start`.
2. Runtime-home isolation for Claude launcher execution under the same project runtime boundary.
3. Minimal lifecycle writeback so future guarded replay can evaluate one explicit owner instead of an undocumented checkpoint.
