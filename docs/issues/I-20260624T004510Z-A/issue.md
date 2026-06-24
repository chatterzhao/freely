---
local_id: I-20260624T004510Z-A
kind: linked
status: in_dev
phase_state: done_b2_ibm
promoted_from: raw-20260624T004510Z
source_candidate: docs/pre-brainstorms/20260624T004510Z--deploy-skills-all-tools/candidates.md
canonical_issue_path: ""
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
pre_tests_path: docs/epics/deploy-skills-registry-default/verification/pre-tests.md
verification_artifact_dir: docs/epics/deploy-skills-registry-default/code-reviews
---

# I-20260624T004510Z-A: deploy-skills 默认部署到全部已安装 tool

- source_candidate: `docs/pre-brainstorms/20260624T004510Z--deploy-skills-all-tools/candidates.md`
- pre_tests_path: `docs/epics/deploy-skills-registry-default/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/deploy-skills-registry-default/code-reviews`

## 实现

1. 修复 `bin/deploy-skills` 第 118 行 `opencode)` 精确匹配 → `opencode*)` 前缀匹配
2. 默认 `--tools` 不再从 AI_TOOL/FREELY_TOOLS/global config 单值读取，改为从 `tool-registry.json5` 读取所有 tool key，通过 `command -v` 检测已安装 tool，部署到全部已安装 tool
