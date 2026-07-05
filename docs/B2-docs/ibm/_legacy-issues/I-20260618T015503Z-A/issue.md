---
local_id: I-20260618T015503Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260618T015503Z
source_candidate: docs/B1-docs/raw-20260618T015503Z/candidates.md
canonical_issue_path: ''
platform_ids:
  github:
    issue_id: '3271'
    url: https://github.com/chatterzhao/freely/issues/3271
    synced_at: '2026-06-21T18:24:53Z'
primary_platform: github
created_at: 2026-06-18 01:55:03+00:00
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/worktree-path-architecture/verification/pre-tests.md
verification_artifact_dir: docs/epics/worktree-path-architecture/code-reviews
platform_state: closed
updated_at: '2026-06-21T18:24:53Z'
---

# I-20260618T015503Z-A: Fix worktree path architecture

- source_candidate: docs/B1-docs/raw-20260618T015503Z/candidates.md
- pre_tests_path: docs/B2-docs/worktree-path-architecture/verification/pre-tests.md
- verification_artifact_dir: docs/epics/worktree-path-architecture/code-reviews

## 实现范围

### 1. worktree-common.sh — ROOT_DIR 定义修正
`$(dirname $0)/../../../../..` → `git rev-parse --show-toplevel`

### 2. wt-create — raw issue 物化到 worktree
7 处 `$ROOT_DIR/docs/issues/` → `$target_path/docs/issues/`

### 3. wt-close — ROOT_DIR 改为 CWD 感知
`$(dirname $0)/../../../../..` → `git rev-parse --show-toplevel`

### 4. pr-merge-guarded — 删除 _absorb_close_frontmatter
Merge 时 raw issue 已从 worktree 带入，无需事后 amend。

### 5. pr-create-guarded — 增加 worktree 内 phase_state 检查
在 worktree 内执行时检查 worktree 的 docs/issues/ 中 phase_state。

### 6. config.toml — PROJECT_ROOT 支持自动推导
考虑向后兼容，暂保持绝对路径，增加文档说明。
