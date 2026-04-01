# 候选：workspace-security-capability-baseline-governance

- id: `C-20260401-1308-A`
- candidate_format_version: `v2`
- title: Define reusable workspace security capabilities instead of burying all security logic inside runtime
- source_brainstorm: `docs/pre-brainstorms/20260401-1308--workspace-security-capability-baseline-governance/brainstorms.md`
- problem: Freely has multiple security-relevant concerns across supply chain, secrets, source map exposure, and agent execution, but no reusable capability layer that lets these workflows be invoked, evolved, and audited as explicit skills.
- why_now:
  - the current discussion already separates product baseline from reusable capability
  - without this second lane, Freely risks either hardcoding everything into runtime or leaving the work as one-off operator knowledge
  - the repository already models reusable workflow knowledge as skills, so security capability work has an obvious landing zone
- acceptance_criteria:
  - the capability boundary is explicit and distinct from Freely-self product governance
  - at least one viable skill split is proposed for supply chain, secret/artifact exposure, and agent execution safety
  - the proposal reuses existing capability patterns already present in `docs/system/workspace/skills/**`
  - source map leakage and dependency-age/provenance checks are captured as capability responsibilities, not only product defaults
  - the result is narrow enough to materialize into one or more capability-owned issues
- promotion_gate:
  - prove these responsibilities are long-lived reusable capabilities rather than one-off product wiring
  - avoid restating `init` / `doctor` policy as if it were already a skill contract
  - identify where scripts, references, and skill entrypoints should differ
- open_questions:
  - should the first materialized surface be one aggregate security skill or several narrow skills
  - how much automated remediation should be allowed before human confirmation
  - whether external-content trust-boundary checks belong with MCP/tool safety or URL intake
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repository already models reusable workflow knowledge as skills. Security audit and remediation patterns fit that same capability layer and should not remain runtime-only or conversational folklore.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `proposed`
- decision_reason:
  - Freely needs reusable security capabilities for long-term dogfooding and downstream reuse
  - separating this lane from Freely-self product baseline avoids mixing architecture defaults with optional or composable execution workflows
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - compare the proposed capability families against the current skills index, identify overlaps, and choose the smallest first materialization slice
- revisit_trigger:
  - reopen or split further if a concrete implementation shows that one proposed capability family is too broad or is already absorbed by an existing skill
