# Issue: test-lane-routing-and-enforcement-governance

- issue_id: `I-20260405-1914-A`
- title: Test lane routing and enforcement governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `test-lane-routing-and-enforcement-governance`
- issue-name: `test-lane-routing-and-enforcement-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-1914-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914/verification/pre-tests.md
- progress_path: `pending://progress-created-on-dev-loop`
- verification_artifact_dir: docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914/code-reviews
- depends_on:
  - `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

当前仓库已经把测试 lane 语义写进 `AGENTS.md`、`LAWS.md` 和 skills，并出现了 `./bin/test-lane` 的实现雏形，但这批能力还没有正式 owner 链路。

同时，已暴露出几个真实执行问题：

1. `feature-local` 只阻止 protected branches，却允许任意 ad hoc writable branch 冒充 dedicated feature/release/hotfix/premerge test lane。
2. `./bin/test-lane` / `./bin/test-test-lane` 入口不可直接执行。
3. 仍有参考文档继续保留旧 replay-only promote 语义。

这说明当前问题已经是独立的 lane-routing/enforcement surface，而不是 promote-gate owner 的附带实现。

## Scope

1. 冻结 `feature-local`、`premerge-integration`、`post-merge-followthrough` 三条 canonical lane，其中 `feature-local` 仅覆盖 dedicated `feature/*`、`feature/premerge-*`、`release/*`、`hotfix/*`。
2. 冻结 lane 与 branch/worktree family 的匹配关系。
3. 落地 `./bin/test-lane` 和 `./bin/test-test-lane` 的 wrapper correctness。
4. 落地 lane misuse 的 machine enforcement 和 focused regression。
5. 对齐直接消费 lane 语义的 truth sources / skills / references。

## Non-Goals

1. 不在本 owner 内自动推断 lane。
2. 不在本 owner 内自动创建 `test-pre-merge-*` batch。
3. 不在本 owner 内实现 lifecycle automation。
4. 不在本 owner 内定义统一 test catalog 或 orchestration DSL。
5. 不在本 owner 内重新打开 `test-pre-merge-* -> develop` 的 promote model 讨论。

## Acceptance

1. 三条 canonical lane 的职责与匹配分支族清晰稳定。
2. `feature-local` 不再接受任意 writable branch，只接受 dedicated `feature/*`、`feature/premerge-*`、`release/*`、`hotfix/*`。
3. `./bin/test-lane` 和 `./bin/test-test-lane` 可直接执行。
4. focused regression 覆盖 lane misuse、入口可执行性和命令退出码传递。
5. skills / checklist / hook README 不再残留旧 replay-only promote 语义。

## IBM Handoff

- implementation_scope_summary:
  - `I-20260405-1914-A` 负责把显式测试 lane 语义接到 wrapper、machine enforcement、focused regression 和相关 truth-source sync。
  - 这条 owner 允许同步更新 `AGENTS.md`、skills、references、`test-lane` 脚本和其 focused tests。
  - auto-routing、batch create、lifecycle automation 仍由后续 owner 承接。
- required_doc_refs:
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914issues/test-lane-routing-and-enforcement-governance.md`
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914brainstorms/b-test-lane-routing-and-enforcement-governance.md`
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914prd.md`
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914pre-tests.md`
  - `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914tasks.md`
  - `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`

## Verification

- `git diff --check`
- `./bin/test-test-lane`
- `./bin/governance-check`
- focused promote-gate regressions that still guard the new `test-pre-merge-* -> develop` semantics

## Completion

- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/milestones.md`
- `AGENTS.md`
- `docs/CONSTITUTION.md`
- `docs/LAWS.md`
- `docs/system/workspace/scripts/quality/test-lane`
- `docs/system/workspace/scripts/tests/test-test-lane`
- `bin/test-lane`
- `bin/test-test-lane`
- `docs/system/workspace/skills/branch-management/SKILL.md`
- `docs/system/workspace/skills/dev-loop-execution/SKILL.md`
- `docs/system/workspace/skills/branch-management/references/pre-test-merge-flow.md`
- `docs/system/workspace/hooks/README.md`
- `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914code-reviews/20260405-test-lane-routing-and-enforcement-implementation-decision.md`
- `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914code-reviews/20260405-test-lane-routing-and-enforcement-verification.md`

## Next

1. `2026-04-05` closeout: explicit lane routing, executable wrappers, and focused lane misuse regression are now owned and verified as one bounded package.
2. Reopen only for automatic lane inference, batch creation UX, or wider test orchestration surfaces that were explicitly kept out of scope here.
3. Do not reopen this owner merely to add new branch families; lane additions must first prove a new constitutional branch responsibility.
