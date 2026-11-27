---
schema_version: '1'
local_id: raw-20261127T110239Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261127T110239Z-A
platform_ids:
  github:
    issue_id: '4737'
    url: https://github.com/chatterzhao/freely/issues/4737
    synced_at: ''
  gitee:
    issue_id: IKYKKT
    url: https://gitee.com/zhaoquan/freely/issues/IKYKKT
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/issues/I-20261127T110239Z-A.md
last_synced_comment_at:
  github: '2026-11-27T11:25:29Z'
  gitee: '2026-11-27T11:25:29Z'
hash: ''
created_at: '2026-11-27T11:02:39Z'
updated_at: '2026-11-27T11:25:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261127T110239Z-A
source_candidate: ''
completed_at: '2026-11-27T11:25:28Z'
closeout_note: ''
severity: P1
---

# fix: 平台评论失败回执不可操作，promote-finalize 重跑会向已关闭 Issue 追加重复评论

workflow_kind: fix

## fix: 平台评论失败回执不可操作，promote-finalize 重跑会向已关闭 Issue 追加重复评论

| Field | Value |
|-------|-------|
| local_id | `raw-20261127T110239Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/issues/I-20261127T110239Z-A.md` |
| created | 2026-11-27T11:02:39Z |
| updated | 2026-11-27T11:02:39Z |

---

> **Freely 治理**：这是 raw issue `raw-20261127T110239Z`。实现前请用 `wt-create --raw-key 20261127T110239Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（#4734 现场）\n执行 `freely issue-sync comment raw-20261127T100325Z` 在 Gitee 返回：\n`POST /repos/zhaoquan/freely/issues/IKYK8N/comments failed: HTTP 401: {"error":"当前issue已关闭评论功能"}`\n调用方无法从这条回执判断：是 API 路径错、token 失效、仓库禁评、还是 Issue 已关闭。\n\n## 精确根因（已实证，不要沿用「Gitee 关闭评论功能」的错误归因）\n1. API 端点正确：Gitee v5「创建某个 Issue 评论」就是 `POST /repos/{owner}/{repo}/issues/{number}/comments`，与 `gitee-issue.py cmd_comment()` 一致。\n2. token 正常：同一 CLI 的 `get`、`close`、`update` 均成功。\n3. 仓库设置：`GET /api/v5/repos/zhaoquan/freely` → `can_comment: true`（一般评论正常）、`issue_comment: false`（**不允许对 closed Issue 评论**，Gitee 默认）。\n4. Issue IKYK8N：`state: closed`、`issue_state: 已完成`，关闭时间 18:31:36+08。正常 `promote-finalize` 评论在 18:31:22+08 已成功（close 前 14 秒）。后续重试发生在 close 之后，因此被 `issue_comment=false` 拒绝。\n\n## 代码路径缺陷（为什么会去评论已关闭 Issue）\n- `bin/issue-sync.d/cmd-promote-finalize.sh:38-54`：本地用 `grep -q '^- event: promote_finalized$'` 防止重复追加评论块，但随后**无条件**调用 `cmd_comment "$raw_id"`，再调用 `cmd_close`。重跑时若 `last_synced_comment_at` 缺失/被 body 重写清空，就会再次推送同一条评论。\n- `bin/issue-sync.d/cmd-comment.sh`：完全不检查平台 Issue 状态就 POST；`platform-adapter` 已有 `get_issue_state()` 但未接入此路径。\n- `gitee-issue.py api_request()`：把所有 HTTP 错误原样抛出，未把 Gitee 特定语义（closed issue + `issue_comment=false`）翻译成可操作原因。\n- 人工排查中的额外错误：用 `GH_REPO=""` 试图只写 Gitee 无效，因为 wrapper 会从 git remote 自动重探 GitHub；结果 GitHub #4734 系统评论从 2 条增至 3 条（IDs 7215983525 / 7216177311 / 7216282291），Gitee/本地各 1 条，副本对账失败。\n\n## 期望\n1. `issue-sync comment` / `freely comment` 在写平台前读取 Issue 状态；若平台为 closed 且该平台不允许 closed-issue 评论，跳过写并返回**可操作诊断**（平台、issue、状态、仓库设置名、解决命令），非零退出，绝不静默吞错。\n2. `promote-finalize` 幂等：若 closing comment 已存在且已同步，或 raw 已 closed，则不再调用 `cmd_comment`；评论先于关闭的顺序保持。\n3. Gitee 401 消息 `当前issue已关闭评论功能` 映射为明确原因，不再只转发原始中文错误。\n4. 不提供/不使用 `GH_REPO=""` 这类隐式平台裁剪；若需单平台操作，必须显式命令参数。\n\n## AT 验收\n- closed Issue + `issue_comment=false`：不发起 POST，返回可操作诊断，非零退出。\n- open Issue：评论正常写入（回归现有 promote-finalize 行为）。\n- 重跑 `promote-finalize`：不产生第二份系统评论；三端评论数一致。\n- 错误回执必须包含平台名、local_id、issue 状态与具体设置名，而不是裸 HTTP 401。\n\n## 非目标\n不自动修改 Gitee 仓库设置；不删除已有重复评论（需单独确认/封装入口）。

### comment-20261127T112528Z
- source: system
- event: promote_finalized
- children: ["I-20261127T110239Z-A"]

拆解为以下任务:
1. [I-20261127T110239Z-A](will-be-updated)
