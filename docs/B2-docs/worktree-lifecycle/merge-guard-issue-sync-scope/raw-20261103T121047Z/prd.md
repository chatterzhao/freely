# PRD: merge 时 issue-sync 按 lane raw key 收敛 + Gitee reopen 形态修复

- issue_id: I-20261103T121047Z-A

## Goal
pr-merge-guarded 在合并时只推进/关闭属于当前分支 raw key 的 issue；其他被 diff 触及的 raw 文档（物化/回填等治理数据）保持原状。gitee-issue.py reopen 与 close 使用同一可用请求形态。

## Modules
- 新增 `docs/system/workspace/scripts/worktree/issue-sync-scope.py`：`filter_issue_ids(ids, raw_key)` 纯函数 + CLI。
- `pr-merge-guarded` `_sync_issues_changed_in_merge`：changed_issues 计算后按分支 raw key 过滤。
- `gitee-issue.py`：新增 `reopen_request(repo, number)`，cmd_reopen 改用它。

## Invariants
- 正常 lane（diff 只含自己 raw/I-* 文档）行为不变。
- 分支名无 raw key 时不过滤（兼容历史）。
- reopen 形态与已可用的 close 形态一致。

## Non-Goals
- 不新增平台写操作、不改 scan/gate 语义。
- 不处理历史已关闭 issue（已人工重开恢复）。

## Eval Plan
- unit：scope 过滤 + reopen request 构造。
- integration：test-pre-merge 跑两个单测。

## Dev-Loop Handoff
RED：两个单测 import 失败/断言失败；实现后 GREEN。
