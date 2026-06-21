---
local_id: I-20260405-1215-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '106'
    url: https://github.com/chatterzhao/freely/issues/106
    synced_at: '2026-04-27T11:24:14Z'
  gitee:
    issue_id: IJFO8L
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8L
    synced_at: '2026-04-27T13:16:20Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:24:14Z'
hash: ''
created_at: '2026-04-27T11:24:14Z'
updated_at: '2026-06-21T15:21:48Z'
platform_state: closed
---

Freely 现在能把 runtime signal 暴露到 Tauri/frontend，但还没有一条稳定的自治声音能力链路。

当前缺口不是“系统怎么播声音”本身，而是 runtime 还没有把以下事实冻结成独立 contract：

- 哪些事件值得提醒
- manager 与 worker 如何区分
- started 与 completed 如何区分
- 原生 tool notice 与 fallback evidence adapter 未来如何在同一平面汇合

因此这条 owner 的职责是冻结标准路径与 sound semantics，而不是把 watchdog 继续做胖。

canonical: docs/epics/workspace-routing-foundation/runtime-audio-notifier-and-sound-semantics-governance/issues/runtime-audio-notifier-and-sound-semantics-governance.md
