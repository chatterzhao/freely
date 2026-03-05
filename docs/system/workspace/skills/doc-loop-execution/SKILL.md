---
name: doc-loop-execution
description: 在法律和宪法下执行 D:doc-loop(IBM+G) 工作流。当 AI 需要接收 issue、产出 brainstorm/map 产物、并维护治理资产（Constitution/Laws/Skills）一致性时使用。
---

# skill:doc-loop-execution

## 适用边界
- `IBM`：issue 接入、brainstorm、mapping、里程碑与路由同步。
- `G`：治理资产维护（`docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/system/workspace/skills/**`）的一致性修复与收敛。

## 工作流
1. 接收 issue 并对齐 epic/story/milestone 所有权。
2. 产出或更新 brainstorm 和 mapping 产物。
3. 在 map 阶段，开发开始前定义 `PRE_TEST` 基线（包括集成验收标准）。
4. 按要求更新 pre-brainstorms 候选项路由/状态。
5. 原子化同步里程碑和 issue 映射。
6. 若存在治理漂移（术语、路由、证据口径、门禁语义不一致），触发 `G` 轨维护并更新对应治理资产。
7. 治理资产变更必须在专用 `feature/*` 分支 + worktree 中进行，并绑定关联实现或门禁变更证据。
8. 用 `skill:laws-enforcer` 验证。

## 完成
- 必需的 doc-loop 产物完整，且 `IBM` 与 `G` 两轨在当前 issue 范围内保持一致可追溯。
