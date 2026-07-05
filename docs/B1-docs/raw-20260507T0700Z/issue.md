---
local_id: raw-20260507T0700Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '243'
    url: https://github.com/chatterzhao/freely/issues/243
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T10:30:15Z'
updated_at: 2026-05-17T04:47:25Z
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/unified-platform/verification/pre-tests.md
verification_artifact_dir: docs/epics/unified-platform/code-reviews
source_candidate: docs/B1-docs/raw-20260507/candidates.md
platform_state: closed
---

## 问题

当前平台交互散落在 5+ 个文件中，功能重叠但不统一：

| 文件 | 职责 | 问题 |
|------|------|------|
| `bin/issue-sync` | 主写路径 | 缺多平台自动补齐 |
| `platform-adapter.py` | Python 封装 | 缺 labels/hash/comment-tracking |
| `issue-sync-batch.py` | 历史遗留 | GitHub-only，绕过 issue-sync |
| `raw-issue-pull` | 平台拉取 | 只找第一个平台 |
| `wt-create` | 工位创建 | chat-inbox 物化后没调 issue-sync create |

## 目标

**merge develop 后，所有用户已配置的仓库平台上的 issue 数量、状态、评论完全一致。**

## 方案

### 统一的仓库平台层

`freely` 所有 CLI/脚本调用统一平台层，不直接调 `gh` 或 `gitee-issue.py`：

```
freely → unified platform layer
           ├── create(local_id) → 所有平台都创建，缺的补齐，platform_ids 写回
           ├── update(local_id) → 所有平台都更新
           ├── close(local_id)  → 所有平台都关闭
           ├── comment(local_id) → 所有平台都推送评论
           └── pull(raw_key)    → 从任一平台拉取，缺的补建
```

### 关键逻辑

1. **chat-inbox → raw issue**：wt-create materialize 后，调 `platform.create(local_id)` → 所有已配置平台创建 issue → platform_ids 写回 frontmatter

2. **平台拉取 → raw issue**：raw-issue-pull 找到 GitHub issue → platform_ids.github 已有 → 调 `platform.create(local_id)` 补建 Gitee → platform_ids.gitee 补全

3. **merge 后同步**：`_sync_issues_changed_in_merge` → 调 `platform.update/close` → 所有平台同步

### 收拢策略

1. `issue-sync` 改造为核心入口，补全多平台自动补齐
2. `platform-adapter.py` 合并进 `issue-sync` 或被其调用
3. `issue-sync-batch.py` 废弃/删除
4. `raw-issue-pull` 改为调用统一平台层
5. `wt-create` materialize 后调用统一平台层

## 改动范围

- `bin/issue-sync`：增加多平台自动补齐 + create-if-missing + Gitee 标题搜索
- `docs/system/workspace/scripts/sync/platform-adapter.py`：合并/被 issue-sync 调用
- `bin/raw-issue-pull`：走统一平台层
- `docs/system/workspace/scripts/worktree/wt-create`：materialize 后调 issue-sync create
- `bin/issue-sync-batch.py`：废弃

## 成功标准

- chat-inbox 来源的 raw issue：创建工位后，所有配置平台都有对应 issue，platform_ids 已写回
- 平台拉取的 raw issue：所有配置平台都有，platform_ids 完整
- merge develop 后：所有平台上该 issue 状态/评论一致
- 只有一个 entry point 调用平台 API：`issue-sync`

- pre_tests_path: `docs/epics/unified-platform/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/unified-platform/code-reviews`
