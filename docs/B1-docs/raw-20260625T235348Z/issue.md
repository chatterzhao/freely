---
local_id: raw-20260625T235348Z48Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3522'
    url: https://github.com/chatterzhao/freely/issues/3522
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T23:54:07Z'
updated_at: '2026-06-25T23:54:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T235348Z-A
source_candidate: docs/B1-docs/raw-20260625T235348Z48Z/candidates.md#C-20260625T235348Z-A
promoted_issue_path: docs/issues/I-20260625T235348Z-A/issue.md
pre_tests_path: docs/B2-docs/wt-close-consistency/verification/pre-tests.md
platform_state: closed
---

## 问题

wt-close 的 bug：
1. CWD 在 worktree 内导致 git branch -d fatal 静默失败
2. 不检查 dev↔test 一致性
3. 先平台后本地

## 步骤

```bash
# 1. CWD 安全
git_root=$(git rev-parse --show-toplevel)
cd "$git_root"
git checkout develop

# 2. 用 raw key 精确匹配工位（不分 fix 或 feature）
raw="20260625T123456Z"
dev_wt=$(git worktree list --porcelain | awk -v k="raw-$raw" '
  $1=="worktree" { wt=$2 }
  $1=="branch" && $2 ~ k { print wt; exit }
')
test_wt=$(git worktree list --porcelain | awk -v k="test-pre-merge-$raw" '
  $1=="worktree" { wt=$2 }
  $1=="branch" && $2 ~ k { print wt; exit }
')

# 3. test dirty → 阻塞
git -C "$test_wt" status --short | grep -q . && { echo "测试工位脏"; exit 1; }

# 4. dev dirty → 阻塞
git -C "$dev_wt" status --short | grep -q . && { echo "开发工位脏"; exit 1; }

# 5. 测试有开发没有 → 阻塞
dev_branch=$(git -C "$dev_wt" rev-parse --abbrev-ref HEAD)
git log --oneline --no-merges "$dev_branch"..HEAD --not "$dev_branch" 2>/dev/null && exit 1

# 6. 开发有测试没有 → 阻塞
git log --oneline --no-merges HEAD.."$dev_branch" 2>/dev/null && exit 1

# 7. 全过 → 删 worktree → 删本地 branch → 删远程 → 关 issue
```

## --force
仅用于放弃开发。不能跳过一致性检查。

## worker 修复后
阻塞 → cherry-pick → commit → push → pr-review → pass → wt-close

## 改动
- docs/system/workspace/scripts/worktree/wt-close
