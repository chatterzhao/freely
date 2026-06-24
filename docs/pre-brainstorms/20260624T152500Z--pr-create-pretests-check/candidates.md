---
source: raw-20260624T152500Z
---

# Candidate: C-20260624T152500Z-A

- status: promoted
- promoted_issue_path: docs/epics/pr-create-pretests-check/issues/I-20260624T152500Z-A.md
- acceptance_criteria:
  - pr-create-guarded blocks PR creation when pretests evidence is missing
  - Error message clearly instructs user to run skill:freely-test-execution
  - Pretests check follows same pattern as wt-close (consistent UX)
- promotion_gate: completion
- open_questions:
  - Should there be a --force flag to bypass? (deferred — not needed for initial implementation)
