# Candidates - 20260616T055035Z--a2a-hygiene-after-run

## Context
- Source: raw-20260616T055035Z (A2A server hygiene + after-run worker detection)
- Status: completed

## Candidates

### C-20260616T055035Z-A: legacy issue
- candidate_id: C-20260616T055035Z-A
- title: A2A server hygiene + after-run worker detection for prompt mode
- problem: A2A zombie processes accumulate on daemon restart; startup healthcheck is insufficient; after-run worker detection missing for prompt mode
- why_now: 5 zombie A2A processes observed; worker dispatch broken when Manager exits with end_turn
- acceptance_hint: A2A processes cleaned on start/stop; healthcheck via HTTP; workers launched after end_turn
- priority: P0
- status: promoted
- decision_reason: Runtime bug affecting worker dispatch reliability
- promoted_issue_path: docs/issues/I-20260616T055035Z-A/issue.md
- milestone: M-20260616T055035Z-A
- next_action: 已实现并合并
- revisit_trigger: ""
- session_refs: []
