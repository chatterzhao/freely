---
name: doc-pre-brainstorm-execution
description: 执行 pre-brainstorm 前置收敛环，负责把新问题收敛为 candidate，并与 milestone 保持原子同步。
---

# skill:doc-pre-brainstorm-execution

## 职责

- 接收原始发现源或仍未稳定的 candidate。
- 在合适的 dedicated worktree 中产出 `brainstorms.md` 与 `candidates.md`。
- 把 candidate 原子同步进 `docs/milestones.md`。
- 明确下一跳是继续 pre-brainstorm，还是进入 `doc-ibm-execution`。

## 不负责

- 不直接产出正式 issue-bound `IBM` 文档。
- 不直接实现代码、测试或主回写 progress。

## 进入前检查

1. 如果当前轮只读分析，可先在当前上下文判断。
2. 如果当前轮要写入 pre-brainstorm 产物：
   - 当前若已在承担该问题上下文的 dedicated worktree，可直接继续。
   - 当前若位于 `main/develop/pre-test-merge` 或主 worktree，先创建/进入 dedicated feature worktree，再写 `brainstorms.md` / `candidates.md`。
3. 如果当前问题明确依赖未合并父分支改动，优先在该父分支上下文或其派生 worktree 中继续 pre-brainstorm，避免在错误基线上收敛。

## 情景步骤

### 情景 A：新问题首次进入 pre-brainstorm

这样做：
1. 读取传入的 `source_input` 与证据。
2. 先确认当前 worktree 合适：
   - 当前 worktree 已承载该问题上下文 -> 继续
   - 当前不适合写入 -> 先创建或进入 dedicated worktree
3. 创建或进入对应的 `docs/pre-brainstorms/<id>/`。
4. 在 `brainstorms.md` 记录：
   - 来源
   - 当前为什么不能直接进入 IBM / dev
   - 当前问题边界
   - 推荐下一跳
5. 在 `candidates.md` 记录 candidate：
   - `title`
   - `status`
   - `decision_reason`
   - `promoted_issue_path`
   - `milestone`
   - `session_refs`
   - 其中 `session_refs` 采用 `tool/session_id/jsonl_path/role` 的最小结构；若 jsonl 路径不可见，使用 `unavailable://<reason>`
6. 原子更新 `docs/milestones.md`：
   - 建立 candidate 映射
   - 放入 `candidate_issues`
   - 给出下一动作

### 情景 B：里程碑中的 `candidate_issues` 仍需继续研究

这样做：
1. 打开对应 `brainstorms.md` 与 `candidates.md`。
2. 先确认继续研究应发生在哪个 worktree：
   - 独立问题 -> 可基于 `develop` 的 dedicated feature worktree
   - 依赖未合并父分支 -> 应在父分支上下文或派生 worktree 中继续
3. 补充：
   - 仍然不清楚的边界
   - 是否依赖父 issue / 父分支
   - 是否需要派生 worktree
4. 若发现该 candidate 最终将依赖未合并父分支：
   - 在 `candidates.md` 中补充 `execution_base` / `integration_target` / `depends_on`
5. 同步更新 milestone 的下一动作。

### 情景 C：研究结束，可晋升到 IBM

这样做：
1. 确认 candidate 已具备进入 issue-bound IBM 的条件。
2. 把 `candidates.md` 的 `status` 更新为 `promoted`。
3. 确保 `milestone` 不再停留在 `pending://milestone-binding`。
4. 如果当前已确定 issue 归属，立刻回填 `promoted_issue_path`，不要让 promoted 长期停留在 `pending://issue-materialization`。
5. 返回：
   - `status=completed`
   - `next_recommended_route=doc-ibm-execution`
   - 最小 issue 上下文摘要

## 回流输出

- `status`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`
- `execution_base`
- `integration_target`
- `depends_on`

## 完成判定

- `brainstorms.md` 与 `candidates.md` 已更新。
- candidate 已同步到 milestone。
- 已明确它继续 pre-brainstorm，还是进入 IBM。
