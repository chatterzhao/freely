---
schema_version: '1'
local_id: raw-20261126T120834Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261126T120834Z-A
platform_ids:
  github:
    issue_id: '4723'
    url: https://github.com/chatterzhao/freely/issues/4723
    synced_at: ''
  gitee:
    issue_id: IKY9OP
    url: https://gitee.com/zhaoquan/freely/issues/IKY9OP
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/issues/I-20261126T120834Z-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-26T12:08:34Z'
updated_at: '2026-11-26T12:08:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children:
- I-20261126T120834Z-A
source_candidate: docs/B1-docs/raw-20261126T120834Z/candidates.md#C-20261126T120834Z-A
completed_at: '2026-11-26T12:40:00Z'
closeout_note: ''
severity: P1
---

# fix: wt-close 退役门禁不认元数据等价测试证据

workflow_kind: fix

## fix: wt-close 退役门禁不认元数据等价测试证据

| Field | Value |
|-------|-------|
| local_id | `raw-20261126T120834Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/worktree-lifecycle/wt-close/raw-20261126T120834Z/issues/I-20261126T120834Z-A.md` |
| created | 2026-11-26T12:08:34Z |
| updated | 2026-11-26T12:08:34Z |

---

> **Freely 治理**：这是 raw issue `raw-20261126T120834Z`。实现前请用 `wt-create --raw-key 20261126T120834Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象
#4137 收口时：评审提交后已在 test 工位用 `test-evidence.py attest-meta` 沿袭证据，`pretests-gate`/`pr-create`/`pr-merge` 全部通过；但 `wt-close` 的 `pretests-retirement-gate` 仍报 `[pretests_stale] 测试工位有新提交但未重新跑测试`，要求重跑全量 CI（约 4 分钟）才能收口。

## 根因
`docs/system/workspace/scripts/quality/pretests-retirement-gate:124-140` 有一段独立于 `test-evidence.py validate` 的 freshness check：`_latest_commit != _last_tested_commit` 即 stale，完全不读 `EQUIVALENCE_CHAIN` / `EQUIVALENCE_SENSITIVE_PATHS`。而 `test-evidence.py validate`（#4703）已经返回 `current/equivalent/stale` 三态并通过同一份 gate 文件。

## 期望
退役门禁删除自造的 失效的 HEAD 精确相等判据，改用 `test-evidence.py validate --json` 的 verdict：`current` 与 `equivalent` 均放行，`stale` 拦截；保留原有的 `TEST_STATUS`/not_tested 与 `pretests-gate` 校验，不放宽任何真代码变更的重测要求。

## 边界
- 不改 `test-evidence.py` 的 `attest-meta` 判据与 HARD_EXCLUDED 列表；
- 不跳过 `pretests-gate`，不删 evidence sha256 绑定；
- 单字段元数据提交可沿袭，`bin/`、`docs/system/`、测试定义变化必须真重跑。

## 验收
- fixture：测试 HEAD = A（证据 ok），追加只改 `docs/B2-docs/**/code-reviews/*.md` 的提交 B → `attest-meta` 后 `pretests-retirement-gate` rc=0；
- 追加改 `bin/freely` 的提交 C → `attest-meta` 拒绝，退役门禁 rc=1；
- 仓库现有 `test-evidence.py` 三态单测全绿。
