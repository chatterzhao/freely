---
local_id: I-20260401-0840-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260401-0840/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '76'
    url: https://github.com/chatterzhao/freely/issues/76
    synced_at: '2026-04-27T11:21:42Z'
  gitee:
    issue_id: IJFO7G
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7G
    synced_at: '2026-04-27T13:15:31Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:42Z'
hash: ''
created_at: '2026-04-27T11:21:42Z'
updated_at: '2026-05-17T12:21:27Z'
platform_state: closed
---

Freely 最早的 availability-manager 研究和 `20260331-1840` brainstorm 都要求同一条恢复状态机：

- 先做当前工具内部的 slot / profile family 恢复
- 当前工具 exhausted 后，再按项目定义的工具顺序尝试下一个工具
- 所有工具都不可用时，保持 no-launch，并把最早恢复提示写成显式控制面真相

后来物化时把这条 contract 收窄成了 `kiro-cli -> codex` bridge。当前 owner 要把它抬回原始设计，但保留 Codex watchdog 的 probe-first / shared-lock / no-launch invariants。

canonical: docs/B2-docs/ibm/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md
