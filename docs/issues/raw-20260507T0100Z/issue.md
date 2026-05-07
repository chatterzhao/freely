---
local_id: raw-20260507T0100Z
kind: raw
status: proposed
phase_state: proposed
platform_ids:
  github: "237"
primary_platform: github
created_at: 2026-05-07T01:00:00Z
author: zhaoquan
channel: github
session_refs: []
pre_tests_path: docs/epics/fix-branch-naming/verification/pre-tests.md
verification_artifact_dir: docs/epics/fix-branch-naming/code-reviews
source_candidate: docs/pre-brainstorms/20260507-fix-branch-naming/candidates.md
---

## 问题
fix-execution SKILL.md 分支规范表中普通 fix 的分支前缀是 feature/ 不是 fix/。

## 修复
7 处 feature/ → fix/，使用 raw-{raw-key}-{slug} 格式。

- pre_tests_path: `docs/epics/fix-branch-naming/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/fix-branch-naming/code-reviews`
