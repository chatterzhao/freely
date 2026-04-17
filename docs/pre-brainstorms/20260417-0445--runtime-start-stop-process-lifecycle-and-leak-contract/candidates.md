# Candidates - 20260417-0445--runtime-start-stop-process-lifecycle-and-leak-contract

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260417-0445-A
- candidate_format_version: v2
- title: Enforce CLI-first runtime lifecycle contract for Freely start/stop without watcher leakage
- problem: `freely` currently mixes user-facing CLI semantics with internal runtime attach/repair semantics. In the field this shows up as repeated `start` / `daemon start` reusing or rebuilding partial runtime state instead of clearly refusing, while `stop` can leave same-project watchdog / dispatcher / AI descendants alive. The result is a restart storm pattern: users believe they stopped the runtime, but surviving watchers relaunch it.
- why_now: Live process inspection already showed all three layers at once: `iflow` fast-exit on local `.iflow` state failure, incomplete AI descendant cleanup, and multiple surviving `ensure-manager --watch` processes that kept recreating the runtime. The user expectation is now explicit: repeated `start` / `daemon start` must require a prior `stop`, and `stop` must be complete for both foreground and daemon launches.
- acceptance_criteria:
  - repeated `freely start --project <project>` rejects with a clear “already running; stop first” contract and does not spawn extra runtime processes
  - repeated `freely daemon start --project <project>` rejects with the same contract and does not spawn extra runtime processes
  - `--force` remains explicit stop-then-start rather than silent attach
  - `freely stop --project <project>` converges to zero same-project supervisor, watchdog, dispatcher, AI, and AI descendant processes within a bounded cleanup window
  - `iflow` fast-exit on local `.iflow` permission/state failure does not trigger blind relaunch storm behavior
  - root project runtime is not silently supervised long-term by stale feature-worktree watcher processes
- promotion_gate:
  - freeze a CLI-first contract that cleanly separates user-facing start semantics from internal recovery semantics
  - add authoritative same-project watcher/dispatcher discovery instead of trusting pid files alone
  - keep the first implementation focused on runtime lifecycle correctness, not a broad process-management rewrite
- open_questions:
  - should user-visible attach ever exist as an explicit flag, or should attach stay internal-only
  - what bounded cleanup window is strict enough for tests without making CI flaky
  - should daemon and foreground paths share a single user-facing rejection message contract
  - how should internal ensure-manager recovery call back into `start` after user CLI stops defaulting to attach
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The field evidence supports a contract bug more than an isolated leak bug. The safe first move is to freeze start/daemon start/stop semantics, then make watcher cleanup conform to that contract.`
    verdict: `ready_for_ibm`
- priority: P0
- status: active
- decision_reason: The runtime leak pattern is not credibly solvable without a stable CLI lifecycle contract. User-facing semantics and internal recovery semantics must be separated before further implementation, otherwise each local fix will be undermined by surviving watchers and ambiguous repeat-start behavior.
- next_action: Turn this into an implementation issue that first codifies repeated-start rejection and stop completeness, then lands the smallest watcher/discovery changes needed to satisfy those tests.
- revisit_trigger: Revisit scope only if later evidence shows that daemon and foreground require materially different lifecycle contracts, or if internal recovery cannot be preserved without redesigning start entrypoints.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
