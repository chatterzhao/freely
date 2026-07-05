# Candidates - 20260412-1721--develop-push-attempt-followthrough

## Context

- Source brainstorm: `docs/B1-docs/20260412-1721--develop-push-attempt-followthrough/brainstorms.md`
- Status: promoted
- Reopens: the completed develop-push followthrough family through a new bounded execution follow-on

## Candidates

### C-20260412-1721-A
- candidate_format_version: `v2`
- title: Develop push attempt followthrough governance
- problem: Freely currently exposes `push_pending` and escalates its urgency, but a successful `develop` merge still relies on later manual followthrough to actually attempt remote delivery. That leaves local-only canonical truth hanging longer than necessary and fails to distinguish “not yet attempted” from “attempted and blocked.”
- why_now: The repo has repeatedly accumulated local `develop` merges that were lawful but not yet pushed, and the current truth surfaces proved useful but still left the final remote-delivery action dependent on human memory. A bounded single-attempt follow-on now has clear value without reopening hard auto-push.
- acceptance_criteria:
  - a successful `develop` merge automatically triggers one controlled push attempt
  - the push attempt still flows through the existing pre-push gate
  - a blocked attempt writes explicit followthrough truth instead of silently leaving generic `push_pending`
  - blocked attempt truth distinguishes governance/hook block from remote-or-network failure
  - the system does not introduce hidden auto-push or retry-until-success behavior
- fix_approach: Materialize a new follow-on owner, add `freely develop-push attempt`, teach the develop push state model about `push_blocked`, and let `pr-merge-guarded` trigger exactly one post-merge attempt in `develop`.
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260412-1721-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/develop-push-attempt-followthrough-governance/issues/develop-push-attempt-followthrough-governance.md`
- source_brainstorm: `docs/B1-docs/20260412-1721--develop-push-attempt-followthrough/brainstorms.md`
- session_refs: []
- follow_on_to: `I-20260408-1200-A`
- next_action: Land the bounded follow-on owner, wire a single post-merge push attempt through the guarded merge path, and verify both success and blocked writeback behavior through focused regressions.
