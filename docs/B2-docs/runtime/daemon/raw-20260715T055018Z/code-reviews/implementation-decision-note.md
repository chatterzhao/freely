- issue_id: I-20260715T055018Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/issues/I-20260715T055018Z-A.md

## Implementation Decision Note

- decision: 1. Delete stale scan cache in start_project_runtime. 2. Add universal auto→listen gate before the stop_ai case in exit handler.

- why_this: Fix 1 forces bootstrap_missing_scan on first build_prompt. Fix 2 prevents restart loops when AI exits with non-stop_ai reasons while scan is empty.

- alternatives_considered: Option A: add "daemon just started" trigger to scan regeneration reason function. Rejected — more complex, 15+ lines vs 1 line rm -f. Option B: only fix stop_ai to handle tool_unproductive. Rejected — future exit kinds would need the same fix.

- boundary_non_goals: NOT changing listen mode scan behavior (already correct). NOT modifying scan regeneration reason function.

- residual_risk: Universal gate runs before stop_ai's retry/override logic — but this is safe because both check ready_count==0 and switch to listen. The universal gate applies to ALL exit kinds uniformly.
