---
issue_id: I-20260625T020333Z-A
kind: fix
phase_state: completed
milestone: M-20260625T020333Z-A
source_candidate: docs/pre-brainstorms/20260625T020333Z--force-abandon-only/candidates.md#C-20260625T020333Z-A
verification_artifact_dir: docs/epics/force-abandon-only/code-reviews
canonical_issue_path: docs/issues/I-20260625T020333Z-A/issue.md
title: wt-close --force semantics clarified as abandon-only, not error bypass
---

# I-20260625T020333Z-A: wt-close --force semantics = abandon-only
- source_candidate: docs/pre-brainstorms/20260625T020333Z--force-abandon-only/candidates.md#C-20260625T020333Z-A
- verification_artifact_dir: docs/epics/force-abandon-only/code-reviews

## scope
Clarify that `wt-close --force` is strictly for abandoning a raw issue, not for bypassing gate errors.

## deliverables
- [x] Code fix: wt-close --help, pretests gate, examples updated
- [x] Pre-tests: verification of --force behavior
- [x] Code review: Implementation Decision Note

## verification
- `wt-close --help` shows `--force = 确定丢弃此 raw issue`
- pretests gate error shows fix vs force paths
- No remaining examples that imply --force for non-abandon scenarios
