---
name: doc-pre-brainstorm-execution
description: 执行 pre-brainstorm 前置收敛环，负责把原始问题收敛为 candidate，并与 milestone 保持原子同步。
---

# skill:doc-pre-brainstorm-execution

## 职责

- 负责把尚未形成稳定 issue 边界的问题收敛为 pre-brainstorm 产物，并把 candidate 与 milestone 保持原子同步。
- 负责在 docs 范围内完成前置研究、边界收敛、候选分解与下一跳建议。
- 不负责 issue-bound `IBM+G` 产物。
- 不负责代码实现、测试执行与 progress 主回写。
- 调用方必须把当前要处理的问题、证据和目标 pre-brainstorm 范围传入；本 skill 不负责自己挑选新的起始问题。

## 进入条件

- 当前输入尚未命中可继续执行的正式 issue。
- 当前问题仍处于前置研究、边界收敛、候选分解阶段。
- 常见来源包括：
  - `chat` / session evidence
  - `review`
  - `test`
  - `github-issue`
  - `docs/PROJECT_INTENT.md`
  - milestone 中仍停留在 `candidate_issues` 的条目

## 输入上下文

- 调用方传入的当前问题描述与来源证据
- 调用方显式附带或指向的：
  - `docs/PROJECT_INTENT.md`
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/milestones.md`
  - 当前关联的 `docs/pre-brainstorms/<id>/` 目录；若不存在则创建
- 按需读取调用方已指向的补充证据：
  - 相关 `issue/progress/recovery` 证据
  - review / test / chat 原始输入
  - 相关治理文档

## 调用约定

- 调用方至少应传入：
  - `source_input`
  - `source_evidence_refs`
  - `pre_brainstorm_dir` 或待创建目标
  - `milestone_path`
  - 当前推荐下一跳仍是本 skill 的原因
- 本 skill 只处理传入问题及其上下文，不在 skill 内另起一个新的研究主题。

## 工作产物

- `docs/pre-brainstorms/<id>/brainstorms.md`
- `docs/pre-brainstorms/<id>/candidates.md`
- `docs/milestones.md`
- 按需更新：
  - 相关治理文档中的术语或路由说明
- `docs/progress/**` 不是本 skill 的工作产物。

## 主事实源

- pre-brainstorm 阶段的主事实源是 `candidates.md`
- milestone 承接 candidate 的可扫描入口，但不是前置收敛事实源
- 本 skill 的目标是把原始问题收敛成可路由的 candidate，而不是直接产出正式 story 产物

## 工作步骤

1. 确认当前为何不能直接进入 `doc-ibm-execution` 或 `dev-loop-execution`：
   - 尚无 issue path
   - milestone 中仅命中 candidate / research-needed 项
   - 虽有相关条目，但当前仍需研究、排序、边界收敛
2. 使用调用方传入的目标目录，或在该问题对应路径下创建 `docs/pre-brainstorms/<id>/`。
3. 在 `brainstorms.md` 中记录至少这些内容：
   - 问题来源
   - 当前为何不能直接走已有 issue
   - 是否属于新问题、既有问题扩边、或治理漂移
   - 推荐后续路由
4. 在 `candidates.md` 中写入或更新 candidate：
   - `title`
   - `status`
   - `decision_reason`
   - `promoted_issue_path`
   - `milestone`
   - `session_refs`
5. 当 candidate 状态不是 `dropped` 时，原子更新 `docs/milestones.md`：
   - 归属哪个 milestone
   - 位于 `candidate_issues`
   - 当前下一步动作通常应指向 `doc-ibm-execution`，而不是直接 `dev-loop-execution`
   - 保留 candidate 与 milestone 的可追溯映射
6. milestone 绑定完成后，必须回写 `candidates.md`：
   - `milestone` 不再允许停留在 `pending://milestone-binding`
   - 若该 candidate 已被接纳进入后续执行面，`status` 更新为 `promoted`
7. 若只是治理问题，允许同步更新治理文档，但不得假装已经进入 dev-loop。

## 不负责

- 不产出正式 issue 目录下的：
  - `issues/{issue}.md`
  - `brainstorms/b-{issue}.md`
  - `prd.md`
  - `pre-tests.md`
  - `tasks.md`
- 不直接进入实现、测试与进度回写

## 状态回流给 auto-loop

当出现以下任一情况时，应结束本轮 skill 内工作，并把状态交还 `auto-loop`：

- 已经收敛出可进入 `doc-ibm-execution` 的 candidate
- 发现当前问题其实已存在稳定 issue 边界，应 reroute
- 当前被阻塞，无法继续前置收敛
- 当前轮只完成了部分研究，需要后续继续本环

回流时最少应提供：
- `status`: `in_progress | blocked | reroute_required | completed`
- `why`
- `updated_artifacts`
- `next_recommended_route`
- `recovery_context`

语义要求：
- 若仍需继续 pre-brainstorm，`next_recommended_route` 保持 `doc-pre-brainstorm-execution`
- 若已形成 issue-ready candidate，`next_recommended_route` 设为 `doc-ibm-execution`
- 若发现当前问题应回到已有 issue，上报 reroute 原因与对应 evidence

## 完成判定

- `brainstorms.md` 与 `candidates.md` 已更新。
- `docs/milestones.md` 与 candidate 状态保持原子一致。
- 当前问题已经被收敛成后续可由 `doc-ibm-execution` 接管的 candidate，或已明确为何继续停留在本环。
