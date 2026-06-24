---
local_id: I-20260624T085740Z-A
kind: linked
status: in_dev
phase_state: done_b2_ibm
promoted_from: raw-20260624T085740Z
source_candidate: docs/pre-brainstorms/20260624T085740Z--parse-prompt-fix/candidates.md#C-20260623T075104Z-A
canonical_issue_path: docs/issues/I-20260624T085740Z-A/issue.md
milestone: M-20260624T085740Z-A
title: 'fix: A2A parse rotting submitted + prompt state semantics'
platform_ids: {}
primary_platform: github
pre_tests_path: docs/epics/parse-prompt-fix/verification/pre-tests.md
verification_artifact_dir: docs/epics/parse-prompt-fix/code-reviews
platform_state: open
---
# I-20260624T085740Z-A: A2A parse + prompt state fix
## 改动
Fix 1: parse submitted + worker_count=0 + 30s grace → resume_manager
Fix 2: prompt "无事可做" --state completed → --state failed + 三态语义
