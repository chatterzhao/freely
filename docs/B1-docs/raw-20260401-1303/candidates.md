# 候选：freely-product-security-baseline-governance

- id: `C-20260401-1303-A`
- candidate_format_version: `v2`
- title: Freeze Freely product security baseline across init, doctor, runtime, and status surfaces
- source_brainstorm: `docs/B1-docs/20260401-1303--freely-product-security-baseline-governance/brainstorms.md`
- problem: Freely currently has narrow security-adjacent governance slices, but no product-level security baseline that defines how default unattended automatic approval must be disclosed, what must be detected and acknowledged during init, how Freely policy maps into tool-specific configuration and launch-time injection, what must be configured by default, and what must be audited before runtime.
- why_now:
  - recent supply-chain and agent-execution incidents make ad hoc repo habits insufficient
  - Freely now needs a canonical answer for default autonomous execution, tool-configuration mapping, secrets, dependency intake, artifact exposure, and agent/network permissions instead of leaving these judgments to per-session advice
  - the existing sensitive-artifact ignore owner proves there is real baseline work, but it only covers one narrow slice
  - the product direction is owner-grade AI autonomy, so Freely needs an explicit answer for activation consent, internal decision escalation, and minimal-risk behavior instead of drifting into ad hoc human re-approval
- acceptance_criteria:
  - a clear boundary exists between Freely product baseline and reusable security capability work
  - `init`, `doctor`, runtime, and status surfaces each have an explicit proposed security responsibility set
  - the proposal explicitly treats unattended automatic approval as a Freely product default implementation posture rather than a downgraded optional mode
  - the proposal explains how Freely canonical policy, tool adapter injection, and project-local tool configuration should relate
  - the proposal defines activation consent, autonomous escalation, and minimal-risk-state behavior in a way that preserves autonomy-first product intent
  - the proposal makes clear that safeguard guidance such as sandboxing or isolated devices is strongly recommended and supported, but default activation blocking is tied to informed consent rather than safeguard completeness
  - the proposal absorbs prior `sensitive-local-artifact-ignore-governance` as one narrow slice rather than treating it as the whole story
  - source map leakage, dependency age / provenance, secret materialization, execution-boundary posture, and runtime state artifacts are represented as first-class baseline topics
  - the output is narrow enough to materialize into one or more focused owner issues rather than a vague umbrella
- promotion_gate:
  - prove the current product truth does not already contain an equivalent end-to-end security baseline
  - keep this lane product-facing; do not collapse into generic skill design
  - identify at least one concrete split between default baseline and optional capability
- open_questions:
  - should non-sandbox autonomous execution be handled as informed-consent posture or as single-purpose explicit-enable posture
  - should `doctor` become a mandatory security gate or remain a layered advisory surface with selective explicit-enable checks only for exceptional capabilities
  - should `baseline-status` expose security posture summaries directly
  - which parts belong in hooks versus runtime checks
  - how should security-focused subagents participate when Freely needs internal multi-agent review without restoring user-step approvals
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repo already has a proven narrow sensitive-artifact owner, but it lacks a product-level baseline covering dependency, artifact exposure, and agent execution. This is a real Freely-self architecture gap rather than a duplicate of the existing ignore contract.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - Freely should not ask every downstream project to invent its own security defaults when Freely itself is the runtime and orchestration product
  - this lane should first freeze the product baseline contract before any implementation or skill split
  - because Freely defaults to autonomous execution, it must define a canonical informed-consent and configuration-mapping path instead of leaving users to infer execution risk from downstream tool flags
  - Freely should support safer environments aggressively without turning safeguard incompleteness into the default blocker for owner-grade autonomy
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
- promoted_issue_path_role: `primary-owner-for-split-candidate`
- promoted_issue_paths:
  - `docs/epics/freely-product-architecture/default-autonomy-activation-consent-and-tool-policy-governance/issues/default-autonomy-activation-consent-and-tool-policy-governance.md`
  - `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/issues/freely-tool-autonomy-policy-materialization-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260401-1303-A` now owns default autonomy posture, activation consent, runtime decision escalation, minimal-risk-state semantics, and product-level posture truth; sibling owner `I-20260401-1303-A-2` owns tool policy materialization, project-local versus launch-time config mapping, and the current Codex posture split.
  - Reusable security-capability follow-ons now materialize separately: `I-20260401-2245-A` covers build artifact exposure/release allowlist audit, and `I-20260401-0115-A` covers supply-chain baseline/install-intake audit.
- revisit_trigger:
  - reopen only if a remaining baseline domain still lacks a dedicated owner after these split follow-ons, or if a current runtime incident shows the product-level split is still too broad
