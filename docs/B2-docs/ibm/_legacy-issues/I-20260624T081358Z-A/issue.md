---
local_id: I-20260624T081358Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T081358Z
source_candidate: docs/B1-docs/raw-20260624T081358Z/candidates.md#C-20260624T081358Z-A
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260624T081358Z-A/issue.md
milestone: M-20260624T081358Z-A
title: 'fix: skills/AGENTS 测试文档 daemon 假设改为 pre-tests.md 委托'
platform_ids:
  github:
    issue_id: '3411'
primary_platform: github
pre_tests_path: docs/B2-docs/testing-docs-pre-tests-delegation/verification/pre-tests.md
verification_artifact_dir: docs/epics/testing-docs-pre-tests-delegation/code-reviews
platform_state: open
updated_at: '2026-06-24T08:13:58Z'
---
# I-20260624T081358Z-A: 测试文档 daemon 假设修复

- source_candidate: `docs/B1-docs/raw-20260624T081358Z/candidates.md`
- pre_tests_path: `docs/B2-docs/testing-docs-pre-tests-delegation/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/testing-docs-pre-tests-delegation/code-reviews`

## 改动
- freely-fix-execution/SKILL.md: daemon → pre-tests.md 委托
- freely-test-execution/SKILL.md: daemon 步骤 → 通用环境准备
- freely-feat-execution/SKILL.md: "启动项目测试" → "按 pre-tests.md 执行验证"
- AGENTS.md: test-pre-merge 段标注为 Freely 自举示例
