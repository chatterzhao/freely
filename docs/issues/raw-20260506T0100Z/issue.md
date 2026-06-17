---
local_id: raw-20260506T0100Z
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
kind: raw
source_family: chat_inbox
created: 2026-05-06 01:00:00+00:00
platform_ids:
  github:
    issue_id: '274'
    url: https://github.com/chatterzhao/freely/issues/274
    synced_at: '2026-05-10T09:29:04Z'
updated_at: '2026-06-17T00:18:05Z'
primary_platform: github
created_at: '2026-05-10T09:29:04Z'
platform_state: closed
---

# raw-20260506T0100Z: scan 盲区——文档链解析错误和断链导致漏扫

## 现象

`task-lifecycle-scan.py` 漏扫了两类本该出现的项：

1. `raw-20260505T1210Z`（issue state refactor）在 milestone 已有 3 个 committed I-* issue，但 scan 误报 `b1_candidate`（candidate 未决策），因为 candidates.md 中 `status: promoted` 的条目未被识别
2. `I-20260421-1530-A`（live-status scan summary）在 milestone 标记 `in_verification`，但 scan 完全没输出——raw dir 已清理，I-* child 孤立

## 根因

### Bug 1: `_parse_h3_sections` 硬编码 `###` 级别

candidates.md 的候选条目用 `## C-xxx`（h2），子节（`### 改动`、`### 验证`）才用 h3。scan 只 split `###`，导致：
- 看到的"section"是"改动""验证"（无 status 字段）
- 真正的候选元数据（`status: promoted`）在 `##` 下，完全不可见
- → 所有 candidate 判定失败 → `candidate_not_decided`

### Bug 2: `_all_base_keys` 无 I-* 来源

key 发现只有两个来源：chat_inbox + `docs/issues/raw-*` 目录。当 raw dir 不存在（完整生命周期走完后清理）但 I-* children 仍存在时，整条链不可见。需要增加 `docs/issues/I-*` 作为 key 来源。

## scan 职责边界（不修的部分）

- **不覆盖 git stash** — scan 是文档链生命周期工具，不是 git 状态管理器
- **不覆盖 test-pre-merge 分支** — 受 `_is_protected_branch` 保护，显式排除
- **不覆盖 milestone 专属 entry** — milestone committed_issues 是另一条治理路径
- **不管没有文档链的裸 git 分支** — 没有 raw → B1 → I 链的分支由 `scan_worktree_governance` 处理
