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
  - define a label taxonomy whose dimensions are explicitly separated:
    - identity / role
    - publication policy
    - public status
  - define GitHub writeback boundaries for comments, labels, closeout, and “no writeback” cases without making GitHub the internal truth source
  - critically re-review `20260403-1000--external-issue-integration-and-self-evolution` and preserve only the parts that remain governance-safe under the contracted-family model
- promotion_gate:
  - prove the result stays compatible with the umbrella source-governance contract and does not reopen a generic repo-wide source-ledger rollout by stealth
  - prove the result does not collapse `human interruption` back into generic intake, and does not collapse AI-discovered problems into “always publish externally”
  - prove internal canonical truth remains in repo docs rather than on GitHub
  - prove the family does not assume GitHub create/sync automation already exists in runtime or manager paths
  - prove any recommended status vocabulary is publication-facing only and not a second `phase_state`
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
  - decide the minimum conceptual mapping fields and publication modes before proposing any local storage artifact or GitHub automation lane
  - keep this line pre-research-only until the loop split and writeback boundaries are stable enough for a bounded policy/schema owner
- revisit_trigger:
  - revisit when publication policy, AI-discovered formalization rules, GitHub mapping semantics, or public-status vocabulary are stable enough to materialize a bounded GitHub-first policy/schema owner
