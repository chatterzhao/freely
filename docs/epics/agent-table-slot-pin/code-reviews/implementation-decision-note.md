---
issue_id: I-20260626T171144Z-A
issue_path: docs/issues/I-20260626T171144Z-A/issue.md
phase_state: done_b2_ibm
---
- issue_id: I-20260626T171144Z-A
## Implementation Decision Note
- decision: Add _init_agent_table_slot_pin at daemon start. Read agent role from agent-id.env, look up slot from agent-table, write to current-slot file.
- why_this: Slot switching uses ~/.ai-auth/ scan (alphabetical), not agent-table assignment. Pinning fixes this.
- alternatives_considered: Redesign entire slot discovery (too invasive), keep as-is (keeps switching bug)
- residual_risk: Codex has separate slot init path (ensure_codex_slot_ready_for_manager) which is not changed
