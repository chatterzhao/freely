---
issue_id: I-20260624T235907Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260624T235907Z-A
## Implementation Decision Note
- decision: hard-reject pre-tests with all mock/not_applicable items
- why_this: current system allows passing with zero real tests
- alternatives_considered: skill-only guidance (too weak)
- boundary_non_goals: partial mock coverage still allowed
- residual_risk: gate may reject legitimate mock-only tests
