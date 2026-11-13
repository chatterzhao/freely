---
schema_version: '1'
local_id: raw-20261111T125724Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261111T125724Z-A
platform_ids:
  github:
    issue_id: '4302'
    url: https://github.com/chatterzhao/freely/issues/4302
    synced_at: ''
  gitee:
    issue_id: IKUOLX
    url: https://gitee.com/zhaoquan/freely/issues/IKUOLX
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/command-wrapper/pr-review-projection/raw-20261111T125724Z/issues/I-20261111T125724Z-A.md
last_synced_comment_at:
  github: '2026-11-13T10:40:48Z'
  gitee: '2026-11-13T10:40:48Z'
hash: ''
created_at: '2026-11-11T12:57:24Z'
updated_at: '2026-11-13T11:02:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261111T125724Z-A
source_candidate: ''
completed_at: '2026-11-13T10:40:48Z'
closeout_note: ''
severity: P2
---

# refactor: 收敛 bin/ 剩余业务实现并收缩投影注册表

workflow_kind: feature

## refactor: 收敛 bin/ 剩余业务实现并收缩投影注册表

| Field | Value |
|-------|-------|
| local_id | `raw-20261111T125724Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-11T12:57:24Z |
| updated | 2026-11-11T12:57:24Z |

---

> **Freely 治理**：这是 raw issue `raw-20261111T125724Z`。实现前请用 `wt-create --raw-key 20261111T125724Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 根因

#4175 要求把 `bin/pr-review-guarded` 的业务实现移回 `workspace/scripts/**`，并盘点其余 `bin/` 入口。
R32 已完成迁移，并新增 `docs/system/workspace/scripts/bin-projections.yaml` 注册表 +
`bin/check-bin-projection` 门禁：超过 40 行的 `bin/` 文件必须登记理由，登记后一旦变成投影
（≤40 行）就必须删除条目，否则门禁失败。

盘点结果是：98 个 `bin/` 入口里 **37 个超过 40 行**，其中一部分是合理的（`bin/issue-sync` 只做
模块加载与路径解析、`bin/test-all` 是聚合测试入口），但另有一部分确实是「实现放在 bin/」：
`freely-package`、`freely-review`、`freely-watchdog`、`freely-cycle`、`deploy-skills`、
`agent-table-query`、`issue-sync-batch.py`、`raw-issue-pull`、`issue-sync-bootstrap`、
`pre-init-runtime`、`git-worktree-guard`、`issue-index`、`cache-baseline`、`test-pre-merge-selfhost` 等。

## 影响

- 修改者仍不知道某条命令的真源在 `bin/` 还是 `workspace/scripts/`。
- 打包与安装态可能漏带真源（`bin/` 与 `scripts/` 的打包白名单不同）。
- 无法复用：`scripts/` 下的模块无法 import `bin/` 里的函数。

## 修复方案

1. 按 `bin-projections.yaml` 的 `implementation-in-bin` 清单逐个判定「是否应成为 scripts/ 投影」，
   不搞一刀切：自包含的 lint/聚合入口（`check-*`、`test-all`）保留在 `bin/`，并在注册表里
   标 `standalone-tool`，理由写清楚。
2. 判定应迁移者：实现移到 `docs/system/workspace/scripts/<domain>/`，`bin/<cmd>` 变
   `exec` 投影（≤8 行），随后删除注册表条目 —— 门禁会强制删除。
3. 每批迁移独立可合并、行为不变，用现有测试验证；改到 `scripts/runtime/` 的批次必须同轮
   补 `tests/unit/t-*.sh`（R27 契约）。
4. 完成后把注册表收缩到只剩 `dispatcher` 与 `standalone-tool` 两类。

## 验收标准

- RED：注册表里 `implementation-in-bin` 条目仍存在。
- GREEN：`implementation-in-bin` 条目清零，或每条都有明确「保留在 bin/ 的理由」并改标
  `standalone-tool`。
- GREEN：`bin/check-bin-projection` 仍 0 退出，且注册表无过期条目。
- 不退化：`bin/freely` 的分派与所有命令行为不变。

### comment-20261113T104048Z
- source: system
- event: promote_finalized
- children: ["I-20261111T125724Z-A"]

拆解为以下任务:
1. [I-20261111T125724Z-A](will-be-updated)
