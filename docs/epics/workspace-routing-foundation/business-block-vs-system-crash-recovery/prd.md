# PRD: business-block-vs-system-crash-recovery

## Goal

让 Freely 明确区分业务阻塞与系统崩溃，并在系统崩溃后可靠恢复到正确 issue / worktree / AI 会话上下文。

## Requirements

1. `blocked_*` 只表示 AI 已识别并显式留痕的业务阻塞。
2. PID 消失、CLI 崩溃、会话断裂等系统事件，不直接改 `phase_state`。
3. 恢复定位顺序固定为 `recovery -> progress -> issue -> milestone -> active worktree/uncommitted changes`。
4. 恢复最小字段包含 `tool/session_id/jsonl_path/branch/worktree_path/phase_state/runtime_state/resume_hint`。
5. auto-loop 与 recovery skills 必须根据这些字段选择正确的 attach/resume/restart 路径。
