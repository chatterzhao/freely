# Brainstorms

## Discovery

- **来源**: GitHub issue #501 (`raw-20260517T082350Z`), chat-inbox, P2
- **原始描述**: supervisor crash: bash at freely:18777 (rc=0)
- **last_exit_reason_before_crash**: `set_e_exit_cmd=bash@freely:18777_rc_0`
- **工具/模式**: `cc-ds-flash-auto` (Claude Code deepseek flash, auto mode)
- **适配器**: acp
- **启动方式**: prompt

## Research

### 与现有工作的关系

本 issue 与以下已物料化的 issue 描述完全一致（supervisor 将 bash rc=0 误报为 crash）：

| Issue | GitHub # | 时间 | 状态 |
|-------|----------|------|------|
| `raw-20260517T082350Z` | #501 | 08:23:50Z | 本 issue |
| `raw-20260517T082422Z` | #502 | 08:24:22Z | 已吸收 → C-20260517T083030Z-A |
| `raw-20260517T083030Z` | #504 | 08:30:30Z | C-20260517T083030Z-A (needs_research) |
| `raw-20260517T083200Z` | #505 | 08:32:00Z | C-20260517T083200Z-A (needs_research) |

- `C-20260517T083030Z-A` (`docs/pre-brainstorms/20260517T083030Z--supervisor-bash-rc0-crash/`) 已完整分析此问题，判定为需研究 supervisor crash 检测逻辑
- `raw-20260517T082422Z`（GitHub #502）已按同样模式吸收到 C-20260517T083030Z-A

### 关键确认点

- 本 issue 与 raw-20260517T082422Z 仅有秒级时间差（08:23:50Z vs 08:24:22Z），显然是同一次事件的多次上报
- 两者的 error payload 完全一致：`bash@freely:18777_rc_0`
- 工具、适配器、问题模式均相同

## Decision

- **判定**: 已存在覆盖此问题的 pre-brainstorms 和 candidate，直接吸收到 C-20260517T083030Z-A
- **吸收理由**: raw-20260517T082350Z (GitHub #501) 与已有 coverage 完全重叠，是同一 supervisor crash 假阳性事件的不同上报
- **下一跳**: 无需独立处理，关注 C-20260517T083030Z-A 的研究进展即可
