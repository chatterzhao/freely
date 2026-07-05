# Candidates - 20260419-1505--runtime-supervisor-attach-reuse-followthrough

- Source brainstorm: `docs/B1-docs/raw-20260419-1505/brainstorms.md`

### C-20260419-1505-A

- title: `Runtime supervisor attach reuse followthrough`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- candidate_status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- problem: `The checkpoint branch still carries healthy supervisor reuse/attach behavior and Claude runtime-home isolation that are not owned by any canonical lifecycle artifact.`
- why_now:
  - repeated attach/reuse logic should not remain branch-local truth
  - the checkpoint worktree is still active and should either promote or be explicitly dropped
  - the added regression tests already define a bounded, verifiable seam
- proposed_scope:
  - reuse healthy same-project supervisors from `freely daemon start`
  - attach foreground `freely start` to a live supervisor between AI cycles and when `ps` is unavailable but cwd ownership is still provable
  - isolate Claude launcher HOME under the project runtime directory
- non_goals:
  - broader runtime startup architecture redesign
  - reopening interruption-manager followthrough scope from other checkpoint owners
  - memark protected-root bootstrap work
- promoted_issue_id: `I-20260419-1505-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-supervisor-attach-reuse-followthrough-governance/issues/runtime-supervisor-attach-reuse-followthrough-governance.md`
- next_action: `Candidate mirror only. I-20260419-1505-A is now the canonical owner for the preserved supervisor attach/reuse checkpoint and its launcher-home isolation followthrough.`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
