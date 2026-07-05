# Candidates - 20260419-2245--runtime-claude-launch-and-session-evidence

- Source brainstorm: `docs/pre-brainstorms/20260419-2245--runtime-claude-launch-and-session-evidence/brainstorms.md`

### C-20260419-2245-A

- title: `Runtime Claude launch and session evidence governance`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- candidate_status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `Freely can switch into a Claude-family fallback path whose print-mode argv contract is wrong under --add-dir, and it can also preserve Claude session ids as resumable targets without verified session evidence.`
- why_now:
  - protected-root replay showed the fallback was broken even when the Claude CLI itself was available
  - manual `say hi` reproduction proved the failure is in Freely's launch syntax, not only in external tool availability
  - stale resume targets make short-lived exec-style tools look alive after the child process is already gone
- proposed_scope:
  - pass Claude-family print-mode prompts through stdin when the runtime launches non-interactively
  - treat Claude resume targets as valid only when project-local session evidence exists
  - rotate or clear stale Claude session anchors when fresh execution produced no verified evidence
- non_goals:
  - redesign generic worker/supervisor heal behavior
  - lock the runtime to `codex`-only behavior
  - widen the owner into all fallback-tool selection policy
- promoted_issue_id: `I-20260419-2245-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-claude-launch-and-session-evidence-governance/issues/runtime-claude-launch-and-session-evidence-governance.md`
- next_action: `Candidate mirror only. I-20260419-2245-A is now the canonical owner for the Claude-family non-interactive launch and verified session-evidence repair.`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
