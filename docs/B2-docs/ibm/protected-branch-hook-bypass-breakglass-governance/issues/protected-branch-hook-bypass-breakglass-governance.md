# Issue: protected-branch-hook-bypass-breakglass-governance

- issue_id: `I-20260402-0020-A`
- title: Hook bypass break-glass governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `protected-branch-hook-bypass-breakglass-governance`
- issue-name: `protected-branch-hook-bypass-breakglass-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260402/candidates.md#c-20260402-0020-a`
- source_brainstorm: `docs/B1-docs/raw-20260402/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/ibm/develop-merge-issue-binding-and-cmi-governance/issues/develop-merge-issue-binding-and-cmi-governance.md`
  - `docs/B2-docs/git-worktree/worktree-exclusive-ownership-and-promotion-lease-governance/issues/worktree-exclusive-ownership-and-promotion-lease-governance.md`
  - `docs/system/workspace/hooks/README.md`
  - `docs/system/workspace/scripts/worktree/pr-merge-guarded`
  - `docs/system/workspace/scripts/quality/governance-check`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前已经有 protected-branch hooks、`pr-merge-guarded`、develop-bound governance merge gate 与 promotion ownership gate，但还缺一个更高层的 canonical contract：

1. 哪些 hook/gate bypass 永远非法
2. 哪些极端场景才允许 break-glass
3. 合法 break-glass 必须留下哪些证据
4. merge conflict completion 如何继续走受控路径，而不是回退到裸 `git commit`
5. 后续 `governance-check` 如何发现未经授权的 bypass

没有这层 contract，任何真实 gate false negative 都可能被 AI 或人类解释成“这次先跳过去”，从而破坏 Freely 的 dogfooding 治理。

## Scope

1. 冻结 protected-branch hook/gate bypass 的 constitutional principle 与 law-level whitelist。
2. 冻结第一阶段 break-glass reason taxonomy、required evidence、minimal operation scope 与 follow-on obligation。
3. 定义 guarded merge completion path 的最小 contract，避免冲突后回退到裸 `git commit`。
4. 定义 bypass receipt / audit contract，让 develop-bound merge 的例外路径可追溯、可检查。
5. 明确当前 `27faa2e` 与 `a10f6d8` 的处置原则：可逆不等于应立即回退，默认先 forward-fix 治理。

## Non-Goals

1. 不把所有 Git 本地限制升级成宿主级绝对不可绕过控制。
2. 不在第一阶段重写整套 branch governance。
3. 不把 ownership anti-stomp 功能本体重新判定为错误。
4. 不把 skill 变成“允许 bypass”的权威来源。

## Acceptance

1. `CONSTITUTION` 明确写出 protected-branch hook/gate bypass 默认违规，只有 break-glass 白名单例外。
2. `LAWS` 成为唯一的 break-glass whitelist truth，至少冻结 reason taxonomy、前置条件、required evidence、forbidden examples 与 follow-on duty。
3. `AGENTS`、`hooks/README`、relevant skills 只作为入口提醒与执行消费，不再自行发明允许场景。
4. `pr-merge-guarded` 的冲突后 completion path 有明确的受控 contract，不再默认回退到裸 `git commit`。
5. `governance-check` 或等价 quality gate 定义 develop-bound bypass audit contract，使未经授权 bypass 在后续 canonical 检查中可见。
6. issue-bound artifacts 明确记录当前两条 merge 的判断：`27faa2e` 可干净逆转，`a10f6d8` 可逆但会与 writeback 产物冲突，因此“能撤”与“应该立即撤”必须分开。

## Current Artifact Set

- `docs/B1-docs/raw-20260402/brainstorms.md`
- `docs/B1-docs/raw-20260402/candidates.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/issues/protected-branch-hook-bypass-breakglass-governance.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/brainstorms/b-protected-branch-hook-bypass-breakglass-governance.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/prd.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/pre-tests.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/tasks.md`
- `docs/B2-docs/ibm/protected-branch-hook-bypass-breakglass-governance/code-reviews/20260402-protected-branch-hook-bypass-breakglass-verification.md`
- `docs/milestones.md`

## Current Evidence

- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `AGENTS.md`
- `docs/system/workspace/hooks/README.md`
- `docs/system/workspace/hooks/protected-branch-breakglass-receipts.md`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/scripts/worktree/pr-merge-guarded`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/progress/workspace-routing-foundation/p-protected-branch-hook-bypass-breakglass-governance.md`

## Verification

- `git diff --check`
- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-governance-check-candidate-v2`
- `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-availability-watchdog-path-resolution`
- `./bin/governance-check`

## Completion

- canonical_merge_commit: `52f55c0`
- canonical_merge_target: `develop`
- closeout_note: `Protected-branch bypass governance is now absorbed into canonical develop with receipt-bearing merge replay, audited historical break-glass ledger, and canonical lifecycle writeback.`
