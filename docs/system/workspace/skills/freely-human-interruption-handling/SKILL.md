---
name: freely-human-interruption-handling
description: >- 处理 human interruption intake。接收 manager 已 claim 的插话，结合
  项目上下文做深度解释，产出 resolution artifact 和 absorption 建议。

  Use when: `freely-human-interruption-manager-triage` skill 委派后。
  触发词："interruption handling"、"处理插话"、"深度解释"。
---

# skill:freely-human-interruption-handling

## 职责

- 读取 raw interruption intake 与当前项目上下文。
- 在 manager 已选 reaction mode 的前提下，解释这条插话真正想改变什么。
- 产出 `interruption resolution artifact`。
- 为下游 worker 或 runtime 生成最小 handoff。
- 明确建议的 canonical absorption target。

## 不负责

- 不替代 `manager-agent` 做 notice / claim / delegate / scheduling。
- 不直接替代 `freely-doc-B1_IBM-execution`、`freely-doc-B2_IBM-execution`、`freely-dev-loop-execution`。
- 不在 protected manager 工位直接落 worker 级长期产物。
- 不直接执行 runtime kill / restart；这仍由 runtime/scripts 执行。

## 最小输入

- raw intake item：`docs/B1-docs/raw-{key}/`
- manager 已选的 reaction：
  - `steer`
  - `followup`
  - `collect`
  - `interrupt`
  - `noise`
- 当前项目上下文：
  - `docs/PROJECT_INTENT.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - 按需读取相关 `B1-docs / issue / progress / recovery`
- 若已知目标工位或当前 issue，也应带入：
  - `execution_base`
  - `integration_target`
  - `depends_on`

## 最小输出

- `problem_kind`
- `current_context`
- `restart_point`
- `suggested_owner`
- `worker_handoff`
- `absorption_recommendation`
- `resolution_artifact`

## 工作流

1. 读取 raw intake message 与当前 intake metadata。
2. 明确这条 interruption 与当前 active issue / milestone / worktree 的关系：
   - 当前 issue 内纠偏
   - 新 discovery
   - runtime / control
   - 暂不进入主线的 noise
3. 保持 manager 已选 reaction mode 不变；本 skill 负责解释和细化，不负责私自重写调度决策。
4. 产出 `interruption resolution artifact`，至少包含：
   - 原始插话摘要
   - 为什么使用该 reaction
   - 推荐的 absorption target
   - 若有下游 worker，给出最小 handoff
5. 若 absorption 为 discovery，交给 `skill:freely-doc-B1_IBM-execution`。
6. 若 absorption 为 continuation，交给当前 issue / recovery / dev 路径。
7. 若 absorption 为 control，交给 runtime / manager continuity。
8. 若 absorption 为 noise，生成 resolution note 并回写原因。

## 完成判定

- 原始 interruption 已被解释，而不是只被转发。
- resolution artifact 已生成并可追溯回 intake item。
- 下游 worker 或 runtime 已拿到最小 handoff。
- canonical absorption target 已明确。
