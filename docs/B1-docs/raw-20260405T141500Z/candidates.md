# Candidates - 20260405-1415--ai-switch-cli-extraction-threshold-and-skeleton-disposition

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260405T141500Z-A: legacy issue
- candidate_format_version: `v2`
- title: ai-switch-cli extraction threshold and skeleton disposition governance
- problem: Freely has already frozen the long-term direction toward a standalone `ai-switch-cli` backend, but there is still no canonical rule for when extraction should start, which implementation pieces must already be stable, or how to treat the local uncommitted skeleton repository that still uses the older `codex-account-switch` name.
- why_now: Without an explicit extraction threshold, the team risks either splitting too early and duplicating unstable slot logic across repos, or keeping backend-specific tool mutation inside Freely longer than necessary. The user also explicitly asked whether the existing local switch repository should be reused and how its current contents should be handled.
- acceptance_criteria:
  - define concrete extraction gates for when Freely should start a dedicated `ai-switch-cli` owner
  - define which helper surfaces must be genericized first, including backup-before-mutation for home-level config rewrites
  - define the disposition policy for the existing local skeleton repository and its outdated `codex-account-switch` naming
  - define whether the skeleton should be renamed in place or discarded in favor of a fresh `ai-switch-cli` repo
  - make the Freely control-plane vs backend split executable enough to guide the first extraction worktree
- promotion_gate:
  - do not reopen the already-frozen Codex slot bundle contract
  - do not claim standalone extraction has started just because a local skeleton directory exists
  - require clear separation between generic backend surfaces and Freely-only orchestration logic
  - avoid copying still-moving Freely shell internals into a new repo before the backend contract is stable
- open_questions:
  - should the first extracted backend continue in shell for parity with current logic, or use a different implementation language once the CLI contract is frozen
  - which current helpers belong in a backend library versus remaining inside Freely control plane
  - should the existing `my-codex-account-switch/codex-account-switch` repository be renamed in place, or replaced with a fresh initialized `ai-switch-cli` repository
  - what is the minimum second-tool evidence required before extraction becomes worth the overhead
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The split threshold is now concrete enough to justify a dedicated follow-on owner. The current skeleton is not yet canonical and should not silently become the backend without an explicit extraction lifecycle.`
    verdict: `ready_for_ibm`
- priority: P1
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason: The question is now narrower than the current Codex verification lane and deserves its own owner so backend extraction timing and skeleton disposition do not stay as informal operator knowledge.
- promoted_issue_path: `docs/B2-docs/ibm/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance/issues/ai-switch-cli-extraction-threshold-and-skeleton-disposition-governance.md`
- next_action: Candidate mirror only. `I-20260405T141500Z-A` is now the canonical `done_ibm` owner for extraction timing, boundary freeze, and skeleton disposition; future extraction work should consume that handoff package instead of reopening candidate research.
- revisit_trigger: Revisit when Codex-first verification is merged, or when a second tool gains verified bundle/probe semantics that make backend extraction economically justified.
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
