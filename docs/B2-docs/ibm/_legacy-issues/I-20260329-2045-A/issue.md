---
local_id: I-20260329-2045-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '68'
    url: https://github.com/chatterzhao/freely/issues/68
    synced_at: '2026-04-27T11:21:17Z'
  gitee:
    issue_id: IJFO76
    url: https://gitee.com/zhaoquan/freely/issues/IJFO76
    synced_at: '2026-04-27T13:15:16Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/issues/ai-auth-change-wake-command-lifecycle-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:17Z'
hash: ''
created_at: '2026-04-27T11:21:17Z'
updated_at: '2026-05-17T12:21:02Z'
platform_state: closed
---

`bin/ai` 的账号成功路径当前暴露了一个独立于账号池可用性和 OAuth 成功率的命令生命周期问题：

- `ai list` / `whoami` / `status` 可以自行退出
- `ai switch codex <slot>` 在打印成功结果后仍可能不退出
- 这个问题即使在 no-op `switch codex <current-slot>` 上也成立
- 前台 `ai-cli` 存活时，其同步子进程是 `freely auth-change-wake --reason switch_success`

这说明当前缺口不是“账号不能切”，而是“成功后的 wake 语义与命令退出语义没有收口”。在 watchdog 路径也会触发 `ai switch` 的前提下，这条链还存在自激递归风险。

`ai login codex` 当前只作为同族 follow-on 风险记录。第一阶段 IBM 和修复以 `switch` 的硬复现为准，不要求执行真实登录。

canonical: docs/epics/workspace-routing-foundation/ai-auth-change-wake-command-lifecycle-governance/issues/ai-auth-change-wake-command-lifecycle-governance.md
