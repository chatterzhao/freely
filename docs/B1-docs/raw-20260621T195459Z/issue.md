---
local_id: raw-20260621T195456Z59Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3287'
    url: https://github.com/chatterzhao/freely/issues/3287
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T19:55:16Z'
updated_at: '2026-06-21T19:55:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

`wt-create` 只检查分支名精确匹配（`fix/raw-{key}-{slug}`），不检查同一 raw_key 是否已有其他工位/分支。如果分支已删但工位目录还在，或同 raw_key 不同 slug，仍会创建重复工位。

## 修复

`wt-create` 在创建分支前增加模糊匹配检查：

```bash
# 1. 模糊匹配: 已有该 raw_key 的活跃分支?
existing_branch=$(git branch | grep "raw-${raw_key}")
if [[ -n "$existing_branch" ]]; then
    echo "拒绝: raw-${raw_key} 已有分支: $existing_branch"
    echo "  请使用已有工位，或先 wt-close 后再重建。"
    exit 1
fi

# 2. 模糊匹配: 已有该 raw_key 的活跃工位目录?
existing_wt=$(git worktree list | grep "raw-${raw_key}")
if [[ -n "$existing_wt" ]]; then
    echo "拒绝: raw-${raw_key} 已有工位"
    exit 1
fi

# 3. raw issue 已关闭?
phase=$(grep "phase_state:" "docs/B1-docs/raw-${raw_key}/issue.md" 2>/dev/null)
if [[ "$phase" =~ (absorbed|completed|dropped) ]]; then
    echo "拒绝: raw-${raw_key} 已关闭 (phase_state=$phase)"
    exit 1
fi
```

## 验证

- 已有相同 raw_key 的工位时，wt-create 拒绝并提示复用工位
- 已关闭的 raw issue 无法创建新工位

🤖 Generated with [Claude Code](https://claude.com/claude-code)
