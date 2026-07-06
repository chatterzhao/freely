- issue_id: I-20260619T061448Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260619T061448Z-A
- source_candidate: docs/B1-docs/raw-20260619T061441Z48Z-a2a-h11-noise/candidates.md#C-20260619T061448Z-A
- verification_artifact_dir: docs/B2-docs/a2a-h11-noise/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260619T061448ZI-20260619T061448Z-A/issue.md
- title: Suppress A2A server h11 non-HTTP noise

# I-20260619T061448Z-A: A2A server h11 noise suppression

- source: `raw-20260619T061441Z48Z` (GitHub #3038)
- milestone: M-20260619T061448Z-A
- phase_state: completed
- component: a2a

## Implementation
- `docs/system/workspace/scripts/runtime/a2a/a2a_server.py` — _a2a_uvicorn_log_config() + log_config in start()
