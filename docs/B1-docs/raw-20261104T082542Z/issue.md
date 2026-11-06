---
schema_version: '1'
local_id: raw-20261104T082542Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261104T082542Z-A
platform_ids:
  github:
    issue_id: '4181'
    url: https://github.com/chatterzhao/freely/issues/4181
    synced_at: ''
  gitee:
    issue_id: IKSWR8
    url: https://gitee.com/zhaoquan/freely/issues/IKSWR8
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-04T08:25:42Z'
updated_at: '2026-11-06T08:33:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T08:25:00Z'
closeout_note: ''
---

# fix: raw-issue-pull 物化后不写一级标题，导致 PR 门禁判定 content_diverged

workflow_kind: fix

## 根因
`raw-issue-pull` 从平台物化 raw issue 时，只写 frontmatter、`workflow_kind` 与正文，**不写 `# <title>` 行**。而 `issue-sync` 的 `_issue_title` 与 parity 比较都依赖一级标题，导致本地 title 为空。

## 证据
- `docs/system/workspace/scripts/sync/platform-adapter.py` 的 `pull_raw_issue()`：取 `title = info.get("title","")` 后仅用于 raw key 校验，落盘 payload 不含标题行。
- 实测：`raw-20261104T074512Z/issue.md` 物化后无 `# ` 行；`gh` 侧标题存在。
- `pr-create-guarded` Step 0b 报 `{"scope":"local","code":"content_diverged","detail":"local canonical content differs from platforms"}`，PR 被阻断。
- 本地 799 条 raw 中 700 条无标题（87.6%），与本次缺陷同源。

## 影响
- 所有经 `wt-create` 物化的新 raw issue 在首次 PR 时都会被 parity 判定为 diverged，必须人工补标题才能继续。
- 本地 raw 不可按标题检索，判重与 scan 失效。

## 修复方案
1. `pull_raw_issue()` 落盘时在 frontmatter 之后写入 `# <title>`（去掉 `[RAW-<key>] ` 前缀，与本地约定一致）。
2. 补一条单测：物化后文件必须含一级标题，且与平台标题一致。
3. 提供一次性回填命令：对本地无标题的 raw 批量补 `# ` 行（默认 dry-run）。

## 验收标准
- RED：对任一平台 raw 执行 pull，断言 issue.md 含 `# ` 行；当前缺失。
- GREEN：新建 raw → wt-create → pr-create-guarded 不再报 content_diverged。
- GREEN：回填命令对 700 条无标题 raw 输出 dry-run 清单，执行后全部含标题。
