---
local_id: raw-20260616T224707Z07Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '2862'
    url: https://github.com/chatterzhao/freely/issues/2862
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T22:47:23Z'
updated_at: '2026-06-16T22:47:23Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Severity: P0 (runtime-critical)

Freely 自主运行的每次 multi-turn 周期都在丢失 session context，每次创建新 session，无法利用 prompt caching，且触发 restart-storm 检测。

## 背景：三种 AI CLI 的 Session ID 格式

| AI CLI | Session ID 格式 | 示例 |
|--------|----------------|------|
| Claude Code (cc) | UUID v4 | `a1b2c3d4-e5f6-...` |
| Codex CLI | UUID v4 | `a1b2c3d4-e5f6-...` |
| OpenCode | `ses_` prefix | `ses_12ef4d6cfffeWnAyWb17Uc2RdX` |

当前代码在 Claude Code → OpenCode 迁移后，多处 session ID 提取逻辑仍假设 UUID v4 格式。

## Root Cause: 三个交互 Bug

### Bug 1: `run-acp-prompt.py:447-451` — prompt 分支缺少 clean UUID 输出行

```python
elif launch_kind == "prompt" and resume_target:
    session_id = resume_target
    print(f"session id: {session_id} (prompt)", flush=True)  # 只有一行！缺少 clean line 1
    session_result = {"sessionId": session_id}
```

所有其他分支 (fresh/resume/fork) 都输出**两行**（line 1: clean ID, line 2: human label），唯独 `prompt` 分支只输出一行带 label 的。

**修复**: 在 label 行之前添加 `print(session_id, flush=True)`，与其他分支对齐。

### Bug 2: `monitor-ai-acp.sh:430,441` — Session ID 提取 regex 只匹配 UUID v4

```bash
# 主提取 (line 430): 只匹配 UUID v4
session_id_clean=$(grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}' "$log_file" | head -1)

# 备用清洗 (line 441): 同样只匹配 UUID v4
_fallback_sid=$(echo "$session_id_out" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}' | head -1)
```

OpenCode 的 `ses_` 格式永远不会匹配。`session-cache.sh:157` **已有**正确实现：
```bash
sed -n 's/.*service=session id=\(ses_[A-Za-z0-9_]*\).*/\1/p' "$log_file"
```
但 `monitor-ai-acp.sh` 未复用此逻辑。

**修复**: 通用化 session ID 提取，同时兼容 UUID v4、`ses_` 和 `session id: <id>` 三种输出格式。建议方案：从 `session_id_out` 中主动 strip 已知 label 后缀 `(prompt)`、`(fresh after prompt failure)`、`(fresh after resume failure)`、`(resumed)`、`(fork)`、`(fork from ...)`，而非仅依赖正向 regex 匹配。

### Bug 3: `freely:3622-3625,3743,3763` — `is_valid_uuid()` 阻断 OpenCode session 恢复

```bash
is_valid_uuid() {
  [[ "$value" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$ ]]
}
```

`ensure_runtime_tool_session_anchor` 尝试从 session-store (SQLite) 恢复 session ID 时，`is_valid_uuid` 拒绝 `ses_` 格式 → 恢复路径被阻断 → 生成全新 UUID 而非使用真实 session ID。

`session-store` (SQLite via `freely-db-cli`) 本身已正确支持 `ses_` 格式的存储和查询。问题仅在 `freely` 脚本的读取侧验证过于严格。

**修复**: 将 `is_valid_uuid` 替换/扩展为 `is_valid_session_id`，同时接受 UUID v4 和 `ses_[A-Za-z0-9_]+` 两种格式。

## Contamination Chain（完整故障链）

