---
name: auto-loop-orchestrator
description: 编排 A:auto-loop(ADD)，从启动外部 AI CLI 工具到首跳 lead-agent、上下文判定，再接入 pre-brainstorm/doc-loop/dev-loop，并回到发现阶段。当 AI 运行自主持续交付循环时使用。
---

# skill:auto-loop-orchestrator

## 首段闭环主链
`sh/ps1 -> external AI CLI tool -> lead-agent -> context-source-skill -> doc-pre-brainstorm-execution | doc-ibm-execution | dev-loop-execution`

约束：
- Freely 当前编排的是外部 AI CLI 工具，而不是自研 AI CLI runtime。
- `lead-agent` 是角色定义，建议落点：`docs/system/workspace/agents/lead-agent.md`。
- `context-source-skill`、`doc-pre-brainstorm-execution`、`doc-ibm-execution`、`dev-loop-execution` 是 skills。
- skill 名称表达职责，不用 loop 前缀表达归属。
- `docs/system/workspace/` 是能力真源；`bin/`、`.githooks/` 等是运行时落点。
- `sh` / `ps1` 的定义源应位于 `docs/system/workspace/scripts/`。
- hook 的定义源应位于 `docs/system/workspace/hooks/`，根目录 `.githooks/` 作为安装产物。

## 工作流
1. 先执行固定前置门禁：`skill:constitution-guard` -> `skill:laws-enforcer`。
2. `system/workspace/scripts` 中定义的 `sh` / `ps1` 启动外部 AI CLI 工具，并进入 `lead-agent`。
3. `lead-agent` 调用 `skill:context-source-skill`，基于当前来源、milestone、工具清单与上下文做 usable issue 判定，并组装下一跳提示词。
4. 根据 `context-source-skill` 的结果分流：
   - 无稳定 issue 边界 -> `skill:doc-pre-brainstorm-execution`
   - issue-bound brainstorm / mapping / governance -> `skill:doc-ibm-execution`
   - ready issue / in-progress -> `skill:dev-loop-execution`
5. 各 loop skill 在环内完成自己的工作，并把状态、阻塞、完成或恢复上下文回流给 `auto-loop`。
6. `system/workspace/hooks` 中定义的 hook 规则按安装流程投影到根目录 `.githooks/` 运行时位置。
7. 更新候选项 / milestone / issue / progress / route 状态记录。
8. 重复循环直到停止条件。

## pre-brainstorms 触发
当任一条件成立时，经 `context-source-skill` 判定后进入 `doc-pre-brainstorm-execution`：
- 问题来源已发现，但 `epic/story/milestone` 尚未收敛。
- 验收边界不清，无法直接进入 `dev-loop`。
- 需要跨工具或子代理进行分歧收敛。

最小产物：
- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- 会话证据（jsonl）在 `candidates.md` 的 `session_refs` 留痕。

## 完成
- 发现、路由和闭环状态保持可追溯。
