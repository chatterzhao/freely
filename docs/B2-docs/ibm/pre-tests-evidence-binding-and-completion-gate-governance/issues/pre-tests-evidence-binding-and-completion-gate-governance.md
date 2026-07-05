# Issue: pre-tests-evidence-binding-and-completion-gate-governance

- issue_id: `I-20260327-0701`
- title: Pre-tests evidence binding and completion gate governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `pre-tests-evidence-binding-and-completion-gate-governance`
- issue-name: `pre-tests-evidence-binding-and-completion-gate-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/candidates.md#c-20260327-0651-a`
- source_brainstorm: `docs/pre-brainstorms/20260327-0651--pretests-gate-and-network-proxy-config/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/story-level-pre-tests-quality-gate-governance/issues/story-level-pre-tests-quality-gate-governance.md`
  - `docs/epics/workspace-routing-foundation/ibm-pretests-executable-acceptance-quality-governance/issues/ibm-pretests-executable-acceptance-quality-governance.md`
  - `docs/system/workspace/hooks/pre-commit.sh`
  - `docs/system/workspace/scripts/runtime/freely`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经冻结了两层上游真源：

- `pre-tests.md` 的最低质量线
- 对 Freely 自治能力默认需要 executable acceptance / real-environment / dogfood 的 IBM 质量要求

但系统还没有把这些定义变成 completion gate。结果就是：

- issue 可以声明 `phase_state=completed`
- feature worktree 也可以继续走 merge / cleanup
- 但系统并不知道当前 issue 的 `pre-tests.md` 是否已绑定、是否已有 machine-readable acceptance item、所需 evidence level 是否真的满足

这让 `pre-tests.md` 仍像一份“看起来存在的文档”，而不是一个能阻断假完成的 gate 输入。

## Scope

1. 冻结 issue 与 `pre-tests.md` 的最小绑定 contract：
   - issue 文档显式声明 `pre_tests_path`
   - issue 文档显式声明 `verification_artifact_dir`
2. 冻结 `pre-tests.md` 中 machine-readable acceptance item 的最小字段：
   - `id`
   - `requirement`
   - `evidence_level`
   - `status`
   - `artifact_ref`
3. 实现最小 gate：
   - 当 staged issue 准备把 `phase_state` 切到 `completed` 时
   - hook 必须检查对应 `pre-tests.md`
   - 若 acceptance items 缺失、未 pass、或 artifact ref 不成立，则阻断提交
4. 给其他 worktree 一条可复用入口：
   - `bin/pretests-gate`
   - 允许后续 merge / cleanup / runtime 路径复用同一条 gate，而不是再写一套判断

## Acceptance

- Freely 真源明确：issue-bound completion gate 必须通过 `issue -> pre_tests_path -> pre-tests acceptance items` 解析，而不是扫描全仓 `pre-tests.md`
- Freely 真源明确：准备将 issue 标记为 `completed` 时，若 `pre-tests.md` 不包含 machine-readable acceptance items，则提交被拒绝
- Freely 真源明确：准备将 issue 标记为 `completed` 时，若存在 `status != pass|not_applicable` 的 acceptance item，则提交被拒绝
- Freely 真源明确：准备将 issue 标记为 `completed` 时，若 `artifact_ref` 仍为 `pending://` 或指向缺失 artifact，则提交被拒绝
- `pre-commit` hook 与 standalone gate 使用同一实现，不产生平行判断
- 这条 gate 不要求一次性解决所有 retirement 自动推断；第一阶段先卡住“宣称 completed”这一关键出口

## Ready For Dev

当前最小 contract 已稳定：

1. 本 issue 是 `story-level-pre-tests-quality-gate-governance` 的 enforcement follow-on，不 reopen 已在 `in_verification` 的旧 issue。
2. 第一阶段只实现 `phase_state=completed` gate，不把 runtime cleanup / branch retirement 全部塞进同一批。
3. `pre-tests.md` 的 acceptance items 继续放在 Markdown 中，先不额外引入独立 JSON schema。
4. artifact plane 仍承载 canonical evidence；gate 只检查 machine-readable 摘要与 artifact existence，不把长证据搬进 hook 本身。

## Implementation References

- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/brainstorms/b-pre-tests-evidence-binding-and-completion-gate-governance.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/prd.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/tasks.md`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/quality/`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## Completion

- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/brainstorms/b-pre-tests-evidence-binding-and-completion-gate-governance.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/prd.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/tasks.md`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/tests/test-pretests-gate`
- `docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `docs/progress/workspace-routing-foundation/p-pre-tests-evidence-binding-and-completion-gate-governance.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-pretests-gate`
- `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `./bin/governance-check`
- `docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/code-reviews/20260327-pretests-gate-feature-verification.md`

## Next

- next_action: `completed`
- revisit_trigger: 当 merged worktree cleanup / retirement 仍可能绕过 issue-bound acceptance evidence 时，再以 follow-on issue 承接 retirement enforcement。
