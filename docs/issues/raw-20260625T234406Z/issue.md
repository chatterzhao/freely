---
local_id: raw-20260625T234406Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3520'
    url: https://github.com/chatterzhao/freely/issues/3520
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T23:44:25Z'
updated_at: '2026-06-25T23:44:25Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

大量文件只提 fix 不提 feature，或相反。fture 开发时会导致命令行报错、帮助文本误导、变量名混乱。

## 功能 Bug

### test-lane (严重)
`docs/system/workspace/scripts/quality/test-lane` line 30-32:
```
feature_local_branch() { [[ "$branch" == feature/* || "$branch" == release/* || "$branch" == hotfix/* ]] }
```
缺少 `fix/*`，导致 fix/raw-* 分支被 feature-local 测试车道拒绝。

### wt-create / pr-review-guarded 变量命名
- `bin/pr-review-guarded`: `_fix_wt` 当 feature 也用，应改为 `_dev_wt` 或 `_src_wt`
- `docs/system/workspace/scripts/worktree/wt-create`: `$fix_branch` 在 feature 前缀下也用，应改为 `$dev_branch`

## 文档 gap

| 文件 | 问题 |
|------|------|
| CONSTITUTION.md L40,69,111,217 | 只提 feature/* |
| LAWS.md L51,58 | 只提 feature/* |
| AGENTS.md L92,106,134,185,266 | 只提 feature worktree |
| CLAUDE.md L27 | 只提 feature worktree |
| manager-agent.md L220,257 | 只提 fix/raw 或 feature |
| pr-merge-guarded L146 | 错误消息只显示 fix/raw- |
| wt-add L77 | 缺 fix/ |
| pre-commit.sh L222,359 | 缺 fix |
| pre-push.sh L147,216 | 缺 fix |
| start-lead-agent.sh L326 | 缺 feature/raw- |

## 改动
修复全部以上文件，统一用 fix|feature 表述。变量命名改为中性。
