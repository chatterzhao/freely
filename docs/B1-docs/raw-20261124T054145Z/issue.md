---
schema_version: '1'
local_id: raw-20261124T054145Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261124T054145Z-A
platform_ids:
  github:
    issue_id: '4669'
    url: https://github.com/chatterzhao/freely/issues/4669
    synced_at: ''
  gitee:
    issue_id: IKXKY8
    url: https://gitee.com/zhaoquan/freely/issues/IKXKY8
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/gate/ci-merge-protection/raw-20261124T054145Z/issues/I-20261124T054145Z-A.md
last_synced_comment_at:
  github: '2026-11-24T06:41:56Z'
  gitee: '2026-11-24T06:41:56Z'
hash: ''
created_at: '2026-11-24T05:41:45Z'
updated_at: '2026-11-24T06:42:02Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261124T054145Z-A
source_candidate: ''
completed_at: '2026-11-24T06:41:56Z'
closeout_note: ''
severity: P0
---

# fix: CI 合并保护链三处失效：guard 权限、分支保护、自签 check

workflow_kind: fix

## fix: CI 合并保护链三处失效：guard 权限、分支保护、自签 check

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T054145Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-24T05:41:45Z |
| updated | 2026-11-24T05:41:45Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T054145Z`。实现前请用 `wt-create --raw-key 20261124T054145Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（2026-11-23 用已认证 gh 通道实测）

1. `.github/workflows/pr-merge-guard.yml` 无 `permissions:` 块。CI run 43827151395 的 guard job 调用 `github.rest.checks.create()` 返回 403，响应头 `x-accepted-github-permissions: checks=write`；`governance/pr-merge-guard` check run 从未创建。该 run 的 check-runs 只有 `guard`/`verify`。
2. `gh api repos/chatterzhao/freely/branches/develop/protection` → HTTP 404 `Branch not protected`。网页 Merge 按钮当前不受任何治理 check 约束。
3. `docs/system/workspace/scripts/worktree/pr-merge-guarded:296-329` 的 `_set_governance_check_pass()`：找不到 check 时用 `gh api .../check-runs` 自行创建 `conclusion=success` 的同名 check，且 PATCH/POST 失败均 `|| true` 吞掉。执行者可自签验收章。

## 根因

治理链设计为 CI 建 in_progress check → 分支保护拦截 → 本地门禁跑完置 success。三个环节各有断点且互相掩盖：CI 第一步失败导致 check 不存在；分支保护未配置导致即使有 check 也不拦截；本地 fallback 自签导致即使前两步修好仍可绕过。

## 修复方向

- workflow 显式声明 `permissions: contents: read, checks: write`。
- develop 开启分支保护，require `governance/pr-merge-guard`，`enforce_admins: true`。
- 移除 pr-merge-guarded 的自签 fallback：check 不存在即 fail-closed，API 失败非零退出。

## 验收

- CI run guard job success，目标 commit 上存在 `governance/pr-merge-guard` check。
- 分支保护 API 返回 required_status_checks 含该 check 且 enforce_admins 为真。
- RED 测试证明：check 缺失或 API 失败时 pr-merge-guarded 非零退出，不自签。

### comment-20261124T064156Z
- source: system
- event: promote_finalized
- children: ["I-20261124T054145Z-A"]

拆解为以下任务:
1. [I-20261124T054145Z-A](will-be-updated)
