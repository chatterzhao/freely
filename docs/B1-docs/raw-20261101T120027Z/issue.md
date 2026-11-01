---
schema_version: '1'
local_id: raw-20261101T120027Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261101T120027Z-A
platform_ids:
  github:
    issue_id: '4112'
    url: https://github.com/chatterzhao/freely/issues/4112
    synced_at: ''
  gitee:
    issue_id: IKS33V
    url: https://gitee.com/zhaoquan/freely/issues/IKS33V
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-01T12:00:27Z'
updated_at: '2026-11-01T12:00:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: 2026-11-01T12:00:00Z
closeout_note: P1 packaging scope absorbed into I-20261101T120027Z-A; issue→PR is a later slice.
---

workflow_kind: feature

## 背景

`@freely/dsh-freely` 是 Freely 的 DSH 打包形态，不是 Super-agent 对比研究的 candidate。

Super-agent 对比 raw 只负责底层运行时协作能力：讨论入口/事件准入、消息级 ownership/handoff、report/attention、HarnessPort。DSH 打包要独立走 B1→B2→TDD→PR，避免和 runtime 重构混在一个 PR。

当前已有 P1 spike 证据：

- `packaging/dsh-freely/`：DSH bundle plugin，Manager session + 工具白名单 + `freely_status` bridge。
- DSH web profile 真加载；Worker session 在 `/tmp/freely-e2e` 写出 DONE.txt 并 commit `fa9c06e`。
- 三角色 preset/persona/工具白名单已验。
- 仍未过：真实 issue → Manager 派工 → Worker → Reviewer → PR 的完整 E2E。

## 任务

1. B1：收敛 DSH 打包形态边界、支持的 profile/版本、服务契约、与 Freely core 的 ownership。
2. B2：物化 `packaging/dsh-freely` 的 PRD/pre-tests/tasks；P1 插件骨架、preset、bridge。
3. 完成 issue→PR E2E，过 pretests-gate。
4. 单独 PR/merge；不混入 Super-agent runtime PR。

## 非目标

- 不把 DSH Router/Ticket 当 Freely loop。
- 不做 headless/desktop、多项目、Panel（除非 B1 重新收敛）。
