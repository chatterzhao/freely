# Candidates: runtime forensic time alignment and stall observability

## Candidate

- id: `C-20260412T184500Z-A`
- candidate_format_version: `v2`
- title: `Runtime forensic time alignment and stall recovery observability`
- source_brainstorm: `docs/B1-docs/raw-20260412-1845/brainstorms.md`
- problem: `Freely already governs human-readable time display, but cross-surface runtime forensics still lack a canonical alignment contract. UTC runtime events, host-local file mtimes, and state artifacts can describe the same run differently, and stall recovery used to leave no explicit runtime event, making real recoveries look like no-ops until state files are inspected manually.`
- why_now:
  - this exact manager-stall investigation initially lost time on UTC vs host-local evidence alignment before the same-run correlation was proven
  - the deeper confirmed gap was observability, not display formatting: recovery happened, but `runtime-events.log` did not say so
  - a narrow follow-on can harden future incident analysis without reopening the completed display-time owner
- acceptance_criteria:
  - freeze the boundary between display-time governance and forensic-alignment governance
  - require explicit runtime events for stall recovery / equivalent runtime-owned re-entry triggers
  - define the minimum correlation anchors needed to align `runtime-events.log`, prompt/cycle/jsonl artifacts, and state files to one run
  - prove with regression evidence that a stall recovery leaves a visible runtime event trail instead of only state-file residue
- promotion_gate:
  - do not widen `runtime-human-readable-time-display-governance`; keep that owner limited to human-facing display semantics
  - absorb only runtime observation / observability scope here, not a repo-wide timestamp redesign
  - tie the follow-on to real evidence from the `2026-04-12 18:12 PDT` self-host stall investigation
- open_questions:
  - should this reopen `application-native-runtime-observation-contract-and-observability-planes`, or land as a narrower runtime-specific follow-on
  - should the canonical correlation anchor be event fields only, or a shared run-id/session-id tuple carried across all evidence planes
  - how much of the forensic checklist belongs in docs versus enforced runtime output/tests
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The display-time owner is not the right place for this gap. The missing contract is runtime forensic alignment and explicit recovery observability across evidence planes.`
    verdict: `ready_for_issue_materialization`
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- dependencies:
  - `runtime-human-readable-time-display-governance`
  - `application-native-runtime-observation-contract-and-observability-planes`
- landing_zones:
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/`
  - `docs/B2-docs/git-worktree/`
- promoted_issue_id: `I-20260412T184500Z-A`
- recommendation: `materialize this as a new narrow runtime observation owner rather than reopening the completed display-time owner or the broader completed observation contract.`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/issues/runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: `candidate mirror only. I-20260412T184500Z-A is now the canonical owner for runtime forensic alignment and stall recovery observability followthrough.`
- revisit_trigger: `future incident analysis still requires manual UTC-vs-local reconciliation or hidden state-file evidence to prove a runtime-owned recovery occurred.`
