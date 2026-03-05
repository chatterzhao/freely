---
name: auto-loop-orchestrator
description: 编排 A:auto-loop(ADD)，从 issue 发现到路由到 doc-loop 或 dev-loop，再回到发现阶段。当 AI 运行自主持续交付循环时使用。
---

# skill:auto-loop-orchestrator

## 预研头脑风暴触发
当任一条件成立时，先进入 `pre-brainstorms`：
- 问题来源已发现，但 `epic/story/milestone` 尚未收敛。
- 验收边界不清，无法直接进入 `dev-loop`。
- 需要跨工具或子代理进行分歧收敛。

预研阶段最小产物：
- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- 会话证据（jsonl）在 `candidates.md` 的 `session_refs` 留痕。

## 多 AI 预研提示词模板
```
你们是预研头脑风暴小组（可由主 AI + 子代理 + 其他 AI CLI 工具组成）。

目标：
1) 从输入问题中提炼候选 issue；
2) 判断是否已具备 epic/story/milestone 归属；
3) 给出 route（doc-loop 或 dev-loop）与原因；
4) 输出可写入 candidates.md 的字段草案。

硬约束：
- 不产出 chat-todo；统一产出候选 issue。
- 会话日志保留为 jsonl 证据，并回填 session_refs。
- 未收敛时必须继续停留 pre-brainstorms，不得伪造 issue-ready。
```

## 工作流
1. 从配置来源发现候选项。
2. 根据就绪状态路由候选项：
   - 未解决 -> `skill:doc-loop-execution`
   - 就绪/进行中 -> `skill:dev-loop-execution`
3. 更新候选项路由/状态记录。
4. 重复循环直到停止条件。

## 完成
- 发现、路由和闭环状态保持可追溯。
