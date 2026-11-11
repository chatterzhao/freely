---
name: freely-recovery-subagent-governance
description: >-
  强制恢复耦合和子代理治理约束。确保 AI 委托任务、恢复中断工作时
  保持分支/worktree 上下文和所有权边界。

  Use when: AI 恢复中断工作、委托子任务、或需要保持上下文所有权。
  触发词："恢复"、"recovery"、"subagent"、"委托"、"上下文所有权"。
loop: runtime
owner: manager
supersedes: []
---

# skill:freely-recovery-subagent-governance

## 工作流
1. 记录活跃分支/worktree/会话上下文。
2. 委托时，定义所有权边界和预期输出。
3. 跟踪子代理完成/失败和合并影响。
4. 恢复时，先判断这是业务阻塞还是系统崩溃：
   - 业务阻塞：沿用已有 `blocked_*` 与 issue/progress 留痕
   - 系统崩溃：不得直接写 `blocked_*`，先做恢复定位
5. 系统崩溃的恢复定位顺序固定为：
   - `docs/recovery/**`
   - `docs/B2-docs/**`
   - `issue`
   - `docs/milestones.md`
   - 当前活跃 worktree 与未提交改动
6. 恢复前必须确认 `tool/session_id/jsonl_path` 是否可追溯；若 jsonl 路径不可见，至少保留显式 `unavailable://<reason>`。
7. 若已知 `tool` 与 `session_id`，先判断“是否还能 resume”和“是否还值得继续 resume”：
   - 仍健康：优先 resume/attach
   - 技术上可 resume，但已出现 `context compacted`、缺少最小 resume evidence、连续 resume 退化或命中本地轮换阈值：允许走 `fresh_with_handoff`
   - 已不能 resume：按桥接恢复重启
8. `fresh_with_handoff` 的最小交接面应尽量包含上一轮 `tool_session_id`、cycle log 路径、branch/worktree、触发 fresh 的原因，以及最近一段输出摘录。
9. 涉及 `context warn`、`context rotate`、`fresh_with_handoff` 的 continuity 边界时，交由 `skill:freely-continuity-watchdog` 作为优先事实源。
10. 需要恢复路径示例时读取 [recovery-examples.md](references/recovery-examples.md)。
11. 如上下文所有权模糊则阻止继续。

## 完成
- 恢复和委托状态完整且可审计。
