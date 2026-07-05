# Pre-Tests
- issue_id: raw-20260513T075847Z
## Unit
- acceptance target: scan outputs platform_only items for non-raw-key open issues
- testing layer: unit
- required evidence: python3 syntax check
- replacement_evidence: python3 -c py_compile passed
## Acceptance Items
### AT-001 non-rawkey visibility
- id: non-rawkey-visibility
- requirement: scan output includes gh-{number} items for platform issues without raw-key
^- status: passed
- artifact_ref: docs/B2-docs/scan-non-rawkey-visibility/code-reviews/review.md
