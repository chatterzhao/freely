---
name: auto-loop-orchestrator
description: 编排 A:auto-loop(ADD)，从 issue 发现到路由到 doc-loop 或 dev-loop，再回到发现阶段。当 AI 运行自主持续交付循环时使用。
---

# skill:auto-loop-orchestrator

## 工作流
1. 从配置来源发现候选项。
2. 根据就绪状态路由候选项：
   - 未解决 -> `skill:doc-loop-execution`
   - 就绪/进行中 -> `skill:dev-loop-execution`
3. 更新候选项路由/状态记录。
4. 重复循环直到停止条件。

## 完成
- 发现、路由和闭环状态保持可追溯。
