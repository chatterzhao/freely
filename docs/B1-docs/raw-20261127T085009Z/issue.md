---
schema_version: '1'
local_id: raw-20261127T085009Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261127T085009Z-A
platform_ids:
  github:
    issue_id: '4731'
    url: https://github.com/chatterzhao/freely/issues/4731
    synced_at: ''
  gitee:
    issue_id: IKYJ83
    url: https://gitee.com/zhaoquan/freely/issues/IKYJ83
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/issues/I-20261127T085009Z-A.md
last_synced_comment_at:
  github: '2026-11-27T09:23:27Z'
  gitee: '2026-11-27T09:23:27Z'
hash: ''
created_at: '2026-11-27T08:50:09Z'
updated_at: '2026-11-27T09:23:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261127T085009Z-A
source_candidate: ''
completed_at: '2026-11-27T09:23:26Z'
closeout_note: ''
severity: P1
---

# fix: 仅单平台副本的 legacy raw 无法物化（wt-create 与 raw-issue-pull 互锁）

workflow_kind: fix

## fix: 仅单平台副本的 legacy raw 无法物化（wt-create 与 raw-issue-pull 互锁）

| Field | Value |
|-------|-------|
| local_id | `raw-20261127T085009Z` |
| kind | `raw` |
| phase_state | `absorbed` |
| canonical | `docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/issues/I-20261127T085009Z-A.md` |
| created | 2026-11-27T08:50:09Z |
| updated | 2026-11-27T08:50:09Z |

---

> **Freely 治理**：这是 raw issue `raw-20261127T085009Z`。实现前请用 `wt-create --raw-key 20261127T085009Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象\nraw-20261108T134701Z（R59，Gitee IKTSRS）只有 Gitee 副本、无 GitHub 副本。\n1. `freely wt-create --raw-key 20261108T134701Z --source platform` 拒绝：`configured raw replicas are inconsistent or unavailable`。\n2. `freely raw-issue-pull --raw-key 20261108T134701Z` 拒绝：只能在包含该 raw-key 的 fix/feature 工位执行；而该工位正是第 1 步无法创建的。\n3. 手工 `git worktree add -b ...` 被 reference-transaction hook 正确拦截（禁止绕过工位封装）。\n4. `freely issue-sync create` 需要本地 issue.md，同样无法生成。\n形成互锁：补副本需要工位，工位需要副本。\n\n## 根因\n工位真源检查要求「所有配置平台副本齐全」才能物化，但没有为「历史单平台 raw」提供显式的补副本封装入口；`raw-issue-pull` 又限定只能从已有工位运行。\n\n## 期望\n1. 提供封装命令（例如 `freely issue-sync create --from-platform gitee <raw-key>` 或 `freely raw-issue-pull --allow-missing-platform` 的显式审计入口），在双平台配置下按已有副本物化本地文档并补齐缺失平台副本，逐平台结果汇总、失败非零。\n2. 不允许 `--force` / `--allow-degraded` 绕过事实类诊断；所有补副本动作经 adapter 双平台汇总。\n3. AT：单平台 legacy raw → 物化成功 + 缺失副本补齐；两平台均缺 → fail-closed；平台不可读 → 非零且打印可执行重试命令。\n\n## 非目标\n不实现 R59 本身的 install 命令；R59 继续排在补副本能力之后。\n\n## 证据\n- wt-create 回执：`configured raw replicas are inconsistent or unavailable`（observations 仅 gitee）。\n- raw-issue-pull 回执：`当前分支 ... 不包含 raw-key`。\n- git worktree add 回执：`fatal: in 'prepared' phase, update aborted by the reference-transaction hook`。

### comment-20261127T092326Z
- source: system
- event: promote_finalized
- children: ["I-20261127T085009Z-A"]

拆解为以下任务:
1. [I-20261127T085009Z-A](will-be-updated)
