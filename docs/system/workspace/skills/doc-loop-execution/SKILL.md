---
name: doc-loop-execution
description: 在法律和宪法下执行 D:doc-loop(IBM) 工作流。当 AI 需要接收 issue、产出 brainstorm/map 产物、并保持里程碑和路由文档一致时使用。
---

# skill:doc-loop-execution

## 工作流
1. 接收 issue 并对齐 epic/story/milestone 所有权。
2. 产出或更新 brainstorm 和 mapping 产物。
3. 在 map 阶段，开发开始前定义 `PRE_TEST` 基线（包括集成验收标准）。
4. 按要求更新 pre-brainstorms 候选项路由/状态。
5. 原子化同步里程碑和 issue 映射。
6. 如需变更规范文档，确保在专用 `feature/*` 分支 + worktree 中工作，并存在关联实现/门禁变更。
7. 用 `skill:laws-enforcer` 验证。

## 完成
- 必需的 doc-loop 产物完整，路由/状态一致。
