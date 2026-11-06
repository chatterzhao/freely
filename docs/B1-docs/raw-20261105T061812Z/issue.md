---
schema_version: '1'
local_id: raw-20261105T061812Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T061812Z-A
platform_ids:
  github:
    issue_id: '4190'
    url: https://github.com/chatterzhao/freely/issues/4190
    synced_at: ''
  gitee:
    issue_id: IKT4B1
    url: https://gitee.com/zhaoquan/freely/issues/IKT4B1
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T06:18:12Z'
updated_at: '2026-11-05T06:18:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T08:55:00Z'
closeout_note: ''
---

# fix: wt-create 四态判定只查分支不查工位目录，半初始化工位被误判为已完成

workflow_kind: fix

优先级：P1（工具链语义错误，影响中断恢复时的正确性判定）

## 现象

`wt-create` 的四态幂等判定只用 `git show-ref --verify --quiet refs/heads/<branch>` 检查分支是否存在，既不检查对应 worktree 目录是否仍然存在，也不检查 test 工位的初始化是否完成。

## 影响

- 分支保留而工位目录被移除（工位被手工删除、磁盘清理、worktree prune）时，重跑会被判为「两个工位都在」并 no-op 退出码 0，但实际没有任何可用工位，后续 B1/B2 与测试全部落空。
- Step 2 中途失败会留下「test 分支已建但 seed / .freely 状态 / test-gate.env 未完成」的工位，四态判定同样视为 no-op，不会重跑初始化，PR 门禁随后报 pretests_not_tested。
- 「dev 缺 / test 在」的不一致拒绝态目前只有静态结构断言，缺少独立的行为回归测试。

## 修复方向

1. 四态判定同时校验分支与 worktree 目录存在性，区分「分支在但工位不在」并进入补建路径。
2. 为 test 工位写入初始化完成标记，no-op 前校验该标记，缺失时重跑 `_init_test_worktree_state()`。
3. 补行为回归测试，覆盖上述半初始化、目录缺失与不一致拒绝态的真实执行，保持双工位齐全时的幂等 no-op。

## 验收标准

- RED：构造「分支在、工位目录不在」与「test 分支在但缺 test-gate.env」两种残留，重跑同一 `wt-create` 命令，当前实现应错误地 no-op。
- GREEN：修复后两种残留都能补齐工位与初始化；「dev 缺 / test 在」仍拒绝；双工位齐全时仍是幂等 no-op 且不产生重复工位。
