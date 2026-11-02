---
schema_version: '1'
local_id: raw-20261102T133249Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261102T133249Z-A
platform_ids:
  github:
    issue_id: '4128'
    url: https://github.com/chatterzhao/freely/issues/4128
    synced_at: ''
  gitee:
    issue_id: IKSFC7
    url: https://gitee.com/zhaoquan/freely/issues/IKSFC7
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-02T13:32:49Z'
updated_at: '2026-11-02T13:32:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: '2026-11-02T13:38:14Z'
closeout_note: ''
---

# [RAW-20261102T133249Z] fix: owner-lane 认领被当前路径不等于项目的守卫挡住

workflow_kind: fix

## 现象

上一轮合入的 owner-lane 身份认领（I-20261102T103231Z-A）在真实路径上**从未生效**。在 owner 自建、`agent_working` 无行的工位里执行 daemon 启动，仍然报：

    unable to resolve agent identity for <worktree>: agent_working has no entry

此前之所以“验证通过”，是因为我先手工执行过一次 claim，把行写进去了；daemon 内的自动认领一次都没有跑过。

## 根因

`_resolve_current_agent_id` 里的守卫条件写错了：

    if [[ -z "$_my_id" && "$_current_path" != "$project" ]]; then
      ... claim ...

`_current_path` 是 `pwd`，`$project` 是传给函数的项目路径。daemon 在工位内启动时，两**者相同**，条件恒为假，整个 claim 分支被跳过。当时加这个守卫是为了避免在项目根误认领，但它恰好把唯一需要认领的场景排除了。

## 影响

- owner lane 仍然起不了 daemon，上一轮宣称的“自举”不成立。
- 因为失败表现与修复前一致（同样一句 agent_working has no entry），很容易被当成“只是还没修”。

## 修复方向

1. 去掉 `!=` 守卫。
2. 依靠既有守卫保证安全（这些在 claim 内部已实现，不需要外层再挡）：
   - 该路径零行才认领，已有绑定原样返回；
   - 项目只能有一个 manager；
   - 路径必须是 `git worktree list` 里的 worktree；
   - 分支必须能解析出 raw key —— 项目根的分支是 develop，解析失败，自然不会认领。
3. `2>/dev/null` 改为捕获 stderr，失败原因写进日志（本次排查就卡在“看不到原因”）。

## 验收

1. 新建工位（`agent_working` 零行）直接 `daemon start`，日志出现 `owner-lane claim: <path> → manager_01`，且启动成功。
2. 已认领的工位再次启动，不再重复写入（走 existing 分支）。
3. 项目根启动不产生认领（分支无法解析 raw key）。
4. 认领失败时日志包含具体 reason（`manager_not_unique` / `not_a_worktree` / `raw_key_unresolved` / `rows_unreadable`）。
5. 新增一个“project == path”的用例，防止该守卫再次回归。
