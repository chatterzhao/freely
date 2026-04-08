# Candidates - 20260407-1042--external-issue-identity-and-publication-boundary

## C-20260407-1042-A

- candidate_format_version: `v2`
- title: `External issue identity, mapping, and publication model after source-family contraction`
- source_brainstorm: `docs/pre-brainstorms/20260407-1042--external-issue-identity-and-publication-boundary/brainstorms.md`
- problem: `After contracting durable source families, Freely needs a family-specific external-issue model that can handle user-created GitHub issues, AI-discovered formalized problems, and external progress writeback without collapsing source identity, public tracking, and internal canonical ownership into one unstable object.`
- why_now:
  - old GitHub issue pre-research mixed too many responsibilities into one line
  - the new source-governance umbrella now explicitly stops at `pre-brainstorm` consumption
  - AI-discovered problems need a formal family lane that is not `human interruption`
- acceptance_criteria:
  - define `external issue` family identity after contraction
  - define how user-created external issues enter the source loop
  - define how AI-discovered durable problems enter the external-issue flow
  - define the relationship among source issue, public tracking issue, and canonical internal owner
  - define minimal mapping and writeback semantics without making GitHub the internal truth source
  - define a label taxonomy that separates identity, platform, and public status concerns
- promotion_gate:
  - prove the result stays compatible with the umbrella source-governance contract
  - prove the result does not collapse human interruption back into generic intake
  - prove internal canonical truth remains in repo docs rather than on GitHub
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
  - open a dedicated worktree for the external-issue family only
  - re-review `20260403-1000--external-issue-integration-and-self-evolution` under the contracted-family model
  - separate source-loop concerns from publication-loop concerns before drafting any GitHub schema or automation
- revisit_trigger:
  - revisit when publication policy, AI-discovered formalization rules, or GitHub mapping semantics need to move from research into implementation
