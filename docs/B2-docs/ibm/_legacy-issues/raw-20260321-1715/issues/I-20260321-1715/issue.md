---
local_id: I-20260321-1715
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260321-1715/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '38'
    url: https://github.com/chatterzhao/freely/issues/38
    synced_at: '2026-04-27T11:15:42Z'
  gitee:
    issue_id: IJFO60
    url: https://gitee.com/zhaoquan/freely/issues/IJFO60
    synced_at: '2026-04-27T13:14:34Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:42Z'
hash: ''
created_at: '2026-04-27T11:15:42Z'
updated_at: '2026-04-27T11:15:42Z'
platform_state: closed
---

Freely 当前已经分别定义了：

- `event source / standing source`
- 主管巡检与委派
- restart point routing
- `external drift / out-of-band reconcile` 的新研究结论

但这些语义还散落在多个真源里，且容易被误读成：

- `auto-loop` 只有周期巡检，没有事件触发入口
- verification / writeback / cleanup 是第四层 loop
- 主管只在最前面路由一次
- 主管既判断又亲自施工

需要一条新的治理 issue，把这些新增澄清收敛成一致的应用产物重构：

- 不回写历史 issue
- 不新造平行 skill
- 在当前新生命周期内统一重构 `three-loop` / `manager-agent` / `auto-loop-orchestrator` / patrol reference

canonical: docs/B2-docs/ibm/manager-watchdog-trigger-and-drift-reconcile-governance/issues/manager-watchdog-trigger-and-drift-reconcile-governance.md
