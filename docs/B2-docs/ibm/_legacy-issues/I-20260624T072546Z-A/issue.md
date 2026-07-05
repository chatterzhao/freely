---
local_id: I-20260624T072546Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T072546Z46Z
source_candidate: docs/B1-docs/raw-20260624T072546Z46Z/candidates.md#C-20260624T072546Z-A
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260624T072546Z-A/issue.md
milestone: M-20260624T072546Z-A
title: 'fix: wt-create/hook/freely feedback 平台硬编码报错修复'
platform_ids: {github: {issue_id: '3410'}}
primary_platform: github
pre_tests_path: docs/B2-docs/platform-agnostic-error-msgs/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/platform-agnostic-error-msgs/code-reviews
platform_state: open
updated_at: '2026-06-24T07:26:03Z'
---
# I-20260624T072546Z-A: 平台硬编码报错修复
- source_candidate: docs/B1-docs/raw-20260624T072546Z46Z/candidates.md
- pre_tests_path: docs/B2-docs/platform-agnostic-error-msgs/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/platform-agnostic-error-msgs/code-reviews
## 改动
- .githooks/reference-transaction.sh
- wt-create: 8 处
- freely feedback --help / chat intake
