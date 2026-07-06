---
local_id: I-20260327-0651
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260327-0651/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '60'
    url: https://github.com/chatterzhao/freely/issues/60
    synced_at: '2026-04-27T11:17:52Z'
  gitee:
    issue_id: IJFO6V
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6V
    synced_at: '2026-04-27T13:15:05Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:52Z'
hash: ''
created_at: '2026-04-27T11:17:52Z'
updated_at: '2026-04-27T11:17:52Z'
platform_state: closed
---

Freely runtime 里和代理有关的默认值目前仍然分散在脚本内部，典型问题是把 localhost 代理写死成运行时 fallback。这样会造成三个直接后果：

1. codex exec、curl/OAuth、watchdog 和 launcher 不能共享同一份 proxy truth。
2. 后续前端如果只改 project config，也无法把所有调用面一起带起来。
3. 代理行为被藏进代码默认值后，任何真实环境下的网络出口变化都会被测试假象掩盖。

这条 issue 的目标是把 proxy 变成 Freely 的项目级能力，而不是散落在 runtime shell 里的隐式假设。

canonical: docs/B2-docs/ibm/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance/issues/project-scoped-network-proxy-configuration-and-launcher-inheritance-governance.md
