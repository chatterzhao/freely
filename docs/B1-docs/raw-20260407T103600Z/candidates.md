# Candidates - 20260407-1036--human-interruption-source-governance-boundary

## C-20260407T103600Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Human interruption runtime contract after source-family contraction`
- source_brainstorm: `docs/B1-docs/raw-20260407-1036/brainstorms.md`
- problem: `After contracting durable source families, Freely needs a family-specific contract for real human interruptions that preserves runtime durability and manager routing while keeping AI-discovered problems and GitHub publication concerns out of the interruption lane.`
- why_now:
  - current dogfooding habits can blur true human interruption with AI-discovered intake
  - runtime truth already exists under `.freely/intake/**` and is already richer than a raw inbox
  - this is the safest first family-specific slice to refine because it is mostly a boundary clarification / adapter decision, not greenfield invention
- acceptance_criteria:
  - define `human interruption` as real human/operator input only
  - inventory the existing runtime-owned durable shapes under `.freely/intake/**` and `.freely/run/interruption-resolution/**`
  - inventory the already-persisted intake fields and identify which are family-local runtime truth versus candidates for a smaller source-facing view
  - define the family responsibilities split across front-door intake, runtime routing, and canonical owner handoff
  - define the minimal unresolved interruption/source view and manager-visible surface without replacing current runtime truth
  - define claim / resolve / absorb semantics that stay compatible with current runtime behavior, including `delegated` continuation / cleanup handoff
  - define which interruption outcomes remain runtime-local/control-local and which become governed problem-sources
  - explicitly distinguish shared source consumption into `pre-brainstorm` from family-local runtime/control/continuity closure
  - define writeback requirements when a human interruption is consumed into `pre-brainstorm`
  - define the first-slice unresolved-removal/backstop invariant for both pre-brainstorm consumption and runtime-local closure without promoting runtime-local closure into the shared consumed contract
  - prove the first-slice contract against the currently tested closure paths: pre-brainstorm absorption, delegated continuation visibility, manager-continuity absorption, and direct-answer/control closure
- promotion_gate:
  - prove the line does not absorb AI-discovered external-issue responsibilities
  - prove the result stays compatible with the umbrella two-state source contract only at the raw source-view layer
  - prove direct-answer/runtime-only handling is preserved
  - prove the first slice is adapter/overlay-oriented rather than a blind storage replacement
  - prove delegated continuation/local re-entry semantics are preserved
  - prove any provisional unresolved-view fields remain family-local unless umbrella validation later proves them reusable
- open_questions:
  - should the family-local truth remain `.freely/intake/**` with a derived unresolved index, or should a thin adapter document be added alongside it
  - which fields belong on a family-local unresolved source view versus full runtime intake truth
  - how should direct-answer/runtime-local/control-only closures clear unresolved visibility without fake `pre-brainstorm` materialization
  - what exact linkage fields are required when a human interruption is consumed into an existing `pre-brainstorm`
  - whether delegated `handoff://continuation` and `handoff://cleanup` should appear as unresolved source items or as runtime-only unresolved work
- acceptance_reviews:
  - reviewer: `independent runtime review`
    mode: `runtime + tests inventory`
    summary: `Current human interruption/local intake already persists `new|classified|delegated|absorbed|dropped`, resolution artifacts, stale-claim recovery, blocked-supervision writeback, and manager delegated-continuation closure; any first slice must preserve these richer runtime semantics and treat two-state source governance as an overlay only.`
    verdict: `needs_research`
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
  - compare current `.freely/intake/**` and `.freely/run/interruption-resolution/**` shapes against the narrowed family contract
  - freeze the first-slice recommendation around overlay/adapter versus full storage migration
  - explicitly identify which minimal source-facing fields proved reusable enough to feed back into the umbrella shared contract, and which must remain family-local
  - separate runtime-local resolution from governed problem-source consumption explicitly
  - turn the currently tested closure matrix into explicit contract language for: `pre-brainstorm` absorption, `handoff://continuation`, `handoff://cleanup`, direct-answer absorption, and `continuity://manager-supervision`
  - specify the smallest manager-visible unresolved view that can be derived without flattening runtime statuses
  - write the first-slice invariant for unresolved removal / absorption backstop, while keeping umbrella gate scope limited to repo-visible governed-problem absorption claims
- revisit_trigger:
  - revisit when interruption semantics again drift toward generic catch-all intake, or when the umbrella schema is stable enough to test a narrow first implementation slice
