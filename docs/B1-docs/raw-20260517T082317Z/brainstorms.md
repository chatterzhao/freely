# Brainstorms

## Discovery

- **来源**: GitHub issue #500 (`raw-20260517T082317Z`), chat-inbox, P2
- **原始描述**: supervisor crash: bash at freely:18777 (rc=0)
- **last_exit_reason_before_crash**: `set_e_exit_cmd=bash@freely:18777_rc_0`
- **工具/模式**: `cc-ds-flash-auto` (Claude Code deepseek flash, auto mode)
- **适配器**: acp
- **启动方式**: prompt

### 时效性与覆盖检查

同一 supervisor bash rc=0 crash 事件已有多个独立 raw issue 和 pre-brainstorm：

| raw issue | GitHub # | 时间 | 状态 |
|-----------|----------|------|------|
| `raw-20260517T082317Z` | #500 | 08:23:17Z | **本 issue（最早）** |
| `raw-20260517T082350Z` | #501 | 08:23:50Z | absorbed → C-20260517T083030Z-A |
| `raw-20260517T082422Z` | #502 | 08:24:22Z | absorbed → C-20260517T083030Z-A |
| `raw-20260517T082453Z` | #503 | 08:24:53Z | needs_research (C-20260517T082453Z-A) |
| `raw-20260517T083030Z` | #504 | 08:30:30Z | needs_research (C-20260517T083030Z-A) |
| `raw-20260517T083200Z` | #505 | 08:32:00Z | needs_research (C-20260517T083200Z-A) |

所有实例的 error payload 完全一致：`bash@freely:18777_rc_0`，工具/适配器/问题模式均相同。

## Research

本 raw issue 与 raw-20260517T082350Z 仅有秒级时间差（08:23:17Z vs 08:23:50Z），显然是同一次 supervisor crash 假阳性事件由不同监控路径上报的多个副本。

- 已有 `C-20260517T083030Z-A` (`docs/pre-brainstorms/20260517T083030Z--supervisor-bash-rc0-crash/`) 完整分析了此问题：supervisor 将 bash rc=0（正常退出）误判为 crash
- raw-20260517T082350Z (GitHub #501) 和 raw-20260517T082422Z (GitHub #502) 已按同样模式吸收到 C-20260517T083030Z-A

## Decision

- **判定**: 已有完整覆盖此问题的 pre-brainstorms 和 candidate，直接吸收到 C-20260517T083030Z-A
- **吸收理由**: raw-20260517T082317Z (GitHub #500) 与已有 coverage 完全重叠，是同一 supervisor crash 假阳性事件的最早上报实例
- **下一跳**: 无需独立处理，关注 C-20260517T083030Z-A 的研究进展即可