```
Cycle N (multi-turn prompt, opencode):
  run-acp-prompt.py: 只输出 "session id: ses_AAA (prompt)" 一行
  monitor-ai-acp.sh: UUID regex 无法解析 ses_ → session_id_clean = "ses_AAA (prompt)" [污染!]
  monitor-ai-acp.sh: 写入 session-store 的 ID 带 "(prompt)" label

Cycle N+1:
  freely: 从 session-store 读取 → "ses_AAA (prompt)" [污染!]
  freely: 传给 monitor-ai-acp.sh --tool-resume-target "ses_AAA (prompt)"
  run-acp-prompt.py: session_id = resume_target = "ses_AAA (prompt)" [污染!]
  run-acp-prompt.py: session/prompt with "ses_AAA (prompt)" → OpenCode 拒绝
  run-acp-prompt.py: session/resume → OpenCode Internal error
  run-acp-prompt.py: session/new → 新 session "ses_BBB"
  run-acp-prompt.py: 输出 "session id: ses_BBB (fresh after prompt failure)"
  monitor-ai-acp.sh: UUID regex 再次失败 → 存储 "ses_BBB (fresh after prompt failure)" [再次污染!]

Cycle N+2+: 无限循环，每次创建全新 session，cache 命中率=0%
```

## Evidence（观测到的运行时证据）

### Cycle Log Timeline (2026-06-16 UTC)

| Cycle | Session ID (stored) | Contaminated? | Result |
|-------|--------------------|---------------|--------|
| 082601 | `ses_12ef4d6cfffeWnAyWb17Uc2RdX` | Clean (fresh) | OK |
| 083315 | `ses_12ef4d6cfffeWnAyWb17Uc2RdX (prompt)` | YES | 本次可用(Python 内部用 clean args.resume)，但存储已污染 |
| 084212 | fallback 到 `ses_12ee5dc13ffeLGr8slXqFoa3Jg (fresh after prompt failure)` | YES | prompt/resume 均失败，降级到 session/new |
| 084748 | 再次降级到 `ses_12ee0c26cffe...` | YES | 同上模式 |

### 并发症状
- **restart-storm-window.tsv**: `1781624858	3` — 3 次快速重启 (2026-06-16T15:47:38Z)
- **bridge-lost.marker**: `bridge_session_lost` — bridge 在 15:55:08Z 死亡
- **preemption-state.env**: preemption reason=`local_continuation_reentry`, intake=`runtime-stalled-ai-recovery`
- **session-state.env**: `LAST_ROTATION_REASON="acp_multi_turn"`, `CLAUDE_SESSION_ID_CURRENT` 含污染 label
- **cycle-20260616-084212.log line 1**: `session id: ses_12ef4d6cfffeWnAyWb17Uc2RdX (prompt) (prompt)` — **双重 label，确认污染传播**

## Acceptance Criteria
- [ ] `run-acp-prompt.py` 所有 launch_kind 分支输出统一的 clean line 1 + label line 2（含 prompt 分支修复）
- [ ] `monitor-ai-acp.sh` session ID 提取兼容 UUID v4、`ses_`、`session id: <id>` 三种格式
- [ ] `monitor-ai-acp.sh` 的 label stripping 逻辑覆盖所有已知 label 后缀
- [ ] `freely` 的 `is_valid_uuid()` 替换为 `is_valid_session_id()`，同时接受 UUID v4 和 `ses_` 格式
- [ ] `monitor-ai-acp.sh` 的 session ID 提取复用或对齐 `session-cache.sh` 的工具感知逻辑
- [ ] 连续 3 次 `LAUNCH_KIND="prompt"` multi-turn cycle 后 session ID 保持 clean（无 label 残留）
- [ ] restart-storm 检测不再因 session ID 污染而误触发
- [ ] 三种 AI CLI (Claude Code / Codex CLI / OpenCode) 的 session 生命周期回归测试通过
- [ ] 切换到 cc 或 codex 工具后，session ID 提取同样正常（UUID v4 路径不受影响）

## Affected Files
1. `docs/system/workspace/scripts/runtime/run-acp-prompt.py:447-451` — prompt 分支缺少 clean 输出行
2. `docs/system/workspace/scripts/runtime/monitor-ai-acp.sh:430,441` — UUID-only regex
3. `docs/system/workspace/scripts/runtime/freely:3622-3625,3743,3763` — is_valid_uuid 拒绝 ses_ 格式
4. `docs/system/workspace/scripts/runtime/session-cache.sh:157` — 已有正确 ses_ regex（参考实现）

## Related
- `session-cache.sh` 已在 `session_extract_id_from_log` 中按工具类型分派不同的 ID 提取策略 → `monitor-ai-acp.sh` 和 `freely` 需对齐
- 此 Bug 在 opencode 从 cc 切换后被激活（Claude Code 使用 UUID v4 → 原代码在其下正常工作，切换到 opencode 后暴露）
