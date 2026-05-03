# Pre-tests — Timezone Standardization

- issue_id: `I-20260503T0901Z-timezone-standardize`
- issue_path: `docs/epics/timezone-standardization/issues/I-20260503T0901Z-timezone-standardize.md`

## Unit
- acceptance target: `Regex patterns accept both old (HHMM) and new (ThhmmZ) formats.`
- testing layer: `unit`
- target environment: `feature-local`
- required evidence: `grep/sed dry-run output`
- blocker taxonomy: `execution_pending_or_failed`
1. Verify `task-lifecycle-scan.py` regex matches both `raw-20260428-1737` and `raw-20260503T0901Z`.
2. Verify `governance-merge-gate` regex matches both branch formats.

## Integration
- acceptance target: `acp-bridge.py logs include Z suffix.`
- testing layer: `integration`
- target environment: `feature-local`
- required evidence: `source review`
- blocker taxonomy: `execution_pending_or_failed`
1. Confirm `acp-bridge.py` line 72 uses `Z` suffix.

## End-to-End
- acceptance target: `All 7 locations updated and consistent.`
- testing layer: `end_to_end`
- target environment: `feature-local`
- required evidence: `grep audit across all 7 locations`
- blocker taxonomy: `execution_pending_or_failed`
1. Run format audit across all locations.

## Acceptance Items

### acp-bridge log format
- id: `acp-bridge-log-tz`
- requirement: `acp-bridge.py log timestamps include Z suffix.`
- evidence_level: `unit`
- status: `pending`
- surface_kind: `runtime`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1`
- case_design: `Read acp-bridge.py line 72 and verify strftime includes Z.`

### task-lifecycle-scan dual regex
- id: `tls-dual-regex`
- requirement: `task-lifecycle-scan.py accepts both old and new format keys.`
- evidence_level: `unit`
- status: `pending`
- surface_kind: `governance`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2`
- case_design: `Verify regex patterns accept both \d{8}-\d{4} and \d{8}T\d{4,6}Z.`

### governance-merge-gate dual regex
- id: `gmg-dual-regex`
- requirement: `governance-merge-gate accepts both old and new format branch names.`
- evidence_level: `unit`
- status: `pending`
- surface_kind: `governance`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3`
- case_design: `Verify branch key extraction matches both formats.`

### wt-create dual regex
- id: `wt-create-dual-regex`
- requirement: `wt-create extracts issue keys from both old and new format branches.`
- evidence_level: `unit`
- status: `pending`
- surface_kind: `governance`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-4`
- case_design: `Verify _extract_issue_key matches both branch formats.`

### CONSTITUTION tag format
- id: `constitution-tag-tz`
- requirement: `CONSTITUTION.md version format includes Z suffix.`
- evidence_level: `unit`
- status: `pending`
- surface_kind: `governance`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-5`
- case_design: `Read CONSTITUTION.md section 3 and verify HHMMZ format.`
