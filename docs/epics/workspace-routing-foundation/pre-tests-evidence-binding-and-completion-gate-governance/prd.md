# PRD: pre-tests-evidence-binding-and-completion-gate-governance

## Goal

让 Freely 在 issue 进入 `completed` 前，能够 machine-readably 检查该 issue 的 `pre-tests.md` 是否真的满足所需 acceptance items 和 evidence。

## Why Now

上游真源已经定义了：

- `pre-tests.md` 质量线
- executable acceptance contract
- Freely 自治能力的 real-environment / dogfood 验收要求

当前真正缺的是 enforcement。没有 enforcement，这些要求仍可能在 closeout 时被绕过。

## Product Surface

- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/hooks/pre-commit.sh`
- `bin/pretests-gate`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## Non-Goals

- 一次性实现 retirement auto-check
- 统一所有历史 issue 的 artifact 命名
- 创建新的 centralized verification database

## Non-Negotiables

- 不扫描全仓 `pre-tests.md`
- 不允许 issue 在没有 `pre_tests_path` 绑定时宣称 `completed`
- 不允许 `status=pending|fail|blocked` 的 acceptance item 混进 completed commit
- 不允许 `artifact_ref=pending://...` 的 acceptance item 被当成已完成

## Context Pack

- `story-level-pre-tests-quality-gate-governance` 已冻结最低质量线
- `ibm-pretests-executable-acceptance-quality-governance` 已冻结 executable acceptance / real-env / dogfood 义务
- 当前要解决的是“如何 enforce”，不是再争论应该写什么样的 `pre-tests.md`

## Decomposition Tree

1. 为 issue 增加 `pre_tests_path` / `verification_artifact_dir` 绑定
2. 为 `pre-tests.md` 增加 machine-readable acceptance item 结构
3. 新增 standalone gate 命令
4. 把 `pre-commit` 接到 gate
5. 用 focused regressions 锁住 fail/pass 路径

## Prototype Path

最小原型是：

1. 一个 issue 在 staged 变更里把 `phase_state` 改成 `completed`
2. hook 找到该 issue 绑定的 `pre-tests.md`
3. gate 发现任一 acceptance item 仍 `pending`
4. 提交被拒绝，并指出缺失项

## Eval Plan

成功：

- `completed` commit 会在缺少 acceptance pass/artefact 时被拦住
- 其他 feature worktree 合并 develop 后，沿用同一套 gate，不用再靠人工记忆
- `pre-tests.md` 既保留可读性，又具备最小 machine-readable 能力

失败：

- hook 不知道看哪个 issue
- gate 仍允许 `pending://` artifact 或 `pending` status 通过
- 实现只对某个 story 特化，不能被其他 worktree 复用

## Execution Slices

1. issue/IBM truth update
2. `pretests-gate` implementation
3. `pre-commit` integration
4. focused regressions
5. milestone / progress writeback

## Revisit Triggers

- 当 completed gate 稳定后，继续扩到 runtime cleanup / retirement gate
- 当前端开始消费 verification summary 时，再决定是否升级为结构化 manifest

## Dev-Loop Handoff

本 issue 先做 CLI + hook enforcement，不要求 runtime manager 立刻接管 retirement decision。
