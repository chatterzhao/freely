---
schema_version: '1'
local_id: raw-20261124T072402Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261124T072402Z-A
platform_ids:
  github:
    issue_id: '4675'
    url: https://github.com/chatterzhao/freely/issues/4675
    synced_at: ''
  gitee:
    issue_id: IKXMQR
    url: https://gitee.com/zhaoquan/freely/issues/IKXMQR
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/issues/I-20261124T072402Z-A.md
last_synced_comment_at:
  github: '2026-11-24T07:59:38Z'
  gitee: '2026-11-24T07:59:38Z'
hash: ''
created_at: '2026-11-24T07:24:03Z'
updated_at: '2026-11-24T07:59:43Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261124T072402Z-A
source_candidate: ''
completed_at: '2026-11-24T07:59:37Z'
closeout_note: ''
severity: P0
---

# fix: governance check 无人置 success，分支保护无法安全启用

workflow_kind: fix

## fix: governance check 无人置 success，分支保护无法安全启用

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T072402Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-24T07:24:03Z |
| updated | 2026-11-24T07:24:03Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T072402Z`。实现前请用 `wt-create --raw-key 20261124T072402Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

raw-20261124T054145Z 修复了 CI guard 的 `checks: write` 权限（guard job 已从 403 变 success，`governance/pr-merge-guard` check 能被创建），但全仓 grep 证实 `_set_governance_check_pass()` 只有定义、无调用点——**没有任何机制把该 check 从 in_progress 置为 success**。CI run 45346477702 的 check runs 显示该 check `conclusion: null`。

## 为何重要（这是配置分支保护的陷阱）

按 .github/workflows/pr-merge-guard.yml:1-31 注释配置 develop 分支保护（require governance/pr-merge-guard）后，所有 PR 会卡死：check 永远 in_progress，无人置 success。本轮实测配置后立即回退（已恢复 protected:false），避免卡死。

## 根因：时序死锁

GitHub 分支保护要求 merge 前 check=success；但治理 check 应在 pr-merge-guarded 跑完全部门禁后才置 success；而 pr-merge-guarded 的 merge 又受该保护阻挡。workflow 注释的设计在「先 merge 后置 success」的顺序下自相矛盾。

## 需要的方向（不在本 raw scope）

- 找到 merge 前置 success 的合法接线点（gate 全部通过后、git merge 之前），或改用 GitHub App token 由 CI 侧在验证通过后置 success。
- 明确「谁拥有 check 的最终判定」——不应由执行者自签，也不应留在无人调用的死代码里。
- 设计可实测的 E2E：配置保护后，合规 PR 能合并、违规 PR 被拦。

## 与前一条的关系

raw-20261124T054145Z（#4669）只修了权限与 fail-closed，分支保护因本缺陷无法安全落地并已回退。本条是它的前置依赖。

### comment-20261124T075937Z
- source: system
- event: promote_finalized
- children: ["I-20261124T072402Z-A"]

拆解为以下任务:
1. [I-20261124T072402Z-A](will-be-updated)
