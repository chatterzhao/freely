# Candidates - 20260407-1036--human-interruption-source-governance-boundary

## C-20260407-1036-A

- candidate_format_version: `v2`
- title: `Human interruption runtime contract after source-family contraction`
- source_brainstorm: `docs/pre-brainstorms/20260407-1036--human-interruption-source-governance-boundary/brainstorms.md`
- problem: `After contracting durable source families, Freely needs a family-specific contract for real human interruptions that preserves runtime durability and manager routing while keeping AI-discovered problems and GitHub publication concerns out of the interruption lane.`
- why_now:
  - current dogfooding habits can blur true human interruption with AI-discovered intake
  - runtime truth already exists under `.freely/intake/**`
  - this is the safest first family-specific slice to refine
- acceptance_criteria:
  - define `human interruption` as real human/operator input only
  - define the minimal unresolved interruption record and manager-visible surface
  - define claim / resolve / absorb semantics that stay compatible with current runtime behavior
  - define which interruption outcomes remain runtime-local and which become durable problem-sources
  - define writeback requirements when a human interruption is consumed into `pre-brainstorm`
- promotion_gate:
  - prove the line does not absorb AI-discovered external-issue responsibilities
  - prove the result stays compatible with the umbrella two-state source contract
  - prove direct-answer/runtime-only handling is preserved
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - open a dedicated worktree for the human-interruption family only
  - inventory current `.freely/intake/**` behavior against the narrowed family definition
  - separate runtime-local resolution from durable-source absorption explicitly
- revisit_trigger:
  - revisit when interruption semantics again drift toward generic catch-all intake, or when the umbrella schema is stable enough for implementation
