# Candidates - 20260417-0445--runtime-start-stop-process-lifecycle-and-leak-contract

## Context
- Source brainstorm: `docs/B1-docs/raw-20260417-0445/brainstorms.md`
- Status: `promoted`
- Route: `materialize-bounded-runtime-owner-and-replay-through-guarded-premerge`

## Candidates

### C-20260417-0445-A: legacy issue
- candidate_format_version: `v2`
- title: `Enforce CLI-first runtime lifecycle contract for Freely start/stop without watcher leakage`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260417-0445-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
  - `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- problem: `freely` currently mixes user-facing CLI semantics with internal runtime attach/repair semantics. In the field this shows up as repeated `start` / `daemon start` reusing or rebuilding partial runtime state instead of clearly refusing, while `stop` can leave same-project watchdog / dispatcher / AI descendants alive. The result is a restart storm pattern: users believe they stopped the runtime, but surviving watchers relaunch it.
- why_now:
  - live process inspection already showed repeated-start drift, stale start-lock truth, surviving same-project relaunchers, and local `.iflow` fast-exit storms in one bounded seam
  - focused implementation and disposable premerge verification are already present, so the remaining blocker is canonical owner lifecycle truth rather than missing executable evidence
  - guarded `develop` promotion cannot lawfully consume candidate-only runtime notes for an implementation-bearing diff
- acceptance_criteria:
  - repeated `freely start --project <project>` rejects with a clear stop-first contract and does not spawn extra runtime processes
  - repeated `freely daemon start --project <project>` rejects under the same contract and does not spawn extra daemon/runtime chains
  - `--force` remains explicit stop-then-start rather than silent attach
  - `freely stop --project <project>` converges on zero same-project watchdog, dispatcher, AI, and AI descendant relaunchers within the bounded cleanup window
  - `.iflow` local-state failure is materialized as runtime failure and the full AI descendant tree is terminated
  - lifecycle-trace and interruption-manager focused regressions remain green as bounded verification for the same seam
- promotion_gate:
  - keep scope on repeated-start rejection, lawful start-lock truth, same-project relauncher cleanup, AI failure containment, and bounded lifecycle trace support
  - do not widen into manager continuity, slot recovery, or a broader runtime orchestration rewrite
  - require explicit owner issue/progress/pre-tests/review truth plus guarded premerge adequacy before `develop` promotion
- open_questions:
  - whether a later owner should expose an explicit user-visible attach mode rather than keeping attach internal-only
  - whether future same-project discovery hardening should distinguish more runtime roles beyond watchdog and interruption-dispatcher without widening this owner
  - whether canonical `develop` followthrough should later materialize one stronger protected-worktree replay artifact for repeated-start rejection itself
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The field evidence supports a contract bug more than an isolated leak bug. The safe first move is to freeze start/daemon start/stop semantics, then make watcher cleanup conform to that contract.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260417-0445-A` is now the canonical owner for CLI-first repeated-start rejection, lawful start-lock handling, same-project relauncher cleanup, AI fast-exit containment, and bounded lifecycle-trace support.
- revisit_trigger: Re-open only if canonical implementation later regresses back toward silent repeated-start attach, leaves relaunch-capable same-project processes behind, or proves this bounded lifecycle seam still hides a different owner-worthy runtime defect.
- decision_reason: `The restart storm pattern is not credibly solvable without one bounded owner that freezes user-facing start/stop semantics and makes watcher cleanup plus AI failure containment conform to that same contract.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
