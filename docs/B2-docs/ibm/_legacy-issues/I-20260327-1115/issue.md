---
local_id: I-20260327-1115
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '62'
    url: https://github.com/chatterzhao/freely/issues/62
    synced_at: '2026-04-27T11:18:05Z'
  gitee:
    issue_id: IJFO6Y
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6Y
    synced_at: '2026-04-27T13:15:08Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:18:05Z'
hash: ''
created_at: '2026-04-27T11:18:05Z'
updated_at: '2026-04-27T11:18:05Z'
platform_state: closed
---

`I-20260318-1630` 已完成的 canonical contract 建立了：

- failure-driven slot sweep
- no-launch gate
- all-unavailable hold
- slot-first identity

但它同时也把“真实 probe 才是 inventory truth、cooldown 不参与恢复逻辑”冻结成已完成边界。

本轮新证据已经证明，OpenAI 的 `wham/usage` OAuth query 能直接基于 `.ai-auth/codex-*/auth.json` 中的 token 并行扫描 slot inventory：

- 不消耗 token
- 不需要复制授权文件到 `~/.codex/auth.json`
- 能在约 3.7 秒内扫完本机 25 个 slot
- 不只返回 quota，还能直接暴露 `deactivated_workspace`

这不是给旧 watchdog issue 加一条 supporting evidence，而是要把 inventory truth / co

canonical: docs/B2-docs/ibm/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance/issues/oauth-slot-inventory-sweep-and-launch-time-confirmation-governance.md
