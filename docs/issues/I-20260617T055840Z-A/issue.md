---
local_id: I-20260617T055840Z-A
kind: linked
status: in_dev
phase_state: done_b2_ibm
promoted_from: raw-20260617T055840Z
source_candidate: docs/pre-brainstorms/20260617T055840Z--merge-guard-rebase-integrity/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-17T05:58:40Z
updated_at: 2026-06-17T06:10:00Z
intake_id: ""
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/merge-guard-rebase-integrity/pre-tests.md
verification_artifact_dir: docs/epics/merge-guard-rebase-integrity/code-reviews
---

# I-20260617T055840Z-A: Merge Guard + Rebase Integrity

- source_candidate: `docs/pre-brainstorms/20260617T055840Z--merge-guard-rebase-integrity/candidates.md`
- pre_tests_path: `docs/epics/merge-guard-rebase-integrity/pre-tests.md`
- verification_artifact_dir: `docs/epics/merge-guard-rebase-integrity/code-reviews`
- branch: `fix/raw-20260617T055840Z-merge-guard-rebase-integrity`

## 目标

1. 拦截 GitHub UI "Merge pull request" 绕过 pr-merge-guarded 的直接 merge
2. git rebase 后自动校验代码完整性，丢失变更时阻止 merge

## 实现

### Fix 1: Branch Protection 拦截直接 merge
- **CI workflow** (`.github/workflows/pr-merge-guard.yml`): 创建 `governance/pr-merge-guard` check (in_progress)，阻塞 GitHub UI merge 按钮
- **pr-merge-guarded**: 新增 `_set_governance_check_pass()` — merge 前通过 GitHub API 将 check 设为 success（替代 `--admin` flag）
- **pr-merge-guarded**: 移除 `gh pr merge --admin`，改为普通 `gh pr merge`（服从 branch protection）
- **一次性配置**: `gh api` 一行命令启用 develop 分支 protection（文档化在 workflow 注释中）

### Fix 2: Rebase 完整性 Hook
- **pre-rebase hook** (`.githooks/pre-rebase` → `docs/system/workspace/hooks/pre-rebase.sh`): rebase 前保存 `git diff develop...HEAD --name-only` 快照
- **post-rewrite hook** (`.githooks/post-rewrite` → `docs/system/workspace/hooks/post-rewrite.sh`): rebase 后对比快照，文件消失则写入 `.freely/run/rebase-lost-files` marker
- **pr-merge-guarded**: 新增 `check_rebase_integrity()` gate — 读取 marker，存在则拒绝 merge 并输出丢失文件列表

## 影响文件
- `.githooks/post-rewrite` (新建)
- `.githooks/pre-rebase` (新建)
- `docs/system/workspace/hooks/post-rewrite.sh` (新建)
- `docs/system/workspace/hooks/pre-rebase.sh` (新建)
- `docs/system/workspace/scripts/worktree/pr-merge-guarded` (修改)
- `.github/workflows/pr-merge-guard.yml` (重写)
