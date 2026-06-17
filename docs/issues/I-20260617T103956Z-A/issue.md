---
local_id: I-20260617T103956Z-A
kind: linked
status: in_dev
phase_state: in_b2_ibm
promoted_from: raw-20260617T103956Z
source_candidate: docs/pre-brainstorms/20260617T103956Z--eliminate-csv/candidates.md
verification_artifact_dir: docs/epics/eliminate-csv/code-reviews
---
# I-20260617T103956Z-A: Complete CSV Elimination
Eliminate all remaining worker_prompts_csv references (~28). Manager prompt: A2A SendMessage pattern.
Runtime: generate prompt file from Task.message. Align with A2A official proto Task.metadata extension point.
