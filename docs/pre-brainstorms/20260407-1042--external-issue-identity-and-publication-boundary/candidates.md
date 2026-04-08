# Candidates - 20260407-1042--external-issue-identity-and-publication-boundary

## C-20260407-1042-A

- candidate_format_version: `v2`
- title: `External issue identity, mapping, and publication model after source-family contraction`
- source_brainstorm: `docs/pre-brainstorms/20260407-1042--external-issue-identity-and-publication-boundary/brainstorms.md`
- problem: `After contracting durable source families, Freely needs a family-specific external-issue model that can handle user-created GitHub issue style inputs and AI-discovered problems that deserve formal external publication, without collapsing durable source identity, public-progress mirroring, and internal canonical ownership into one unstable GitHub object or one overloaded owner family.`
- why_now:
  - the older `20260403-1000` GitHub issue pre-research explored useful mapping ideas, but mixed source ingestion, publication, internal owner truth, and self-evolution scheduling too broadly
  - the newer source-governance umbrella now explicitly narrows durable source families to `human interruption` and `external issue`, which makes the external-issue family boundary first-class
  - AI-discovered problems need a bounded rule for when they formalize into external-issue lineage instead of being treated as raw human interruption or generic runtime noise
- acceptance_criteria:
  - define `external issue` family identity after contraction and separate `source loop`, `owner loop`, and `publication loop`
  - define how user-created GitHub issue style inputs enter the source loop
  - define when AI-discovered problems qualify for external-issue formalization, and when they remain internal-only
  - define the relationship among `source issue`, optional `publication target`, and canonical internal owner
  - define a minimum mapping contract that supports `source_ref`, `internal_owner_ref`, `publication_ref`, and bounded `publication_mode` without freezing implementation storage too early
  - define mapping invariants that keep `internal owner` canonical even when `source issue` and `publication target` coincide
  - define a formalization decision table for user-created versus AI-discovered external-issue entry, including internal-only, source-only, and source-plus-publication cases
  - define a label taxonomy whose dimensions are explicitly separated:
    - identity / role
    - publication policy
    - public status
  - define GitHub writeback boundaries for comments, labels, closeout, and “no writeback” cases without making GitHub the internal truth source
  - define the minimum publication policy distinctions among:
    - externally-created issue reused as source-only/public surface
    - externally-created issue plus separate public tracking issue
    - AI-discovered issue kept internal-only
    - AI-discovered issue later published externally
  - critically re-review `20260403-1000--external-issue-integration-and-self-evolution` and preserve only the parts that remain governance-safe under the contracted-family model
  - produce an explicit keep / split / reject table for `20260403-1000` so later work does not silently re-import bundled assumptions
  - define the minimum consumption / dedupe evidence needed to prevent already-consumed external source issues from being re-scanned as fresh intake
- promotion_gate:
  - prove the result stays compatible with the umbrella source-governance contract and does not reopen a generic repo-wide source-ledger rollout by stealth
  - prove the result does not collapse `human interruption` back into generic intake, and does not collapse AI-discovered problems into “always publish externally”
  - prove internal canonical truth remains in repo docs rather than on GitHub
  - prove the family does not assume GitHub create/sync automation already exists in runtime or manager paths
  - prove any recommended status vocabulary is publication-facing only and not a second `phase_state`
  - prove the first slice can remain storage-agnostic if mapping invariants are stable, instead of forcing premature `.freely/*` local-state design
- open_questions:
  - under what explicit policy may `source issue` and `publication target` be the same external object?
  - what minimum public-status vocabulary is stable enough to expose without leaking internal owner semantics?
  - what durable evidence should the owner loop record when an AI-discovered problem is intentionally kept internal-only?
  - is a canonical mapping artifact required in the first slice, or can storage stay deferred until a later GitHub-first policy/schema owner?
- acceptance_reviews:
  - reviewer: `human`
    verdict: `supports-with-boundary-tightening`
    note: The candidate is viable if it freezes loop separation, canonical owner truth, and publication limits first; it becomes unsafe again if GitHub labels or local mapping files are chosen before those invariants are explicit.
- decision_reason:
  - external-issue handling now sits on the source-storage boundary and cannot be reduced to a GitHub sync implementation detail
  - the highest-risk failure mode is lifecycle collapse, where source, owner, and publication silently become the same object
  - freezing boundary semantics before storage or automation choices is the lowest-risk path to a governance-compatible first slice
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
  - finish the GitHub-first policy review for `source issue` vs optional `publication target` vs internal owner
  - rewrite the old `20260403-1000` conclusions into an explicit keep/split/reject table, instead of silently inheriting its bundled assumptions
  - freeze a formalization decision table for user-created versus AI-discovered external-issue entry before choosing storage or automation
  - define the minimum dedupe/consumption evidence contract that keeps already-consumed external issues from re-entering intake
  - decide the minimum conceptual mapping fields and publication modes before proposing any local storage artifact or GitHub automation lane
  - keep this line pre-research-only until the loop split and writeback boundaries are stable enough for a bounded policy/schema owner
- revisit_trigger:
  - revisit when publication policy, AI-discovered formalization rules, GitHub mapping semantics, or public-status vocabulary are stable enough to materialize a bounded GitHub-first policy/schema owner
