---
local_id: I-20260405-1914-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '112'
    url: https://github.com/chatterzhao/freely/issues/112
    synced_at: '2026-04-27T11:24:48Z'
  gitee:
    issue_id: IJFO8S
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8S
    synced_at: '2026-04-27T13:16:30Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:48Z'
hash: ''
created_at: '2026-04-27T11:24:48Z'
updated_at: '2026-06-21T15:21:52Z'
platform_state: closed
---

当前仓库已经把测试 lane 语义写进 `AGENTS.md`、`LAWS.md` 和 skills，并出现了 `./bin/test-lane` 的实现雏形，但这批能力还没有正式 owner 链路。

同时，已暴露出几个真实执行问题：

1. `feature-local` 只阻止 protected branches，却允许任意 ad hoc writable branch 冒充 dedicated feature/release/hotfix/premerge test lane。
2. `./bin/test-lane` / `./bin/test-test-lane` 入口不可直接执行。
3. 仍有参考文档继续保留旧 replay-only promote 语义。

这说明当前问题已经是独立的 lane-routing/enforcement surface，而不是 promote-gate owner 的附带实现。

canonical: docs/epics/workspace-routing-foundation/test-lane-routing-and-enforcement-governance/issues/test-lane-routing-and-enforcement-governance.md
