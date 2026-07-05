# 候选：build-artifact-exposure-and-release-allowlist-capability

- id: `C-20260401T224500Z-A`
- candidate_format_version: `v2`
- title: Materialize build artifact exposure audit and release allowlist as an automation-first security capability
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- problem: Freely currently relies too much on human memory to catch `.map`, `.env`, secret-bearing files, and unintended build side products before release-facing outputs are consumed. There is no canonical build artifact exposure audit or release allowlist gate in `doctor` or the build path.
- why_now:
  - recent security review confirmed that automation and enforced workflow must replace operator memory where possible
  - the current repo already has a concrete build output surface (`dist/` -> Tauri) that can absorb a narrow first slice immediately
  - this slice is narrow enough to implement without reopening the broader security baseline umbrella
- acceptance_criteria:
  - a reusable build artifact exposure audit script exists
  - the audit rejects obviously forbidden release-facing artifacts such as `.map`, `.env*`, and common secret/certificate files
  - a repo-scoped allowlist defines which build output files are permitted
  - `freely doctor` runs the audit as part of security baseline checking when build output exists
  - the current repo build path automatically runs the audit instead of relying on manual review
  - production build config states its source-map posture explicitly
- promotion_gate:
  - keep the first slice narrow: build artifact exposure and release allowlist only
  - do not widen into full supply-chain or full runtime secret scanning
  - write the contract so later repos can reuse the same audit shape
- open_questions:
  - should future versions support multiple output directories
  - should the allowlist contract later move to a more generic security config surface
  - which additional forbidden artifacts belong in the default pattern set after the first slice lands
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `This is the smallest security capability slice that directly turns “automation over memory” into runnable truth: fail forbidden release artifacts, require an allowlist, and wire the audit into doctor/build.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - this slice directly operationalizes the already-agreed security principle that enforced workflow should replace operator memory
  - current Freely repo topology has an immediate landing zone through `dist/`, `doctor`, and the existing build scripts
  - it remains a sibling capability slice rather than reopening broader product-baseline owners
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/build-artifact-exposure-and-release-allowlist-audit-governance/issues/build-artifact-exposure-and-release-allowlist-audit-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260401T224500Z-A` now owns the first automation-first artifact exposure slice: doctor/build audit, repo allowlist, and explicit production sourcemap posture.
- revisit_trigger:
  - split further if build artifact exposure proves too broad and needs separate source-map or secret-artifact owners
