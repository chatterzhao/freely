# Brainstorms

## Discovery

- **来源**: chat-inbox → `raw-20260517T082422Z` (GitHub #502)
- **摘要**: runtime supervisor 上报 bash at freely:18777 以 rc=0 退出并被判定为 crash。
- **现场信息**:
  - `tool`: cc-ds-flash-auto (Claude Code deepseek flash auto mode)
  - `adapter`: acp (ACP bridge)
  - `launch_kind`: prompt（一次性 prompt 启动）
  - `last_exit_reason_before_crash`: `set_e_exit_cmd=bash@freely:18777_rc_0`
- **核心异常**: bash 以 rc=0（正常退出）被 supervisor 上报为 crash。

### 时效性与覆盖检查

同一主题已有 3 个独立 pre-brainstorm：

| pre-brainstorm | raw issue | 时间 | GitHub |
|---|---|---|---|
| `20260517T082453Z--supervisor-bash-rc0-crash` | `raw-20260517T082453Z` | 08:24:53Z | #503 |
| `20260517T083030Z--supervisor-bash-rc0-crash` | `raw-20260517T083030Z` | 08:30:30Z | #504 |
| `20260517T083200Z--supervisor-crash-bash-rc0` | `raw-20260517T083200Z` | 08:32:00Z | #505 |

其中 `20260517T082453Z` 已有完整的发散→收敛→决策分析，定位核心问题为 **"supervisor 未区分进程正常退出 (rc=0) 和异常崩溃 (rc!=0)"**；`083030Z` 和 `083200Z` 均已进入 milestones.md 的 candidate_issues 队列，status=needs_research。

本 raw issue `raw-20260517T082422Z` 是同一主题的最早实例（GitHub #502，08:24:22Z），已被上述 brainstorms 覆盖。

**判定**: 无需重复发散收敛，吸收到已有 candidate 中。

## Research

此处复用现有分析的结论：

1. **rc=0 是强信号**：bash 以退出码 0 退出表示正常结束，不应触发 crash 处理路径。
2. **set_e_exit_cmd 标签**：来自 bash `set -e` 触发的退出溯源，但最终 shell rc 为 0 说明上层捕获处理。
3. **launch_kind=prompt**：一次性 prompt 启动，任务完成后进程退出是预期行为。
4. **可能性 A（正常退出被误分类）最可能**：supervisor 将"进程不再运行"一律视为 crash，未识别正常退出的生命周期语义。

详细分析参照 `docs/pre-brainstorms/20260517T082453Z--supervisor-bash-rc0-crash/brainstorms.md`。

## Decision

- **判定**: 本 raw issue 已被现有 pre-brainstorms 覆盖，吸收到已有 candidate `C-20260517T083030Z-A`。
- **下一跳**: 无需单独推进；现状 tracking 在 `M-20260517T083030Z-A` 下。
