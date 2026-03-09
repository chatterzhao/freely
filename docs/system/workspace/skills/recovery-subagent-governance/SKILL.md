---
name: recovery-subagent-governance
description: 强制恢复耦合和子代理治理约束。当 AI 委托任务、恢复中断工作、或需要保持分支/worktree 上下文和所有权边界时使用。
---

# skill:recovery-subagent-governance

## 工作流
1. 记录活跃分支/worktree/会话上下文。
2. 委托时，定义所有权边界和预期输出。
3. 跟踪子代理完成/失败和合并影响。
4. 恢复时，先判断这是业务阻塞还是系统崩溃：
   - 业务阻塞：沿用已有 `blocked_*` 与 issue/progress 留痕
   - 系统崩溃：不得直接写 `blocked_*`，先做恢复定位
5. 系统崩溃的恢复定位顺序固定为：
   - `docs/recovery/**`
   - `docs/progress/**`
   - `issue`
   - `docs/milestones.md`
   - 当前活跃 worktree 与未提交改动
6. 恢复前必须确认 `tool/session_id/jsonl_path` 是否可追溯；若 jsonl 路径不可见，至少保留显式 `unavailable://<reason>`。
7. 若已知 `tool` 与 `session_id`，优先使用对应工具的 resume/attach 能力；若不能 resume，再按桥接恢复重启。
8. 需要恢复路径示例时读取 [recovery-examples.md](references/recovery-examples.md)。
9. 如上下文所有权模糊则阻止继续。

## 完成
- 恢复和委托状态完整且可审计。
