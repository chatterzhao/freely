---
schema_version: '1'
local_id: raw-20261127T100325Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261127T100325Z-A
platform_ids:
  github:
    issue_id: '4734'
    url: https://github.com/chatterzhao/freely/issues/4734
    synced_at: ''
  gitee:
    issue_id: IKYK8N
    url: https://gitee.com/zhaoquan/freely/issues/IKYK8N
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/issues/I-20261127T100325Z-A.md
last_synced_comment_at:
  github: '2026-11-27T10:31:13Z'
  gitee: '2026-11-27T10:31:13Z'
hash: ''
created_at: '2026-11-27T10:03:25Z'
updated_at: '2026-11-27T10:31:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261127T100325Z-A
source_candidate: ''
completed_at: '2026-11-27T10:31:13Z'
closeout_note: ''
severity: P1
---

# fix: 单平台物化的失败回执全角冒号导致 unbound variable

workflow_kind: fix

## fix: 单平台物化的失败回执全角冒号导致 unbound variable

| Field | Value |
|-------|-------|
| local_id | `raw-20261127T100325Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/issues/I-20261127T100325Z-A.md` |
| created | 2026-11-27T10:03:25Z |
| updated | 2026-11-27T10:03:25Z |

---

> **Freely 治理**：这是 raw issue `raw-20261127T100325Z`。实现前请用 `wt-create --raw-key 20261127T100325Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象\n#4731 新增的 wt-create 显式 source-platform 路径中，失败回执写作 `补齐缺失平台副本（$raw_key）`，其中 **全角冒号不在变量名边界内**：bash 将 `raw_key：` 解析为变量名，在 `set -u` 下抛 `raw_key： unbound variable`，掩盖了原始的 issue-sync create 部分失败回执。\n\n## 实证\nR59 现场（raw-20261108T134701Z）：\n- Gitee 副本可读，GitHub 副本缺失；`issue-sync create` 正确返回 PARTIAL（github failed / gitee skipped）。\n- wt-create 进入拒绝分支后抛 `/docs/.../wt-create: line 1038: raw_key： unbound variable`，未打印预期的可执行拒绝信息。\n\n## 根因\nShell 双引号内 `$raw_key：` 的变量名边界包含全角标点；应使用 `${raw_key}` 或 ASCII 标点。\n\n## 期望\n1. 所有新增 shell 字符串中的变量引用统一用 `${var}` 显式边界。\n2. AT：在 `set -u` 下以 stub issue-sync 返回非零，必须打印「拒绝创建工位: issue-sync create 未能补齐缺失平台副本（raw-<key>）」而非 unbound variable。\n3. 回归：#4731 的 10 项 AT 全绿。\n\n## 非目标\n不处理 GitHub 平台侧身份不可达本身（那是平台可用性问题，回执已正确 fail-closed）。\n\n## 证据\n- 命令：`freely wt-create --raw-key 20261108T134701Z --source-platform gitee --source platform --kind fix --slug install-command-parity`\n- 输出：`[issue-sync] create PARTIAL: created=gitee failed=github` 后接 `raw_key： unbound variable`。

### comment-20261127T103113Z
- source: system
- event: promote_finalized
- children: ["I-20261127T100325Z-A"]

拆解为以下任务:
1. [I-20261127T100325Z-A](will-be-updated)
