---
name: auto-loop-orchestrator
description: 编排 A:auto-loop(ADD)，从启动外部 AI CLI 工具到首跳 lead-agent、来源判定、usable issue 分流，再接入 doc-loop 或 dev-loop，并回到发现阶段。当 AI 运行自主持续交付循环时使用。
---

# skill:auto-loop-orchestrator

## 首段闭环主链
`sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> no-usable-issue-skill | has-usable-issue-skill -> doc-loop-execution | dev-loop-execution`

约束：
- Freely 当前编排的是外部 AI CLI 工具，而不是自研 AI CLI runtime。
- `lead-agent` 是角色定义，建议落点：`docs/system/workspace/agents/lead-agent.md`。
- `context-source-skill`、`no-usable-issue-skill`、`has-usable-issue-skill` 是 skills。
- skill 名称表达职责，不用 loop 前缀表达归属。

## 工作流
1. 先执行固定前置门禁：`skill:constitution-guard` -> `skill:laws-enforcer`。
2. `sh/ps1` 启动外部 AI CLI 工具，并进入 `lead-agent`。
3. `lead-agent` 调用 `skill:context-source-skill`，基于当前来源与上下文做 usable issue 判定。
4. 根据 `context-source-skill` 的结果分流：
   - 无 usable issue -> `skill:no-usable-issue-skill`
   - 有 usable issue -> `skill:has-usable-issue-skill`
5. `skill:no-usable-issue-skill` 继续停留 `pre-brainstorms`，产出 `brainstorms.md` / `candidates.md` 并同步 milestone。
6. `skill:has-usable-issue-skill` 再决定接入：
   - `skill:doc-loop-execution`
   - `skill:dev-loop-execution`
7. 更新候选项 / milestone / route 状态记录。
8. 重复循环直到停止条件。

## pre-brainstorms 触发
当任一条件成立时，经 `context-source-skill` 判定后进入 `no-usable-issue-skill`：
- 问题来源已发现，但 `epic/story/milestone` 尚未收敛。
- 验收边界不清，无法直接进入 `dev-loop`。
- 需要跨工具或子代理进行分歧收敛。

最小产物：
- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- 会话证据（jsonl）在 `candidates.md` 的 `session_refs` 留痕。

## 完成
- 发现、路由和闭环状态保持可追溯。
