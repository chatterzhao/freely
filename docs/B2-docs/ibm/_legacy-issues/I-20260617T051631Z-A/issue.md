- issue_id: I-20260617T051631Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260617T051631Z-A
- source_candidate: docs/B1-docs/raw-20260617T051631Z-frontend-dynamic-projects/candidates.md#C-20260617T051631Z-A
- verification_artifact_dir: docs/B2-docs/frontend-dynamic-project-list/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260617T051631Z-A/issue.md
- title: Dynamic project list via adapter

# I-20260617T051631Z-A: Frontend dynamic project list

- source: `raw-20260617T051631Z` (GitHub #2892)
- phase_state: completed
- component: frontend-probe

## Implementation
- adapter.ts — listProjects() in interface + MockProbeAdapter
- tauriAdapter.ts — TauriProbeAdapter.listProjects() with fallback
- AppShell.tsx — useEffect loads from adapter
