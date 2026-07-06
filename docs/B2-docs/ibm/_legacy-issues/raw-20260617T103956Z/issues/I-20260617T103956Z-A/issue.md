---
local_id: I-20260617T103956Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T103956Z56Z
source_candidate: docs/B1-docs/raw-20260617T103956Z56Z/candidates.md
verification_artifact_dir: docs/B2-docs/eliminate-csv/code-reviews
platform_ids:
  github:
    issue_id: '2942'
    url: https://github.com/chatterzhao/freely/issues/2942
    synced_at: '2026-06-17T17:02:12Z'
updated_at: '2026-06-17T17:02:12Z'
primary_platform: github
created_at: '2026-06-17T17:02:12Z'
platform_state: closed
---
# I-20260617T103956Z-A: Complete CSV Elimination
Eliminate all remaining worker_prompts_csv references (~28). Manager prompt: A2A SendMessage pattern.
Runtime: generate prompt file from Task.message. Align with A2A official proto Task.metadata extension point.
