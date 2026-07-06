- issue_id: I-20260626T130431Z-A
- kind: fix
- phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260626T130431Z/code-reviews
- source_candidate: docs/B1-docs/raw-20260626T130431Z31Z/candidates.md#C-20260626T130431Z-A
- pre_tests_path: docs/B2-docs/wt-close-force-phase6b/verification/pre-tests.md
- source_raw: raw-20260626T130431Z31Z
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260626T130431ZI-20260626T130431Z-A/issue.md
- title: wt-close Phase 6b respects --force, errors not silently swallowed

# I-20260626T130431Z-A: wt-close Phase 6b force fix

## 实现
- Phase 6b: without --force uses safe removal, errors exit 1
- Phase 6b: with --force uses force removal with severe warning log
