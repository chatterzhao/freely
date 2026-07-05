# Implementation Decision: Complete CSV Elimination
- issue_id: I-20260617T103956Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: Remove all ~28 CSV references, update Manager prompt, runtime generates prompt from Task.message
- why_this: A2A Task.metadata is standard extension point, Message.parts[0].text carries task content
- alternatives_considered: Gradual removal — rejected: partial CSV creates confusion
- boundary_non_goals: Don't change ACP session/prompt mechanics
- residual_risk: Manager AI must learn new a2a-exit pattern via prompt update
