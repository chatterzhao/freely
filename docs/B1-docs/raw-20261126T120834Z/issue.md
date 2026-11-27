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
updated_at: '2026-11-27T06:56:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
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

### comment-20261126T124546Z
- source: system
- event: root_cause_correction

## 根因更正（2026-11-26，本会话自查）

先前立项描述「退役门禁不认元数据等价证据」经源码复查**不成立**，更正如下：

- `docs/system/workspace/scripts/quality/pretests-retirement-gate:122-124` 使用 `_sp.check_output(...)` / `_sp.DEVNULL`，但脚本只 `import subprocess`（:40），从未定义 `_sp`；`try/except Exception: pass` 把 NameError 吞掉，`_latest_commit` 恒空 → 那段自造 HEAD 相等判据（`:140-149`）是死代码，从未生效。
- 真正拦截 wt-close 的是其后的 `test-evidence.py validate --json`（#4703 三态判据），该判据对 equivalent 放行、stale 拦截，行为正确。
- 实测 develop 基线：做完 `attest-meta` 后退役门禁 rc=0；只有真代码变更（未重跑）才 rc=1。

## 本 issue 的真正范围

修复死代码与静默吞异常：删除整段自造 freshness check（`:120-149`），以 `test-evidence.py validate --json` 的 verdict 为唯一新鲜度判据；保留 not_tested、evidence sha256 绑定与 pretests-gate 校验。不改 `test-evidence.py` 的判据与 HARD_EXCLUDED，不放宽 stale/not_tested。

## 验收

- AT：gate 源码无 `pretests_stale` / `_sp.check_output`；fixture 三态 equivalent rc=0、stale rc=1、not_tested rc=1。
- 既有 `test-evidence.py` 三态单测与 #4137 收口证据回归。
