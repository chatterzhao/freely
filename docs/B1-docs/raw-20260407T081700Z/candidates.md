# Candidates - 20260407-0817--source-ledger-routing-and-manager-audit-boundary

## C-20260407T081700Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Source inbox, routing absorption boundary, and manager/worker audit contract`
- source_brainstorm: `docs/B1-docs/raw-20260407-0817/brainstorms.md`
- problem: `Freely lacks a clean problem-source visibility surface distinct from pre-brainstorm registry and runtime-local intake. The right unification target is not “every raw signal”, but “every source that has been judged to be a real governed problem”. Those problem-sources should stay short, remain two-state, and be consumed into pre-brainstorm as the common first digestion step, while analysis continues in pre-brainstorm and downstream canonical artifacts.`
- why_now:
  - current source visibility is fragmented across runtime intake, pre-brainstorms, milestones, reviews, tests, and patrol
  - `docs/B1-docs/raw-INDEX.md` is a registry, not a compact unconsumed inbox
  - protected-root manager work needs a clearer handoff boundary between discovery, dispatch, and canonical writeback
  - status drift between docs and implementation remains a recurring dogfooding problem
- acceptance_criteria:
  - record the current implementation inventory by durable source family and explicitly separate refactor work from net-new capability
  - explicitly separate raw signal handling from durable problem-source handling
  - explicitly separate problem-source visibility from later canonical lifecycle truth
  - explicitly contract the default durable source families to `human interruption` and `external issue`, unless research proves a third family is unavoidable
  - define review/test/runtime anomaly as discovery mechanisms by default rather than durable source families
  - define the anti-loop rule: findings discovered while consuming an existing line stay in that line unless they are genuinely outside its absorbable boundary
  - determine whether a durable source inbox is warranted and, if so, how the contracted durable families should enter it
  - define `consumed` for durable problem-sources as absorption into pre-brainstorm, while keeping later issue/progress/recovery movement as downstream lifecycle progression rather than source consumption
  - keep source state itself two-state only and avoid intermediate source statuses
  - keep source documents short and source-like, while putting analysis in pre-brainstorm or downstream canonical artifacts
  - define that review/test artifacts do not enter the source pool merely by existing; only newly discovered independent problems may create a new durable source
  - identify the narrowest first implementation slice, and prove which non-first-slice discovery mechanisms or source families stay out of scope
  - define a manager-first visibility contract that stays small without blinding manager patrol to runtime, fleet, recovery, or arbitration truth
  - define when worker status-vs-reality audit is mandatory versus optional, and keep that audit route-scoped rather than manager-global by default
  - identify the smallest viable hook/gate backstop for source-inbox alignment without over-gating runtime-local event churn
- promotion_gate:
  - prove the current partially implemented human-intake/runtime path is being refactored rather than replaced blindly
  - prove the proposal does not create a second orchestration truth surface parallel to milestones and canonical lifecycle artifacts
  - prove the routing contract stays compatible with existing `PROJECT_INTENT` and `LAWS`
  - prove milestone remains an orchestration surface rather than being reinterpreted as a raw-source queue
  - prove the proposal preserves the distinction between raw signals that never become governed problems and problem-sources that must enter pre-brainstorm
  - identify at least one bounded implementation slice if a durable source-inbox layer is still judged worthwhile
  - keep expansion beyond `human interruption` and the linked `external issue` research line out of the first slice unless new evidence proves the narrowed model cannot carry the needed contract
- open_questions:
  - should the live unresolved source inbox live under `~/.freely/projects/<project-hash>/`, project `.freely/**`, or a mixed adapter model
  - should current human interruption storage remain family-local runtime state with an unresolved-index overlay, or be rehomed into a more general project-global local source inbox for the contracted durable families
  - how should this work align with the older GitHub issue pre-research in `docs/B1-docs/raw-20260403-1000/**`, instead of silently replacing or duplicating it
  - is there any durable family beyond `human interruption` and `external issue` that truly cannot be modeled as one of those two
  - how should one source map to multiple owners or multiple sources collapse into one owner
  - what is the exact first slice: schema only, storage boundary only, human-intake refactor, or gate backstop
