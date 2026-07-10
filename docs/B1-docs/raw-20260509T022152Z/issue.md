---
local_id: raw-20260509T022152Z52Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260509T022152Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '264'
    url: https://github.com/chatterzhao/freely/issues/264
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/issues/I-20260509T022152Z-A/issue.md
pre_tests_path: docs/B2-docs/worker-launch-writable-redirect/pre-tests.md
verification_artifact_dir: docs/B2-docs/worker-launch-writable-redirect/code-reviews
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-09T02:22:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

- pre_tests_path: `docs/B2-docs/worker-launch-writable-redirect/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/worker-launch-writable-redirect/code-reviews`

## 根因链

```
Manager AI 写 continuity → delegate worker to develop（保护分支）
  → runtime 读 continuity → 生成 worker prompt Worktree: develop
    → worker 在 develop 启动 → 无法 commit → 退出 → storm
```

## 证据

- `worker_prompt_resolved_worktree` (freely L9013) 直接从 prompt header 读 Worktree 路径，不做保护分支检查
- AI 在 continuity 中选的 target 是 develop，runtime 照办，不重定向
- #261 修复在 prompt 里加了 companion 工位信息，但只是告诉 AI 路径，不是 runtime 自动重定向

## 修复

`worker_prompt_resolved_worktree` 检测到 target 是保护分支（develop/main/test-pre-merge-*）时：
1. 从 branch 名提取 raw-key
2. 通过 `git worktree list` 查找配对 fix/raw-{key}-* 或 feature/raw-{key}-*
3. 返回可写工位路径

## 相关

- #261: worker prompt 加入 companion 工位信息（提示层）
- 本 issue: runtime 自动重定向（执行层）
