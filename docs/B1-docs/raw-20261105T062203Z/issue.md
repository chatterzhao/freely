---
schema_version: '1'
local_id: raw-20261105T062203Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261105T062203Z-A
platform_ids:
  github:
    issue_id: '4191'
    url: https://github.com/chatterzhao/freely/issues/4191
    synced_at: ''
  gitee:
    issue_id: IKT4DY
    url: https://gitee.com/zhaoquan/freely/issues/IKT4DY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-05T06:22:03Z'
updated_at: '2026-11-06T09:25:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-06T09:25:00Z'
closeout_note: ''
---

# fix: wt-create 恢复模式把已存在的 dev 工位解析成带 hash 后缀的不存在路径

workflow_kind: fix

优先级：P1（恢复路径把错误状态写入 scan state，不阻断主链路但污染工位定位）

## 现象

`wt-create` 恢复模式（`resume_mode=1`）补建缺失的 test-pre-merge 工位后，用 `freely_wt_resolve_target_path "$dev_branch"` 取得 dev 工位路径，用在两处：恢复摘要打印，以及 `_update_scan_state` 写入 `scan_state_worktree`。

## 根因

`freely_wt_resolve_target_path()` 的语义是「为**即将新建**的工位计算目标路径」：目标目录已存在时追加分支名 sha1 前 8 位后缀以避免冲突。恢复模式下 dev 工位**本来就已存在**，因此该函数必然返回一个带后缀、实际上不存在的路径。

## 实测

在真实项目执行 `freely wt-create --raw-key 20261104T074512Z --source platform --kind fix --slug package-output-guard`，恢复成功、test 工位与 `test-gate.env` 均创建正确，但摘要打印 `dev (kept): .../fix-raw-20261104T074512Z-package-output-guard-0dd8a968`（该目录不存在）；同时 `.freely/run/manager-task-source-scan-latest.json` 中该 raw key 的 `scan_state_worktree` 被写成同一错误路径。真实 dev 工位路径没有后缀。该运行时字段已现场修正，代码缺陷仍在。

## 影响

- 恢复摘要给出不存在的 dev 路径，自动化或人按提示进入工位会失败。
- scan state 的 worktree 字段指向不存在目录，依赖该字段定位工位的后续逻辑会误判。
- AT-002 只断言 test 工位的创建与初始化，没有断言 dev 路径解析，因此没有捕获。

## 修复方向

1. 恢复模式改为从 `git worktree list --porcelain` 按 dev 分支反查真实工位路径，不再复用「新建目标路径」函数。
2. 恢复摘要与 `_update_scan_state` 都使用反查结果；反查不到时报错，不要猜测路径。
3. AT-002 增加断言：恢复输出的 dev 路径必须存在且等于预建的 dev 工位路径，scan state 的 worktree 字段与之一致。

## 验收标准

- RED：现有恢复模式在 dev 工位已存在时输出带 hash 后缀的不存在路径，且把该路径写入 scan state。
- GREEN：修复后输出与 scan state 都指向真实 dev 工位路径；test 工位补建、完整初始化与二次重跑幂等能力不受影响。
