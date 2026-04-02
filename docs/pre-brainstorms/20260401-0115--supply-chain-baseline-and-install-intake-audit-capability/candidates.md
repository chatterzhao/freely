# 候选：supply-chain-baseline-and-install-intake-audit-capability

- id: `C-20260401-0115-A`
- candidate_format_version: `v2`
- title: Materialize automation-first supply-chain and install-intake baseline audit
- source_brainstorm: `docs/pre-brainstorms/20260401-0115--supply-chain-baseline-and-install-intake-audit-capability/brainstorms.md`
- problem: Freely still lacks a canonical automation-first audit for lockfile presence, risky install lifecycle scripts, non-registry dependency specifiers, and mutable GitHub Actions refs. That leaves a real security baseline topic trapped in human review memory.
- why_now:
  - the broader security baseline explicitly called out supply-chain, install script, and mutable action ref risk
  - adjacent owners already proved the repo can absorb narrow automation-first security slices without reopening the whole umbrella
  - this slice is small enough to land directly in `doctor` and reusable scripts now
- acceptance_criteria:
  - a canonical supply-chain baseline audit script exists
  - the audit fails when a repo with `package.json` lacks a root lockfile
  - the audit fails when package manifests use disallowed direct dependency specifiers such as `git+`, `github:`, `http(s):`, `file:`, or `link:`
  - the audit fails when package manifests define install-time lifecycle scripts such as `preinstall`, `install`, `postinstall`, or `prepare` unless the script name is explicitly allowlisted
  - the audit fails when GitHub Actions external `uses:` refs are pinned to mutable tags instead of full commit SHAs
  - `freely doctor` replays the same audit as part of baseline checking
- promotion_gate:
  - keep the first slice narrow: root lockfile, direct specifier, install script, and workflow pinning only
  - do not widen into minimum package age, provenance, or CVE intelligence
  - do not absorb artifact exposure or execution-boundary review slices that already have dedicated owners
- open_questions:
  - whether later slices should support policy config rather than hard-coded baseline deny rules
  - whether mutable GitHub Action pinning should eventually cover composite/local action exceptions more richly
  - whether minimum package age and provenance should become a sibling or a second phase of the same capability family
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `This is the next narrow security capability slice that directly operationalizes automation-over-memory without reopening the full security umbrella.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - the remaining supply-chain baseline topics are real and current, not stale wishlist items
  - a focused audit plus doctor integration closes an actual gap while preserving narrow owner boundaries
  - this slice creates reusable machine-enforced truth that future CI or hooks can call directly
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/issues/supply-chain-baseline-and-install-intake-audit-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260401-0115-A` now owns the narrow supply-chain baseline slice: root lockfile presence, direct dependency intake baseline, explicit lifecycle allowlist enforcement, mutable GitHub Action ref rejection, and `doctor` enforcement.
- revisit_trigger:
  - reopen or split further if minimum package age, provenance, or transitive vulnerability policy needs to materialize as a separate capability family
