---
schema_version: '1'
local_id: raw-20261127T131717Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261127T131717Z-A
platform_ids:
  github:
    issue_id: '4743'
    url: https://github.com/chatterzhao/freely/issues/4743
    synced_at: ''
  gitee:
    issue_id: IKYL2Q
    url: https://gitee.com/zhaoquan/freely/issues/IKYL2Q
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/issues/I-20261127T131717Z-A.md
last_synced_comment_at:
  github: '2026-11-27T13:32:47Z'
  gitee: '2026-11-27T13:32:47Z'
hash: ''
created_at: '2026-11-27T13:17:17Z'
updated_at: '2026-11-27T13:32:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261127T131717Z-A
source_candidate: ''
completed_at: '2026-11-27T13:32:46Z'
closeout_note: ''
severity: P1
---

# fix: 平台身份发现把正文提及的 raw key 误判为副本，导致 create 永久 indeterminate

workflow_kind: fix

## fix: 平台身份发现把正文提及的 raw key 误判为副本，导致 create 永久 indeterminate

| Field | Value |
|-------|-------|
| local_id | `raw-20261127T131717Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/issues/I-20261127T131717Z-A.md` |
| created | 2026-11-27T13:17:17Z |
| updated | 2026-11-27T13:17:17Z |

---

> **Freely 治理**：这是 raw issue `raw-20261127T131717Z`。实现前请用 `wt-create --raw-key 20261127T131717Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象\nR59（raw-20261108T134701Z）只有 Gitee 副本，需补 GitHub 副本。`freely issue-sync create` 返回：\n`[issue-sync] GitHub: platform-side identity undetermined; refusing to create (rerun after platform recovers)`\n重试多次仍失败。\n\n## 精确根因\n`platform-adapter.py` 的 `GitHubHandler.search_raw_issue()` / `GiteeHandler.search_raw_issue()` 同时搜索 title 和 body，只要文本含 `raw-<key>` 就算候选。\n- R59 的 discover-raw 回执：github `status=ambiguous, reason=duplicate_matches, raw key ... is ambiguous: 4 matches`。\n- 实际 4 个命中是 #4734 / #4731 / #4645 等 issue，正文里引用了 R59 的 raw key（我们写反馈时引用的），**标题没有 R59 身份前缀**。\n- 于是 `_replica_decide` 得到 indeterminate，create 按设计 fail-closed 拒绝，形成永久阻塞。\n\n## 根因判断\n**身份判据错误**，不是平台不可读，也不是 create 的 fail-closed 策略错误。身份只能由标题前缀 `[RAW-<key>]` 或 `[I-<key>-<suffix>]` 决定；正文引用不是身份。\n\n## 期望\n1. 两个 handler 的 search_raw_issue 只按规范标题前缀匹配 raw key，不再用 body 文本参与身份判定。\n2. 保留 title 搜索的只读查询以发现候选；候选必须再经标题前缀校验才算副本。\n3. 多个合法前缀副本仍返回 ambiguous（fail-closed），不得擅自选一个。\n4. AT：body 含 key 但标题无前缀 → 0 匹配；标题有规范前缀 → 唯一匹配；两个规范副本 → ambiguous；Gitee/GitHub 两 handler 同一判据。\n5. 回归：R59 `issue-sync create` 能补全 GitHub 副本。\n\n## 非目标\n不改 raw_title_contract 的标题格式；不放宽 create 的 indeterminate 拒绝；不改平台写通道。\n\n## 证据\n- discover-raw GitHub：4 matches（#4734/#4731/#4645 等正文引用）。\n- 实际平台检索：无标题含 `[RAW-20261108T134701Z]` 的 GitHub issue。

### comment-20261127T133246Z
- source: system
- event: promote_finalized
- children: ["I-20261127T131717Z-A"]

拆解为以下任务:
1. [I-20261127T131717Z-A](will-be-updated)
