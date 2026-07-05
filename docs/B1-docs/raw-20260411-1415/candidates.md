# 候选：pretests-adequacy-item-schema-materialization

- id: `C-20260411-1415-A`
- candidate_format_version: `v2`
- title: Materialize richer pre-tests adequacy item schema without introducing parallel test truth
- source_brainstorm: `docs/B1-docs/20260411-1415--pretests-adequacy-item-schema-materialization/brainstorms.md`
- problem: `pre-tests.md` is already the canonical test truth, but executable gates still mostly consume the minimal five acceptance-item fields (`id/requirement/evidence_level/status/artifact_ref`). This can prove that some tests ran, but cannot reliably prove that enough tests ran for the intended lane and promotion gate.
- why_now:
  - repeated misses are now concentrated in adequacy discrimination, not lane existence or basic evidence binding
  - richer schema intent (`surface_kind/target_lane/promotion_gate/task_refs/case_design`) already exists in pre-brainstorm and owner truth but is under-materialized in executable gates
  - this can be upgraded incrementally with low regression risk if phase-gated
- acceptance_criteria:
  - freeze an adequacy item v2 schema that keeps the existing five required fields and defines richer adequacy metadata
  - add gate diagnostics that can classify `not-run` vs `run-but-insufficient` vs `sufficient-with-evidence`
  - define and implement a phased enforcement path: warn-first, then hard-gate for new owners, then selected hard fields for develop-bound promotion
  - codify that `pre-tests.md` remains the only canonical file and no `tests.md`-like parallel file is introduced
  - land focused regressions that prove backward compatibility for old items and stronger enforcement for new materialized owners
- promotion_gate:
  - do not widen this owner into runtime launch hard-gating; focus only on adequacy item schema materialization
  - do not attempt all-history migration in phase one
  - preserve current passing paths for legacy owners until phase policy says otherwise
- open_questions:
  - whether `task_refs` should be mandatory at phase two or phase three
  - whether `case_design` should start as structured string blocks or a stricter key-value mini-schema
  - whether `promotion_gate` values should include `post_merge_followthrough` directly or keep it under `retirement` workflow first
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The missing layer is machine-readable adequacy semantics. Minimal-field checks are necessary but not sufficient to determine whether issue-required testing is complete.`
    verdict: `ready_for_materialization`
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason:
  - this gap directly explains why "ran tests" and "ran enough tests" are conflated at gate time
  - the change can be delivered incrementally with low functional regression risk
  - it strengthens canonical `pre-tests.md` usage rather than adding new document surfaces
- next_action:
  - candidate mirror only. `I-20260411-1415-A` is now the canonical owner for schema v2 + phased gate enforcement.
  - keep launch-time hard-gate and retirement-gate expansion as separate follow-on owners
- promoted_issue_path: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/issues/pretests-adequacy-item-schema-materialization-governance.md`
- revisit_trigger:
  - another issue passes minimal acceptance-item structure but still escapes due to missing adequacy semantics
  - team pressure to add a second test truth file (`tests.md`) reappears due to schema underfit
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
