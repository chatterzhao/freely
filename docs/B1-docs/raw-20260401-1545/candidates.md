# 候选：acp-client-agent-protocol-runtime-adoption

- id: `C-20260401-1545-A`
- candidate_format_version: `v2`
- title: Materialize ACP as an optional adapter boundary between Freely and external code agents
- source_brainstorm: `docs/B1-docs/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- problem: Freely already orchestrates multiple external code agents, but the current integration surface is tool-specific. Session semantics, permission handling, and tool/runtime adapters differ across canonical tools such as `codex`, `kiro-cli`, and `iflow`, plus experimental current implementations such as `cc`. ACP may offer a more uniform client-to-agent contract, but it is still unclear whether that benefit outweighs bridge cost, token overhead, and mismatch with Freely's autonomy-first governance.
- why_now:
  - Freely has already materialized multi-tool runtime governance, slot contracts, session continuity, and auto-approve paths, so the adapter layer is now visible as a distinct concern
  - current external tooling is heterogeneous enough that session, permission, and tool-call contracts are increasingly duplicated per tool
  - if ACP is useful, it should be introduced as a bounded adapter study before more tool-specific glue accumulates
- acceptance_criteria:
  - compare ACP against the current Freely runtime approach specifically in the `Freely client -> external code agent` context
  - distinguish clearly which concerns belong to ACP and which must remain Freely-owned governance
  - evaluate ACP against at least token overhead, session model, continuity/memory, permission handling, and multi-agent extensibility
  - define whether ACP should be rejected, kept as optional adapter research, or promoted toward a narrow prototype bridge
  - define the minimum Freely-side adapter contract that any ACP evaluation must satisfy
  - define the recommended adapter architecture for Freely: `direct`, `acp`, and per-tool selection policy
  - define the issue-level acceptance shape that a future ACP prototype owner would need, without treating that prototype execution as candidate-level acceptance
  - make explicit whether a future prototype requires a first-class adapter axis before any `direct/acp` dual-path implementation can be judged fairly
- promotion_gate:
  - do not treat ACP as a replacement for three-loop governance, worktree governance, or recovery truth
  - do not assume ACP automatically solves auto-approve, risk routing, or autonomous committee review
  - do not require existing tools to migrate in one batch
  - only promote if the bounded adapter benefits are clearer than the bridge/maintenance cost
  - prefer a narrow prototype or contract mapping over a whole-runtime rewrite
  - keep `direct` as a first-class fallback even if ACP is adopted for some tools
  - distinguish clearly between current repo tools, experimental current implementations, and future speculative tool targets
- open_questions:
  - which concrete future tools are the best first prototype targets if they expose ACP cleanly
  - whether `cc-use-codex-cli` should be modeled as one agent endpoint with nested capability, or two agent layers
  - whether ACP reduces enough adapter duplication to justify bridge maintenance for tools that do not natively speak ACP
  - whether ACP's permission/session model can coexist cleanly with Freely's non-interactive `auto` mode and future risk-aware approval planner
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `ACP appears valuable as an optional adapter boundary, but not as a replacement for Freely's governance and continuity truth.`
    verdict: `needs_more_research`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- expected_outcome:
  - a bounded judgement on whether ACP should enter Freely as a real adapter-layer capability
  - a clear boundary between ACP-owned communication concerns and Freely-owned autonomy/governance concerns
  - a minimal Freely adapter contract that can later drive prototype evaluation
  - a clear dual-path adapter conclusion: `direct` remains first-class, ACP stays optional and per-tool selectable
  - a prototype-ready issue-level acceptance shape: existing direct tools can opt into ACP, and new tools can be onboarded by either adapter path
  - a clear statement of prototype preconditions, including whether a dedicated adapter axis must exist first
- decision_reason:
  - Freely's strongest current value is autonomy governance, not transport standardization, so ACP must be evaluated as an adapter concern rather than an architecture rewrite
  - the current multi-tool runtime has matured enough that integration heterogeneity is now a concrete problem worth isolating
  - a bounded pre-brainstorm is safer than prematurely materializing ACP into runtime work before the contract mismatch is understood
  - the emerging stable answer is dual-path architecture rather than mandatory ACP migration
  - the candidate must stay at research-boundary level and not absorb future prototype execution acceptance
- next_action:
  - this candidate is now materialized as `I-20260401-1545-A`; the active owner freezes the adapter boundary, issue-level acceptance shape, and implementation handoff for a future dual-path prototype
- revisit_trigger:
  - re-open candidate-level research only if the issue-bound ACP contract fails to remain stable, or if ACP no longer fits the external code-agent boundary assumed by this materialization
