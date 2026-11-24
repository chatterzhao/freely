---
schema_version: '1'
local_id: raw-20261124T054217Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4671'
    url: https://github.com/chatterzhao/freely/issues/4671
    synced_at: ''
  gitee:
    issue_id: IKXKYB
    url: https://gitee.com/zhaoquan/freely/issues/IKXKYB
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-24T05:42:18Z'
updated_at: '2026-11-24T05:42:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P1
---

# fix: issue-sync update 吞掉 Gitee 失败，部分成功伪装整体成功

workflow_kind: fix

## fix: issue-sync update 吞掉 Gitee 失败，部分成功伪装整体成功

| Field | Value |
|-------|-------|
| local_id | `raw-20261124T054217Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-24T05:42:18Z |
| updated | 2026-11-24T05:42:18Z |

---

> **Freely 治理**：这是 raw issue `raw-20261124T054217Z`。实现前请用 `wt-create --raw-key 20261124T054217Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象

`bin/issue-sync.d/cmd-update.sh:32`：Gitee 更新失败只 `echo ... >&2`，不传播状态；第 35 行 `echo update complete` 使函数返回 0。可能出现 GitHub 成功、Gitee 失败、命令整体仍成功。


与 Freely 强调的双平台一致性、fail-closed 原则冲突。上层 Runtime 会误以为双平台同步完成，长期无人值守时产生静默漂移。`pr-create-guarded` / `wt-close` 等链路均依赖平台状态一致性。` 与已有 #4136（Gitee PR 关闭时远端名当平台名）边界不同：本题是 update 路径的失败传播，非关闭路径。

## 修复方向

- 汇总两平台结果：github=success/failure、gitee=success/failure、overall=partial_failure。
- 任一平台失败即非零退出；不因 Gitee 缺 token 静默跳过（除非显式声明 skip 语义）。
- 增加可重试与幂等保护，避免重复写。

## 验收

- RED：mock Gitee 更新失败，命令非零退出且输出部分失败汇总。
- GREEN：双平台均成功时行为与当前一致。
