---
name: doc-ibm-execution
description: 在法律和宪法下执行 issue-bound docs 环，负责 `IBM+G` 产物、里程碑同步和进入 `dev-loop-execution` 前的文档收敛。
---

# skill:doc-ibm-execution

## 适用边界
- `IBM`：issue 接入、brainstorm、mapping、里程碑与路由同步。
- `G`：治理资产维护（`docs/CONSTITUTION.md`、`docs/LAWS.md`、`docs/system/workspace/skills/**`）的一致性修复与收敛。
- 本 skill 是 docs 内循环，不负责实现代码；实现进入 `dev-loop-execution`。

## 核心产物

- `docs/epics/{epic}/{story}/issues/{issue-name}.md`
- `docs/epics/{epic}/{story}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic}/{story}/prd.md`
- `docs/epics/{epic}/{story}/pre-tests.md`
- `docs/epics/{epic}/{story}/tasks.md`
- `docs/milestones.md`
- 按需更新：
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/**`

## 工作流
1. 接收 issue 并对齐 epic/story/milestone 所有权。
2. 产出或更新 issue-bound brainstorm：`brainstorms/b-{issue-name}.md`。
3. 在 map 阶段完善：
   - `prd.md`
   - `pre-tests.md`
   - `tasks.md`
4. 在开发开始前定义 `PRE_TEST` 基线，包括集成验收标准与最小证据要求。
5. 若当前 issue 来源于 pre-brainstorm candidate：
   - 更新 `candidates.md` 的 `promoted_issue_path`
   - 更新 candidate 状态与 route/status 记录
6. 原子化同步 `docs/milestones.md` 与 issue 映射、状态和下一动作。
7. 若存在治理漂移（术语、路由、证据口径、门禁语义不一致），触发 `G` 轨维护并更新对应治理资产。
8. 治理资产变更必须在专用 `feature/*` 分支 + worktree 中进行，并绑定关联实现或门禁变更证据。
9. 用 `skill:laws-enforcer` 验证。
10. 若 issue 已具备实现条件，明确向 `auto-loop` 返回“可进入 dev-loop”的状态与最小上下文。

## 状态交换

- 向 `auto-loop` 回流的最小结果应包括：
  - issue 是否已完成接入与落位
  - `PRE_TEST` 是否已建立
  - milestone 是否已同步
  - 是否已具备进入 `dev-loop-execution` 的条件
  - 若阻塞，阻塞原因与下一动作

## 完成
- 必需的 doc-loop 产物完整，且 `IBM` 与 `G` 两轨在当前 issue 范围内保持一致可追溯。
