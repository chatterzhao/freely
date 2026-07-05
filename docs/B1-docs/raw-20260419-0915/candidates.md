# Candidates - 20260419-0915--three-loop-single-source-followthrough

## Context
- Source brainstorm: `docs/B1-docs/20260419-0915--three-loop-single-source-followthrough/brainstorms.md`
- Status: `promoted`
- Route: `materialize-three-loop-single-source-followthrough-owner`

## Candidates

### C-20260419-0915-A
- candidate_format_version: `v2`
- title: `Three-loop lifecycle single-source governance followthrough`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260419-0915-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
- problem: The original three-loop owner is already completed, but this follow-on governance pass still needs to land the rule that `docs/system/workspace/three-loop-capability-lifecycle.md` is the sole detailed whole-app lifecycle truth and that downstream skills/agents read and sync against it instead of co-maintaining parallel detailed restatements.
- why_now:
  - this document defines the whole-app lifecycle and is a critical onboarding/runtime reference
  - parallel detailed maintenance across multiple docs increases drift risk and violates the single-source intent
  - the refactor is already implemented on the current feature lane and only lacks lawful develop-bound lifecycle evidence
- acceptance_criteria:
  - `docs/system/workspace/three-loop-capability-lifecycle.md` is the only detailed whole-app lifecycle specification in the active truth set
  - downstream agent/skill docs state that they should read and sync to this canonical document when lifecycle semantics matter, rather than restating the detailed model
  - the develop-bound diff carries concrete issue, pre-tests, tasks, progress, and review artifacts for this governance-only follow-on owner
  - guarded replay through `test-pre-merge-three-loop-governance-20260419` succeeds and the temporary worktrees retire after merge
- promotion_gate:
  - keep scope on single-source lifecycle governance and consumer sync expectations only
  - do not reopen broader loop-model architecture debates that were already closed by `I-20260324-0405`
  - require same-line owner lifecycle evidence before guarded merge to develop
- open_questions:
  - whether future doc/skill templates should automate a standard “read canonical lifecycle truth first” reminder instead of repeating local prose
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `This follow-on owner is narrow and lawful: it closes the remaining single-source governance gap after the original three-loop model issue already completed.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260419-0915-A` is now the canonical owner for the three-loop single-source governance followthrough and immediate retirement of the temporary merge worktrees after guarded replay.
- revisit_trigger: Re-open only if canonical `develop` still allows parallel detailed lifecycle truth to drift across active docs or if consumer-facing skills/agents prove the read-and-sync contract is still underspecified.
- decision_reason: `The detailed three-loop lifecycle model is already stable, but this follow-on governance rule still needs a lawful develop-bound owner after the original family completed. A narrow new owner is safer than silently extending the completed issue.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
