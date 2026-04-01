# 候选：freely-product-security-baseline-governance

- id: `C-20260401-1303-A`
- candidate_format_version: `v2`
- title: Freeze Freely product security baseline across init, doctor, runtime, and status surfaces
- source_brainstorm: `docs/pre-brainstorms/20260401-1303--freely-product-security-baseline-governance/brainstorms.md`
- problem: Freely currently has narrow security-adjacent governance slices, but no product-level security baseline that defines what must be configured by default, what must be audited before runtime, and what runtime itself must refuse or constrain.
- why_now:
  - recent supply-chain and agent-execution incidents make ad hoc repo habits insufficient
  - Freely now needs a canonical answer for secrets, dependency intake, artifact exposure, and agent/network permissions instead of leaving these judgments to per-session advice
  - the existing sensitive-artifact ignore owner proves there is real baseline work, but it only covers one narrow slice
- acceptance_criteria:
  - a clear boundary exists between Freely product baseline and reusable security capability work
  - `init`, `doctor`, runtime, and status surfaces each have an explicit proposed security responsibility set
  - the proposal absorbs prior `sensitive-local-artifact-ignore-governance` as one narrow slice rather than treating it as the whole story
  - source map leakage, dependency age / provenance, and secret materialization are represented as first-class baseline topics
  - the output is narrow enough to materialize into one or more focused owner issues rather than a vague umbrella
- promotion_gate:
  - prove the current product truth does not already contain an equivalent end-to-end security baseline
  - keep this lane product-facing; do not collapse into generic skill design
  - identify at least one concrete split between default baseline and optional capability
- open_questions:
  - should `doctor` become a mandatory security gate or a layered advisory surface
  - should `baseline-status` expose security posture summaries directly
  - which parts belong in hooks versus runtime checks
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repo already has a proven narrow sensitive-artifact owner, but it lacks a product-level baseline covering dependency, artifact exposure, and agent execution. This is a real Freely-self architecture gap rather than a duplicate of the existing ignore contract.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `proposed`
- decision_reason:
  - Freely should not ask every downstream project to invent its own security defaults when Freely itself is the runtime and orchestration product
  - this lane should first freeze the product baseline contract before any implementation or skill split
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - compare current `init` / `doctor` / runtime surfaces against the four proposed baseline domains and decide the smallest issue split that can materialize without conflating product governance with reusable skill design
- revisit_trigger:
  - revisit or expand if a current runtime incident shows that one of the proposed baseline domains is still too broad or belongs under an already-active owner issue
