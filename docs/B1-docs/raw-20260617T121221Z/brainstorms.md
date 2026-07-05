# Brainstorm: Remove worker_prompts_csv leftovers
## Discovery
PR #2914 removed CSV delegation but 7 A2A-layer locations still reference worker_prompts_csv field.
These are leftover from incomplete refactoring — field is no longer used by any code path.
## Decision
Promote. Remove all writes/reads. DB column stays for backward compat.
