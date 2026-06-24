---
local_id: raw-20260624T141559Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3435'
    url: https://github.com/chatterzhao/freely/issues/3435
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T14:16:17Z'
updated_at: '2026-06-24T14:35:00Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
absorbed_into: fix/raw-20260624T141559Z-feedback-issue-sync
---

## 问题

`cmd_feedback` 是唯一绕过多平台抽象层 `issue-sync` 的命令。

### 具体表现

1. **硬编码 `gh issue create`** — 只能创建到 GitHub，不支持 Gitee
2. **`--repo` 参数多余** — repo 应该从 `git remote` 自动获取，不需要用户手工传
3. **不写 `docs/issues/` 本地文件** — issue-sync 的其他命令都依赖本地 issue.md，feedback 却跳过
4. **`_resolve_gh_repo()` 只能解析 GitHub URL** — 即使传了 Gitee URL 也会失败

### 对比架构

| 命令 | 平台方式 | 多平台 |
|------|---------|:---:|
| `wt-close` | → issue-sync close | ✅ GitHub + Gitee |
| `pr-create-guarded` | → develop-push | ✅ |
| `pr-merge-guarded` | → develop-push | ✅ |
| **`feedback`** | **gh issue create 硬编码** | ❌ 仅 GitHub |

### 正确做法

`cmd_feedback` 应该对齐为 issue-sync 的薄封装：

1. 从 `git remote` 自动获取 repo，去掉 `--repo` 参数
2. 生成本地 `docs/issues/raw-{key}/issue.md`
3. 调用 `issue-sync create` 推送到所有配置的平台
4. 加平台只需在 adapter 层新增，feedback 零改动
