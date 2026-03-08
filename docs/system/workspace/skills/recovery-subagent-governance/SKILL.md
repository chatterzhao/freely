---
name: recovery-subagent-governance
description: 强制恢复耦合和子代理治理约束。当 AI 委托任务、恢复中断工作、或需要保持分支/worktree 上下文和所有权边界时使用。
---

# skill:recovery-subagent-governance

## 工作流
1. 记录活跃分支/worktree/会话上下文。
2. 委托时，定义所有权边界和预期输出。
3. 跟踪子代理完成/失败和合并影响。
4. 恢复时，在继续执行前验证连续性产物，并确认 `tool/session_id/jsonl_path` 是否可追溯；若 jsonl 路径不可见，至少保留显式 `unavailable://<reason>`。
5. 如上下文所有权模糊则阻止继续。

## 完成
- 恢复和委托状态完整且可审计。
