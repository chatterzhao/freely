# Issue: pre-test-merge-responsibility-usage-and-lifecycle-governance

- issue_id: `I-20260322-1801`
- title: pre-test-merge responsibility, usage, and lifecycle governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `pre-test-merge-responsibility-usage-and-lifecycle-governance`
- issue-name: `pre-test-merge-responsibility-usage-and-lifecycle-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/code-reviews`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md#c-20260322-1801-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/CONSTITUTION.md`
  - `docs/LAWS.md`
  - `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
  - `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

## Compatibility Note

- 历史 issue/story/path 保留 `pre-test-merge` 命名，避免破坏既有引用。
- 当前 canonical 语义已经升级为 `test-pre-merge-*` 测试批次前缀族。
- 本文提到的 `pre-test-merge`，都应按 `test-pre-merge-*` 前缀族解释，而不是单例长期分支。

## Why

Freely 这次不是遇到一次性 merge 事故，而是暴露出 `pre-test-merge` 作为治理对象的定义不完整：

- 它是临时预集成验证批次，但当前系统还不能稳定表达这个批次何时开始、何时 stale、何时必须退休。
- 它被误当成比较基线、旧实现回收中转站，甚至接近“事实主线”，与 `develop` 的长期集成真相角色发生混淆。
- 进入 `develop` 的 promotion 语义也不清楚：到底是保留整个批次快照，还是回放来源 feature 的已验证结果。

如果这层职责定义不先稳定，Freely 之后即使补 runtime/status 也只是围绕不清晰的治理对象加功能，仍会继续在狗粮过程中反复误用 `pre-test-merge`。

## Scope

1. 明确 `pre-test-merge` 的唯一职责：它是临时预集成验证批次，不是长期开发父分支，也不是默认事实真相。
2. 明确 `pre-test-merge` 的允许/禁止操作：
   - 允许：组合验证、短周期集成验收、复杂冲突预演、promotion 前预演。
   - 禁止：在 protected 环境直接 add/commit 新实现、把它当默认 feature 父分支、把旧批次快照当成当前 `develop` 真相。
3. 明确批次生命周期：
   - 启用
   - 进行中
   - 已验证
   - 已失效 / stale
   - 已退休
4. 明确 stale / retire / rebuild 的治理信号：
   - `develop` 已继续前进并让旧批次不再具备权威性
   - 批次内出现未回流到来源 feature 的 protected-env 差异
   - promotion/cleanup 证据未闭环
5. 明确 promotion 语义边界：
   - 何时可以把批次结果推进到 `develop`
   - 何时必须 replay 来源 feature，而不是保留 `pre-test-merge` 快照

## Acceptance

- `CONSTITUTION.md`、`LAWS.md` 与 `pre-test-merge-flow.md` 对 `pre-test-merge` 的职责边界、允许/禁止操作和临时性表述一致。
- `cleanup-lifecycle.md` 与 `manager-reactivation-patrol.md` 能表达 stale / retire / rebuild 的最小治理信号和收口义务。
- `docs/milestones.md` 与 issue 文档对当前问题的下一跳一致：先稳定职责定义，再进入能力实现，不把 runtime/status 补丁和治理定义混成同一个 issue。
- 本 issue 明确声明 `pre-test-merge` 不是长期真相面，`develop` 才是最终集成主线；promotion 默认围绕来源 feature 的已验证结果，而不是默认保留批次快照。

## Completion

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/skills/branch-management/references/cleanup-lifecycle.md`
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/code-reviews/20260322-pre-test-merge-responsibility-usage-and-lifecycle-governance-verification.md`
- `docs/pre-brainstorms/20260322-1801--pre-test-merge-governance-lifecycle/candidates.md`
- `docs/milestones.md`

## Verification

- `./bin/governance-check`
- read the updated governance truth sources together and confirm they all describe the same `pre-test-merge` role
- confirm the follow-on capability work remains a separate lifecycle instead of being silently folded into this definition issue

## Next

- 先完成职责和生命周期定义收敛。
- `pre-test-merge lifecycle management capability` 仍保留为后续独立 lifecycle，不在本 issue 中直接实现 runtime/status 能力。
