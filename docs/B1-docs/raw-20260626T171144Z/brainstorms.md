---
b1_id: B1-20260626T171144Z
phase_state: completed
source_raw: raw-20260626T171144Z44Z
source_url: https://github.com/chatterzhao/freely/issues/3569
produced_candidate: C-20260626T171144Z-A
created_at: 2026-06-26
---
# B1_IBM: slot switching not aware of agent-table per-role assignment
## Problem
Slot discovery scans ~/.ai-auth/ alphabetically, doesn't know agent-table assignment.
## Decision: Pin agent-table slot at startup
_init_agent_table_slot_pin writes assigned slot to ~/.ai-auth/.{tool}-current-slot.
## Candidate
- candidate_id: C-20260626T171144Z-A
- status: promoted
- milestone: M-20260626T171144Z-A
