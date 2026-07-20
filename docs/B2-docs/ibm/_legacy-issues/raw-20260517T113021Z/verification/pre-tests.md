# Pre-tests: raw-20260517T113021Z closeout

## Acceptance Items

### A1: issue.md has phase_state=absorbed and absorbed_into
- red-green-status: not_applicable
- status: passed
- test_command: grep -q 'phase_state: absorbed' docs/B1-docs/raw-20260517T113021Z/issue.md && grep -q 'absorbed_into: I-20260517T113021Z-A' docs/B1-docs/raw-20260517T113021Z/issue.md
- expected_output: exit 0
- actual_output: exit 0
- evidence_file: .freely/run/test-evidence/closeout-A1.log

### A2: I-20260517T113021Z-A issue file exists with frontmatter
- red-green-status: not_applicable
- status: passed
- test_command: grep -q 'local_id: I-20260517T113021Z-A' docs/B2-docs/ibm/_legacy-issues/raw-20260517T113021Z/issues/I-20260517T113021Z-A/issue.md && grep -q 'source_candidate:.*C-20260517T113021Z-A' docs/B2-docs/ibm/_legacy-issues/raw-20260517T113021Z/issues/I-20260517T113021Z-A/issue.md
- expected_output: exit 0
- actual_output: exit 0
- evidence_file: .freely/run/test-evidence/closeout-A2.log

### A3: Platform issue closed
- red-green-status: not_applicable
- status: passed
- test_command: grep -q 'platform_state: closed' docs/B1-docs/raw-20260517T113021Z/issue.md
- expected_output: exit 0
- actual_output: exit 0
- evidence_file: .freely/run/test-evidence/closeout-A3.log