---
b1_id: B1-20260715T063959Z
phase_state: completed
source_raw: raw-20260715T063959Z
created_at: 2026-07-15
---

# B1: AI_MODE 默认值回退 auto

## Input
- raw-20260715T063959Z: aimode-hotfix2 错误将 AI_MODE 默认从 auto 改为 wait

## Problem

### 概念混淆：task_mode ≠ AI_MODE

| 变量 | 语义 | 有效值 | 正确默认 |
|------|------|--------|---------|
| `task_mode` | daemon 运行模式 | auto, wait, listen, id:<scan-id> | **wait** |
| `AI_MODE` | Claude AI 交互姿态 | auto, step | **auto** |

`AI_MODE` 传给 `start-lead-agent.sh --mode` 参数，该脚本 line 213 校验：
```bash
[[ "$mode" == "auto" || "$mode" == "step" ]] || { echo "[ERROR] unsupported mode: $mode"; exit 1; }
```

aimode-hotfix2 (PR #3898) 将 6 处 `${AI_MODE:-auto}` 改为 `${AI_MODE:-wait}`。`--mode wait` 被拒绝，导致每次 AI launch 报 `unsupported mode: wait` → `tool_unproductive`。

### 实际影响

daemon-launch.log 显示：
```
[ERROR] unsupported mode: wait
[WARN] ai process exited rc=1 (session_id=unavailable)
[WARN] tool_unproductive detected
```

所有 AI cycle 都因 mode 无效而失败，supervisor 陷入重启循环。

### 验证

直接 CLI 调用 API 正常（`claude-apikey-ds-flash-auto -p "say hi"` 返回正常）。问题确认在 freely 内部。

## Decision

回退 6 处 `${AI_MODE:-wait}` → `${AI_MODE:-auto}`。保留 3 处 `${AI_MODE:-none}`（log 行不需要有效 mode 值）。

## Candidate
- candidate_id: C-20260715T063959Z-A
- status: promoted
- milestone: M-20260715T063959Z-A
