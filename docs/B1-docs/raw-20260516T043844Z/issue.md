---
local_id: raw-20260516T043844Z44Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '357'
    url: https://github.com/chatterzhao/freely/issues/357
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T04:39:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
absorbed_into: raw-20260710T005219Z---

## pre-push.sh 逻辑

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T043844Z44Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T04:38:44Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T043844Z44Z`。实现前请用 `wt-create --raw-key 20260516T043844Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T04:38:44Z"
title: "gitee 远程分支无法删除：pre-push hook 不识别 delete 操作，需通过 API 删除"

## 背景

`wt-close` Phase 4 删除远程分支时执行 `git push <remote> --delete <branch>`，但 `.githooks/pre-push` → `pre-push.sh` 不处理 `(delete)` 类型的 ref，将其归入 `*)` 兜底分支直接拒绝。

```bash
# pre-push.sh 逻辑
local_branch="${local_ref#refs/heads/}"
case "$local_branch" in
  feature/*|hotfix/*) ... ;;
  *)  # (delete) 落在这里，被拒绝
    [HOOK] Push blocked: unsupported branch type '(delete)'.
```

结果是 `wt-close` 的 `git push --delete 2>/dev/null || true` 静默失败——wt-close 认为删除成功，但远程分支实际还在。

## 需求

**短期（本次）**：新增 gitee 远程分支 API 删除能力，模仿 `docs/system/workspace/scripts/runtime/gitee-issue.py` 的实现模式：
- 使用 Gitee REST API v5：`DELETE /api/v5/repos/{owner}/{repo}/git/refs/heads/{branch}`
- 认证方式与 `gitee-issue.py` 一致（`GITEE_ACCESS_TOKEN` / `GITEE_TOKEN`）
- `wt-close` Phase 4 对 gitee remote 优先走 API 删除，失败再 fallback `git push --delete`

**后续（另开 issue）**：修 `pre-push.sh` 支持 `(delete)` ref type，让 `git push --delete` 也能正常工作。

## 参考

- `gitee-issue.py`：Gitee API 封装模式（`api_request`、`detect_repo`、token 管理）
- `wt-close` Phase 4：当前远程删除逻辑（line 242-260）
- GitHub API 删除已验证可用：`gh api -X DELETE repos/{owner}/{repo}/git/refs/heads/{branch}`