- acceptance_reviews:
  - reviewer: `Pauli`
    mode: `independent review`
    summary: `Current runtime intake is a richer persisted state machine than the proposed two-state governance simplification, so any two-state model must stay narrowly scoped to a raw inbox layer rather than replacing runtime or lifecycle truth.`
    verdict: `needs_research`
  - reviewer: `Avicenna`
    mode: `independent review`
    summary: `Current gates strongly validate source_candidate and milestone linkage, but they do not yet validate interruption/source absorption into canonical repo artifacts, which makes narrow backstop work plausible.`
    verdict: `needs_research`
  - reviewer: `Leibniz`
    mode: `independent review`
    summary: `A raw source ledger may help, but forcing all sources through pre-brainstorm or collapsing governance truth to consumed/unconsumed would conflict with existing routing and lifecycle law.`
    verdict: `needs_research`
  - reviewer: `Feynman`
    mode: `independent review`
    summary: `A blanket top-level docs/sources tree is likely too broad and would blur runtime-local signals, issue-bound evidence, and durable governance records into one parallel queue.`
    verdict: `needs_research`
  - reviewer: `Lorentz`
    mode: `independent review`
    summary: `The proposal overreaches if it collapses manager visibility to two documentary surfaces or makes every worker perform a manager-grade audit-first patrol; current truth requires runtime/fleet-first manager patrol and route-scoped worker checks.`
    verdict: `needs_research`
- priority: `P1`
- status: `needs_research`
- decision_reason:
  - the underlying problem is real, but the strong version of the redesign is not yet architecture-safe
  - the repo already has a partial human-intake/runtime implementation, so the right next step is a narrower boundary decision rather than a repo-wide reinvention
  - this governance line should stop at pre-brainstorm intake: it owns how sources become governed problems and enter pre-brainstorm, not the full downstream issue lifecycle
  - manager visibility simplification, source absorption tracking, and worker audit duty should be designed together, not patched independently
  - current repo truth is plural at the raw-signal layer, but the durable source model should stay narrow: default to `human interruption` and `external issue`, and treat review/test/runtime anomaly as discovery mechanisms unless they expose a genuinely independent new problem
  - once a durable source is judged to be a real governed problem, pre-brainstorm should become its common first consumption step
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - finish the current-state inventory by durable source family and freeze non-first-slice mechanisms as contract-clarification only unless new evidence appears
  - rewrite the schema and gate discussion around the contracted durable families: `human interruption` and `external issue`
  - decide whether Freely should introduce a narrow durable problem-source inbox layer at all, or instead only strengthen source-routing contracts and gate checks around existing artifacts
  - use `human interruption` as the first proving lane before promoting any generic source schema; treat reusable schema as a derivative outcome, not an independent architecture-first freeze
  - if such an inbox remains desirable, define the contract/location boundary first: contract truth versus live unresolved source documents versus runtime-local control-plane evidence
  - explicitly link and compare the GitHub issue family against `20260403-1000--external-issue-integration-and-self-evolution`, because that line already proposed scan/create/sync/mapping semantics but is still pre-research-only today
  - define review/test/runtime-anomaly discovery rules so current-line absorption wins by default and only genuinely independent new problems create a new durable source
  - keep hook/gate design source-family-specific at the raw-signal boundary, but align the contracted durable families on one common rule: once recognized as a governed problem, they are consumed into pre-brainstorm
  - bias the first materialization slice toward human interruption / local governance intake; only place unresolved-index removal backstop after that slice has made the removable artifact legible
- revisit_trigger:
  - revisit when there is a concrete bounded proposal for the first source family and its storage boundary, or when another dogfooding incident proves the current source visibility gap cannot be solved by tightening existing pre-brainstorm/milestone/routing contracts alone

## C-20260407T081700Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Family-validated minimal source view and unresolved-index contract`
- source_brainstorm: `docs/B1-docs/raw-20260407-0817/brainstorms.md`
- problem: `Freely still lacks a stable minimal contract for a durable source-facing view and corresponding unresolved index, but freezing that contract as a generic architecture before any family proves it would over-abstract past current runtime truth. The contract must therefore be derived from a first validated family slice, then narrowed to the reusable subset only if that subset survives contact with reality.`
- why_now:
  - the umbrella research now rejects repo-wide rollout and needs a bounded first slice
  - current `human interruption` runtime truth is rich enough to expose where a shared source-view contract is actually reusable and where it is not
  - storage and gate decisions still need a contract, but that contract should be provisional-and-family-validated before it becomes a generic owner
- acceptance_criteria:
  - define the smallest source-facing field set that survives validation against the first family slice without replacing family-local runtime truth
  - define unresolved-index fields and guarantee it only carries active unresolved items
  - define `unconsumed` and `consumed` semantics without introducing intermediate source states
  - define the minimum canonical-owner linkage fields around the contracted durable source families, with `consumed` meaning absorbed into pre-brainstorm
  - define which fields belong in a reusable source-facing view versus family-local runtime truth versus pre-brainstorm / owner artifacts
  - explicitly record which candidate fields remain family-specific and therefore should not be frozen into the shared contract yet
- promotion_gate:
  - prove the contract is derived from at least one validated family slice rather than frozen in isolation
  - prove the contract fits current human-intake/runtime truth without replacing runtime state machines
  - prove the contract does not reinterpret milestone as a raw-source queue
  - prove the contract can reference GitHub issue lineage without assuming GitHub automation already exists
