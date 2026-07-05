---
local_id: I-20260622T104129Z-A
kind: I
phase_state: completed
source_candidate: docs/B1-docs/raw-20260622T104129Z/candidates.md#C-20260622T104129Z-A
verification_artifact_dir: docs/B2-docs/I-20260622T104129Z-A/code-reviews
raw_refs:
- raw-20260622T104129Z
candidate_refs:
- C-20260622T104129Z-A
created_at: '2026-06-22T10:41:29Z'
updated_at: '2026-06-22T10:41:29Z'
---

# I-20260622T104129Z-A: FREELY_SKIP Env Var Bypass Reason

## Summary

将 FREELY_SKIP_IBM_GATE 和 FREELY_SKIP_CREATE_GATE 从布尔型改为 reason-string 型，
值必须匹配正则 `^违规绕过门禁中，理由充分，是：`

## Changes

- pre-commit.sh: FREELY_SKIP_IBM_GATE reason gate
- pre-push.sh: FREELY_SKIP_IBM_GATE + FREELY_SKIP_CREATE_GATE reason gate
- pre-merge-commit.sh: FREELY_SKIP_IBM_GATE reason gate
- reference-transaction.sh: FREELY_SKIP_IBM_GATE reason gate
- .githooks/: sync all 4 hook files

## Acceptance Criteria

- [x] FREELY_SKIP_IBM_GATE=1 被拒绝并显示 GATE
- [x] FREELY_SKIP_CREATE_GATE=1 被拒绝并显示 GATE
- [x] 正确的 reason regex 格式被接受
