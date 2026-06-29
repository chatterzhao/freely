---
local_id: I-20260413-0208-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-05-19T23:20:00Z'
platform_ids:
  github:
    issue_id: '143'
    url: https://github.com/chatterzhao/freely/issues/143
    synced_at: '2026-04-27T11:27:07Z'
  gitee:
    issue_id: IJFO9U
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9U
    synced_at: '2026-04-27T13:17:13Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:27:07Z'
hash: ''
created_at: '2026-04-27T11:27:07Z'
updated_at: '2026-06-29T13:38:57Z'
platform_state: closed
---

Freely 当前的产品心智与运行时入口 contract 仍存在一条会误导用户和未来 UI 接口的错位：

1. `freely start` 实际是前台附着 supervisor，会跟随调用会话结束而停机
2. 产品 intent 又要求 runtime 持续运行，除非明确停止
3. 现有测试已经把 `start/restart/stop/status` 锁成前台/控制面 contract，不能静默改成后台
4. 若不先冻结 foreground/background/UI close/state truth 的边界，后续实现极易把入口语义变更、daemon 引入、恢复链回归混成一次高风险改动

canonical: docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md
