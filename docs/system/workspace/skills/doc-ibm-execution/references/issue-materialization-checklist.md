# Issue Materialization Checklist

## Entry checks

- 当前输入已经是 milestone-owned issue，或 candidate 已被 milestone 接纳
- 若仍只是未绑定 milestone 的 pre-brainstorm candidate：回到 `doc-pre-brainstorm-execution`
- 若来源 candidate 是 `candidate_format_version: v2`，先读取其 `acceptance_criteria`、`promotion_gate`、`open_questions`、`acceptance_reviews`

## Stable ownership required

写 IBM 正式产物前，必须先确认：

- `epic-name`
- `story-name`
- `issue-name`

任一未稳定：

- 停止写正式 IBM 产物
- 回到 `doc-pre-brainstorm-execution`

## Required artifacts

- `docs/epics/{epic-name}/{story-name}/issues/{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/brainstorms/b-{issue-name}.md`
- `docs/epics/{epic-name}/{story-name}/prd.md`
- `docs/epics/{epic-name}/{story-name}/pre-tests.md`
- `docs/epics/{epic-name}/{story-name}/tasks.md`

写完后仍需按 [prd-quality-bar.md](prd-quality-bar.md) 检查 `prd.md` 是否达到 AI-ready 最小结构；未达标时不得宣称 `done_ibm`。

## Required write-back

- `candidates.md.promoted_issue_path`
- `docs/milestones.md.issue_path`
- `phase_state=in_ibm`
- 继承有效 `session_refs`
- 在 issue / `prd.md` / `pre-tests.md` / `tasks.md` / issue-bound brainstorm 中继续深化 acceptance 边界
- 在 `pre-tests.md` 中默认先写 executable acceptance 行为，而不是 wording review / truth-source reading checklist
- `pre-tests.md` 默认显式回答：
  - pre-merge focused regression / smoke
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
- 若某类 acceptance 不适用，必须同时写出：
  - why_not_applicable
  - replacement_evidence
- 对每个关键 acceptance 面，默认写出：
  - environment
  - evidence
  - failure signal
  - failure handling / replay expectation
- 若存在 merge 后验收，显式标记 `post-merge acceptance`
- 在 `pre-tests.md` 中写清 story-level 质量 gate 最低字段：
  - acceptance target
  - testing layer
  - target environment
  - required evidence
  - blocker taxonomy
- 最小 blocker taxonomy 至少区分：
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`
- 对 `post-merge acceptance`，必须同时写出：
  - target environment: `develop` 或 `pre-test-merge`
  - environment type: `protected verification worktree`
  - failure handling: 验收失败后回到 feature worktree / 新 feature worktree 修复
  - route semantics:
    - `pre-test-merge`: 主线前临时验证，只做预检运行测试 / 预测试 merge，不直接并入 `develop`
    - `develop`: 已进入主线后的 completion verification，不承担主线前预测试
