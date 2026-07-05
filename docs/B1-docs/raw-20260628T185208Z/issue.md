---
local_id: raw-20260628T185208Z08Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260628T005815Z-A
pre_tests_path: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/code-reviews
---

- absorbed_into: I-20260628T005815Z-A
- pre_tests_path: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/human/discuss/raw-20260628T005815Z15Z/code-reviews

## Problem
Gate/skill alignment: pretests-gate only accepts "pass" not "passed", B2 skill examples show old paths, governance-merge-gate uses *.md instead of I-*.md.

## Scope
- pretests-gate/retirement-gate: accept both pass and passed
- governance-merge-gate: I-* prefix, better skip error msg
- B2 skill: update template paths
- pre-tests.md files: use pass (old-gate-compatible)
