---
issue_id: I-20260624T235907Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260624T235907Z-A
## Implementation Decision Note
- decision: fallback checks actual_output (GREEN) not pretests-gate (RED)
- why_this: pre-tests.md existence proves RED (doc written) not GREEN (tests executed)
- alternatives_considered: keep pretests-gate call (rejected - mixes RED/GREEN)
- boundary_non_goals: Worker path unchanged
- residual_risk: none
