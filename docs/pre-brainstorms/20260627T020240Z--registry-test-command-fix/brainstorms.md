---
b1_id: B1-20260627T020240Z; phase_state: completed
source_raw: raw-20260626T173930Z; produced_candidate: C-20260627T020240Z-A
created_at: 2026-06-27
---
# B1_IBM: registry test_command fixes
## Problem
cline --yolo deprecated, claude --max-tokens 50 unsupported. Discovered during batch slot testing.
## Decision
Fix registry test_command. cline: --auto-approve true. claude: drop --max-tokens.
## Candidate
candidate_id: C-20260627T020240Z-A; status: promoted; milestone: M-20260627T020240Z-A
