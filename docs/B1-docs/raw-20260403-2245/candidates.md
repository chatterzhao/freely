# Candidates - 20260403-2245--sandbox-compatible-runtime-bootstrap-and-operator-state

## Context

- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260403-2245-A

- candidate_format_version: `v2`
- title: Sandbox-compatible runtime bootstrap and operator-state governance
- problem: In a sandboxed operator session, Freely can currently lose both lawful recovery paths at once: direct worktree Git writes may be blocked, and `freely start/chat/status` may also fail because global operator state defaults to `$FREELY_HOME` outside the sandbox and runtime discovery hard-depends on `/bin/ps`.
- why_now:
  - this failure happened during the canonical `develop` salvage closeout on `2026-04-03`
  - the current worktree-bootstrap lane already proved sibling worktree tool boundaries are not enough by themselves
  - completed runtime command owners explicitly require future contract changes to open a new lifecycle instead of silently reopening finished scopes
- acceptance_criteria:
  - Freely defines a lawful bootstrap path when the default `$FREELY_HOME` is unwritable in the current sandbox
  - runtime readiness and status surfaces degrade clearly when process inspection is sandbox-blocked, instead of failing as if the whole command were invalid
  - the contract distinguishes truly global operator state from project-scoped fallback state
  - sandbox-constrained operator sessions can still route work into the correct project/worktree without pushing development back into protected branches
- promotion_gate:
  - prove the failure is a real operator dead-end, not just a local shell quirk
  - keep the owner narrow to runtime/operator-state bootstrap and degraded readiness semantics
  - do not reopen completed `project command semantics` or `tool boundary bootstrap` umbrellas
  - identify which artifacts may lawfully move to project scope and which must remain global/shared
- open_questions:
  - should Freely automatically choose a project-local fallback for `$FREELY_HOME` when the default home is unwritable, or should that remain an explicit operator opt-in
  - which parts of `$FREELY_HOME` are truly shared control-plane truth versus bootstrap-local convenience state
  - what is the minimum process/readiness evidence Freely can trust when `/bin/ps` is unavailable
  - should degraded runtime mode be limited to bootstrap/intake routing, or can it also truthfully serve `status/live-status`
- acceptance_reviews:
  - reviewer: `pending`
    verdict: `accepted`
    note: narrowed owner boundary has been frozen into a dedicated workspace-routing-foundation issue
- decision_reason:
  - this discovery was exposed by real dogfood cleanup rather than hypothetical architecture debate
  - the gap sits between two already-completed owners and therefore needs its own lifecycle
  - leaving the failure undocumented keeps a silent path back toward protected-root misuse
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260403-2245-A`
- promoted_issue_path: `docs/B2-docs/ibm/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialized into a dedicated issue on branch `feature/sandbox-compatible-runtime-bootstrap-and-operator-state-20260403-2245`
  - implement project-scoped bootstrap fallback and ps-less degraded readiness without reopening parent owners
- revisit_trigger:
  - reopen immediately if sandbox-constrained sessions still cannot route lawful work through Freely without falling back to protected-root edits
