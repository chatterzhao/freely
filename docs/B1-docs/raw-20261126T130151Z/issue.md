---
schema_version: '1'
local_id: raw-20261126T130151Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261126T130151Z-A
platform_ids:
  github:
    issue_id: '4726'
    url: https://github.com/chatterzhao/freely/issues/4726
    synced_at: ''
  gitee:
    issue_id: IKYAHY
    url: https://gitee.com/zhaoquan/freely/issues/IKYAHY
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/issues/I-20261126T130151Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-26T13:01:51Z'
updated_at: '2026-11-26T13:02:05Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children:
- I-20261126T130151Z-A
source_candidate: docs/B1-docs/raw-20261126T130151Z/candidates.md#C-20261126T130151Z-A
completed_at: '2026-11-26T13:35:00Z'
closeout_note: ''
severity: P1
---

# fix: pr-merge followthrough 重置 test HEAD 后未沿袭证据

workflow_kind: fix

## fix: pr-merge followthrough 重置 test HEAD 后未沿袭证据

| Field | Value |
|-------|-------|
| local_id | `raw-20261126T130151Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/issues/I-20261126T130151Z-A.md` |
| created | 2026-11-26T13:01:51Z |
| updated | 2026-11-26T13:01:51Z |

---

> **Freely 治理**：这是 raw issue `raw-20261126T130151Z`。实现前请用 `wt-create --raw-key 20261126T130151Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
#4137 与 #4722 连续两轮：pr-merge 成功后 followthrough 把 test-pre-merge 工位 reset 到 develop merge commit，但 test-gate.env 的 EQUIVALENCE_CHAIN 仍停在 PR 分支最后提交。随后 `wt-close` 的退役门禁判 stale，要求重跑全量 CI（约 5 分钟）或手工执行 attest-meta 才能收口。

## 根因
pr-merge followthrough 只做 `git reset --hard <merge commit>`（或等价同步），没有调用 `test-evidence.py attest-meta`。merge commit 的内容与已测试的 PR HEAD 完全一致（`git diff PR_HEAD..MERGE` 为空），属于 #4703 定义的元数据等价提交，应自动沿袭证据。

## 期望
`pr-merge-guarded` 在 followthrough 重置 test 工位 HEAD 后，若 `git diff <tested_head>..<new_head>` 与敏感路径交集为空且测试定义指纹未变，自动调用 `test-evidence.py attest-meta` 把新 HEAD 加入 EQUIVALENCE_CHAIN，并打印沿袭回执（from → to、changed_paths）；若命中敏感路径则**不沿袭**，打印要求重跑的明确指引。

## 边界
- 不改 `test-evidence.py` 的 attest-meta 判据与 HARD_EXCLUDED；
- 不伪造证据：只对真实等价提交沿袭，失败 fail-closed；
- 不改变 wt-close 退役门禁的校验（仍以 validate 三态为准）；
- test 工位不产生原创提交。

## 验收
- fixture：PR HEAD A 有 GREEN 证据 → merge 到 develop 得 B（`git diff A..B` 空）→ followthrough 后 chain 含 B，wt-close 退役门禁 rc=0；
- 反例：merge 后 develop 另有真代码提交 C → 沿袭拒绝，wt-close rc=1 且打印重跑命令；
- 既有 test-evidence 三态单测与两轮真实收口回归。