- open_questions:
  - should the unresolved index be a single file or a generated view over source documents
  - what is the smallest canonical-owner linkage shape that still supports later gate checks
  - how should one source reference multiple owners, if at all
  - should the schema encode only the two default durable families now, leaving later family expansion as an explicit schema revision
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260407T081700Z-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - derive a provisional reusable source-view contract from the first `human interruption` slice instead of freezing a generic schema in isolation
  - test the provisional contract against human interruption as the proving lane and external issue lineage as a boundary case, while keeping review/test/runtime anomaly as non-default discovery mechanisms
  - promote only the subset that remains reusable after family validation; leave family-specific fields in the family contracts
- revisit_trigger:
  - revisit when the first family slice has made a reusable subset legible enough to promote into a shared contract, or when family validation shows the shared layer should remain only invariant-level

## C-20260407T081700Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Human interruption and local intake alignment with narrow source contract`
- source_brainstorm: `docs/B1-docs/raw-20260407-0817/brainstorms.md`
- problem: `Current .freely/intake/** and interruption resolution already provide partial durable source behavior, but the writeback semantics and manager-facing unresolved view are runtime-oriented rather than the narrowed source contract now under review.`
- why_now:
  - this is the strongest first implementation family because runtime truth already exists
  - it offers a proving ground without dragging GitHub issue implementation or discovery-mechanism governance into one rollout
- acceptance_criteria:
  - preserve current interruption-manager triage behavior and runtime-local durability
  - align human interruption/local intake writeback with the narrowed source-document contract
  - define whether current `.freely/intake/**` remains the family-local truth with an overlay index or becomes an adapter into a broader local source layer
  - expose a small manager-visible unresolved view without regressing manager patrol over runtime/fleet truth
- promotion_gate:
  - prove the refactor is additive/narrowing and does not break current interruption handling behavior
  - prove the result is still compatible with protected-root manager dispatch and dedicated-worktree canonical writeback
  - prove the design does not force direct-answer/runtime-local resolutions into repo-doc materialization
- open_questions:
  - overlay versus migration for current `.freely/intake/**`
  - whether the first slice needs project-global local storage or only a cleaner manager-facing view
  - how interruption resolution artifacts should link back into the narrowed source contract
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260407T081700Z-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - compare current `.freely/intake/**`, interruption claim/resolve flow, and interruption-resolution artifacts against a provisional source-facing contract derived from this family
  - identify the smallest viable refactor that introduces manager-visible unresolved truth without broad storage migration
  - keep the slice explicitly compatible with later `external issue` alignment, but do not widen it to review/test/runtime-anomaly ingestion
- revisit_trigger:
  - revisit when the family slice has either produced a reusable shared subset for 0817-B or shown that the shared contract must remain narrower than originally expected

## C-20260407T081700Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Stage-based source absorption backstop`
- source_brainstorm: `docs/B1-docs/raw-20260407-0817/brainstorms.md`
- problem: `Current governance gates validate candidate/milestone/owner chains, but they do not yet provide a narrow backstop that verifies a durable source item actually leaves the unresolved queue once canonical absorption is claimed.`
- why_now:
  - the real dogfooding pain includes fake closure and stale unresolved truth
  - current gate stack already provides a lifecycle-aware base that can be extended narrowly
- acceptance_criteria:
  - define which stage checks source existence/linkage, which checks unresolved-index exit, and which only backstops repo-visible claims
  - keep closure semantics durable-family-aware and avoid one universal move rule
  - scope the first enforcement path to durable source-inbox entries only
  - preserve existing candidate -> milestone -> owner gating
- promotion_gate:
  - prove the backstop extends the current gate stack rather than creating a second orchestration gate
  - prove it does not over-gate runtime-local churn
  - prove it is compatible with the first-slice human interruption/local-intake family
- open_questions:
  - exact stage placement: pre-brainstorm, owner materialization, merge-time, or a mix
  - whether unresolved-index removal should be checked at issue materialization time or only at protected-branch merge time
  - how to represent allowed non-repo absorption targets such as direct-answer/runtime-local resolutions
- priority: `P1`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- dependencies:
  - `C-20260407T081700Z-A`
  - `C-20260407T081700Z-C`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - map the proposed source backstop onto the existing gate stack only after the first `human interruption` slice makes the removable unresolved artifact explicit
  - keep the first enforcement path on human interruption/local intake, and treat external issue linkage as follow-on reconciliation with the existing 20260403 pre-research line
  - do not widen first-stage enforcement to review/test/runtime-anomaly discovery events
- revisit_trigger:
  - revisit when the first-slice human-intake alignment has made gate placement and removable-artifact semantics concrete enough to backstop without inventing a second orchestration surface
