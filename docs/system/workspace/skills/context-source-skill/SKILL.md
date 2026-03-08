---
name: context-source-skill
description: 对当前输入做来源分层、可执行性判定、workspace 准备判断与下一跳组装，为 lead-agent 产出自治编排结果。
---

# skill:context-source-skill

## 职责

- 判断当前输入属于原始发现源、编排来源还是延续来源。
- 判断当前是否已经拥有 milestone-owned issue，还是仍需先进入 pre-brainstorm。
- 判断本轮是否会写入仓库，以及是否需要先创建/进入 dedicated worktree。
- 产出下一跳 skill、最小上下文包与 workspace 准备建议。

## 不负责

- 不直接执行 `pre-brainstorm` / `IBM` / `dev-loop` 主工作。
- 不直接修改长期状态文档作为主工作。
- 不替代 `branch-management` 创建 worktree。

## 输入

- `input_context`
- `docs/PROJECT_INTENT.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/milestones.md`
- `workspace/tools.md`
- 按需读取：
  - `docs/pre-brainstorms/**`
  - issue / progress / recovery
  - code-review / test / chat / session evidence

## 输出

- `source_class`
- `route_kind`
- `usable_issue`
- `target_skill`
- `workspace_action`
- `execution_base`
- `integration_target`
- `depends_on`
- `phase_state`
- `session_evidence_refs`
- `required_context`
- `next_prompt`

## 情景步骤

### 情景 A：输入来自原始发现源

适用输入：
- `PROJECT_INTENT`
- chat / session evidence
- test
- code-review
- github-issue
- 治理漂移
- 运行时异常

这样做：
1. 先把当前输入归类为 `source_class=discovery`。
2. 检查 `docs/milestones.md` 中是否已经存在明确匹配的 milestone-owned issue。
3. 若没有稳定 issue，或只是命中候选 / 边界不稳：
   - 选择 `target_skill=doc-pre-brainstorm-execution`
   - 产出 `source_input`、`source_evidence_refs`、建议的 `pre_brainstorm_dir`
4. 若当前轮会写 docs，且当前不在合法 dedicated worktree：
   - `workspace_action=create_or_enter_worktree`
   - 默认 `execution_base=develop`
5. 返回下一跳 prompt，明确“先 pre-brainstorm，再 candidate->milestone”。
6. 若当前输入已带有会话证据，按 `docs/LAWS.md` 第 2C 章输出结构化 `session_evidence_refs`。

### 情景 B：输入来自 `milestones.md`

这样做：
1. 先把当前输入归类为 `source_class=milestone`。
2. 判断命中的条目属于哪一类：
   - `candidate_issues`
   - `committed_issues`
   - `completed_issues`
3. 如果是 `candidate_issues`：
   - 若边界仍不稳或还缺研究，进入 `doc-pre-brainstorm-execution`
   - 若 candidate 已清晰，进入 `doc-ibm-execution`
4. 如果是 `committed_issues`：
   - 若缺 `b-issue/prd/pre-tests/tasks`，进入 `doc-ibm-execution`
   - 若 docs 足够，进入 `dev-loop-execution`
   - 同时根据 milestone 条目的 `phase_state` 判断是否应该期待 `progress`
5. 如果是 `completed_issues`：
   - 不重复执行；返回校验/追溯或回流

### 情景 C：输入来自 issue / progress / recovery

这样做：
1. 归类为 `source_class=continuation`。
2. 如果是 `progress`：
   - 只把它视为 dev-loop 执行态跟踪，不把它当成新问题发现池
   - 选择 `target_skill=dev-loop-execution`
3. 如果是 `recovery`：
   - 恢复到中断前记录的目标环
4. 如果是 issue：
   - 缺 docs -> `doc-ibm-execution`
   - docs 足够 -> `dev-loop-execution`
5. 对 issue 条目，不再只看泛化 `status`；必须结合 `phase_state` 与 `runtime_state` 判断进入 IBM、dev-loop、completion verification 还是 recovery。
6. 若 `phase_state` 停在 `in_*`：
   - 先检查当前会话是否仍可 attach / resume
   - 再检查最近一次 `progress` / `recovery` 是否证明执行仍连续
   - 若证据中断或会话不可续接，先进入 `recovery-subagent-governance`
   - 只有恢复判定通过，才继续把该条目视为原 `in_*` 阶段
7. 若当前输入来自系统监控（如 PID 消失）而不是 AI 主动交接：
   - 不得直接把该 issue 标记为 `blocked_*`
   - 先按 `recovery -> progress -> issue -> milestone -> active worktree` 顺序定位上下文
   - 根据 `tool/session_id/jsonl_path/resume_hint` 选择正确的 resume 或 restart 路径

### 情景 D：本轮将写入仓库，需要先准备 worktree

这样做：
1. 判断当前目标 skill 是否会写入仓库：
   - `doc-pre-brainstorm-execution`：会
   - `doc-ibm-execution`：会
   - `dev-loop-execution`：会
2. 若当前在 `main/develop/pre-test-merge` 或主 worktree 中：
   - 标记 `workspace_action=create_or_enter_worktree`
3. 判断新工作是否依赖未合并父分支改动：
   - 不依赖 -> `execution_base=develop`
   - 依赖 -> `execution_base=<parent feature branch>`
4. 无论哪种情况，都保持 `integration_target=develop`，除非任务本身是 release/hotfix/premerge 场景。
5. 把 `execution_base`、`integration_target`、`depends_on` 一起交给下一跳。

## 完成判定

- 当前输入已被归类到正确来源层。
- 当前下一跳 skill 已明确。
- 若本轮需要写入，worktree 准备动作与基线已明确。
- 对依赖未合并父分支的任务，已显式给出 derived worktree 判断结果。
