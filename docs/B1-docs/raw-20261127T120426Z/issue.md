---
schema_version: '1'
local_id: raw-20261127T120426Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4740'
    url: https://github.com/chatterzhao/freely/issues/4740
    synced_at: ''
  gitee:
    issue_id: IKYKS3
    url: https://gitee.com/zhaoquan/freely/issues/IKYKS3
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-27T12:04:26Z'
updated_at: '2026-11-27T12:04:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P1
---

# fix: 缺封装 comment-delete 入口，副本重复评论无法清理

workflow_kind: fix

## fix: 缺封装 comment-delete 入口，副本重复评论无法清理

| Field | Value |
|-------|-------|
| local_id | `raw-20261127T120426Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-27T12:04:26Z |
| updated | 2026-11-27T12:04:26Z |

---

> **Freely 治理**：这是 raw issue `raw-20261127T120426Z`。实现前请用 `wt-create --raw-key 20261127T120426Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象\n#4734 的代码修复已完成，但 raw-reconciliation 被评论数不一致阻塞：GitHub #4734 有 3 份相同系统评论（IDs 7215983525 / 7216177311 / 7216282291），Gitee IKYK8N 与本地各 1 份。现有封装命令只能新增评论，无法删除平台侧重复评论。\n\n## 风险\n直接用 `gh api DELETE` 或 `curl` 调用平台 API 会绕过平台写通道审计与双平台对账，违反项目约定；但不用则 #4734 无法收口，且未来任何重复评论都只能靠人工平台操作。\n\n## 根因\n`platform-adapter.py` 有 `comment`（POST）但没有 comment-delete 入口；`issue-sync` 动作表也没有对应封装命令。Gitee 侧 API 实际支持 `DELETE /repos/{owner}/{repo}/issues/comments/{id}`，GitHub 侧亦有 delete issue comment API，但封装层未暴露。\n\n## 期望\n1. 新增封装命令 `freely issue-sync comment-delete <local_id> --platform <github|gitee> --comment-id <id>`（等价 CLI 形态可自定，但必须显式平台与评论 ID）。\n2. 写前做身份校验：该 `<local_id>` 必须在本地文档中映射到该平台的 issue；评论 ID 必须属于该 issue；不匹配即拒绝，不执行删除。\n3. 删除后打印逐平台回执（deleted / absent / error），任一错误非零退出并给出可操作重试命令；不允许 `--force` / `--allow-degraded` 绕过。\n4. 不提供隐式平台裁剪（如 `GH_REPO=""`），平台必须由显式参数指定。\n5. AT：stub adapter 覆盖 0/1/3、身份不匹配拒绝、无调用方直连 gh/curl、commands.md 登记；回归既有 comment 创建路径。\n\n## 非目标\n不自动删除 #4734 的重复评论（需人工确认后用新命令执行）；不改 Gitee 仓库 `issue_comment` 设置；不改评论创建语义。\n\n## 证据\n- GitHub #4734 三条评论 ID 与时间：7215983525(10:31:21Z) / 7216177311(10:40:56Z) / 7216282291(10:46:09Z)。\n- Gitee IKYK8N 仅 1 条评论，`issue_comment=false` 导致 closed Issue 无法补评。
