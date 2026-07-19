---
local_id: raw-20260718T043147Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260718T043147Z-A
platform_ids:
  github:
    issue_id: '3992'
    url: https://github.com/chatterzhao/freely/issues/3992
    synced_at: ''
  gitee:
    issue_id: IK1WUK
    url: https://gitee.com/zhaoquan/freely/issues/IK1WUK
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-18T04:32:10Z'
updated_at: '2026-07-18T04:32:10Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 根因
Worker 10 个 slot 配置 opencode-apikey-ds-flash-auto 作为 AI CLI，但所有 submitted tasks 从未被 worker 拉取执行。退出原因均为 `manager_worker_launch_verification_blocked`。

## 影响
- 23 agent_dead 工位无法恢复
- 14 merged_develop 无法 closeout
- 15 i_non_terminal 无法更新 phase_state
- 整条开发流水线停摆

## 需要排查
1. opencode CLI 进程是否能正常启动
2. ACP bridge 初始化在哪一步超时或失败
3. 门禁 verification 为什么拦截 worker launch——是 config 缺失还是 slot 权限问题

## 证据
- agent-table.toml: worker_slot=opencode-apikey-ds-flash-auto, pool=10
- A2A tasks: 大量 submitted 但从未 transitioning 到 working
- Continuity round 091: "ACP bridge worker launch — workers time out on initialize"
