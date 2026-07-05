---
local_id: I-20260624T004510Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260624T004510Z
source_candidate: docs/B1-docs/raw-20260624T004510Z/candidates.md#C-20260624T004510Z-A
canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260624T004510Z-A/issue.md
milestone: "M-20260624T004510Z-A"
title: "fix: deploy-skills opencode wildcard fix + registry-driven default tool detection"
platform_ids:
  github:
    issue_id: '3397'
primary_platform: github
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-24T00:45:10Z
updated_at: 2026-06-24T01:30:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/B2-docs/deploy-skills-registry-default/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/deploy-skills-registry-default/code-reviews
---

# I-20260624T004510Z-A: deploy-skills opencode 通配符修复 + registry 驱动默认 tool 检测

- source_candidate: `docs/B1-docs/raw-20260624T004510Z/candidates.md#C-20260624T004510Z-A`
- pre_tests_path: `docs/B2-docs/deploy-skills-registry-default/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/deploy-skills-registry-default/code-reviews`
- milestone: M-20260624T004510Z-A

## 实现

1. 修复 `bin/deploy-skills` 第 99 行 `opencode)` 精确匹配 → `opencode*)` 前缀匹配
2. 默认 `--tools` 改为从 `tool-registry.json5` 读取所有 tool key，通过 `command -v` 检测已安装 tool，部署到全部已安装 tool
