---
local_id: I-20260405-2055-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '113'
    url: https://github.com/chatterzhao/freely/issues/113
    synced_at: '2026-04-27T11:25:05Z'
  gitee:
    issue_id: IJFO8T
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8T
    synced_at: '2026-04-27T13:16:32Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:05Z'
hash: ''
created_at: '2026-04-27T11:25:05Z'
updated_at: '2026-06-21T15:21:54Z'
platform_state: closed
---

Freely 已经为 `freely start` 冻结了 shared codex slot-switch lock 的 startup preflight，也已经为 project command family 冻结了 `restart` 的语义层级；但两者之间仍留了一个真实缺口：当 restart 将要被 active shared lock 阻塞时，当前 project runtime 仍可能先被停掉，再发现下一次启动无法前进。对于 dogfood 中的真实运行项目，这个顺序错误会把“有界失败”升级成“可避免的 runtime 中断”。

canonical: docs/epics/workspace-routing-foundation/restart-slot-switch-preflight-preserves-active-runtime-governance/issues/restart-slot-switch-preflight-preserves-active-runtime-governance.md
