# Issue: worktree-helper-shell-source-compatibility-governance

- issue_id: `I-20260405-2302-A`
- title: Worktree helper shell source compatibility governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `worktree-helper-shell-source-compatibility-governance`
- issue-name: `worktree-helper-shell-source-compatibility-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-2302-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-worktree-helper-shell-source-compatibility-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
  - `AGENTS.md`
  - `docs/system/workspace/skills/branch-management/references/feature-worktree-flow.md`
  - `docs/system/workspace/scripts/worktree/wt-add`
  - `docs/system/workspace/scripts/worktree/wt-enter`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经把 worktree boundary、`wt-create`、`sync-tooling` 与 `post-checkout` auto-bootstrap 冻结为 canonical contract，但当前 dogfood 又暴露出一个新的 CLI-first regression：

1. 文档和 `AGENTS.md` 指导用户执行 `source ./bin/wt-add ...`
2. 文档和 worktree guidance 也保留了 `source ./bin/wt-enter ...`
3. 默认 shell 环境是 `zsh`
4. 现有 `bin/wt-add` / `bin/wt-enter` wrapper 直接读取 `BASH_SOURCE`，因此在默认 `zsh` 的 source 路径上立即失败

这意味着实际 user-facing command path 已经偏离仓库真源：内部脚本仍可在 `bash` 测试里通过，但文档教给用户的正式命令在默认 shell 下坏掉。

## Scope

1. 修复 `bin/wt-add` 与 `bin/wt-enter` wrapper 的 source-safe shell compatibility。
2. 保持现有 helper contract：
   - `wt-add` 仍必须在 protected branches / `test-pre-merge-*` 上拒绝 direct add
   - `wt-enter` 仍必须把 shell 导向正确的 dedicated worktree
3. 增加 focused regressions，覆盖 documented `bin/` wrapper path，而不是只测内部 worktree scripts。
4. 仅在证据表明确有同类 shared bug 时，吸收最小必要的 sibling sourced wrapper fix；不得顺手重写整套 wrapper framework。

## Non-Goals

1. 不重开 worktree boundary/bootstrap owner。
2. 不改变 `wt-create` 作为标准入口的地位。
3. 不设计新的 cross-shell abstraction layer。
4. 不把所有 `bin/*` wrapper 一次性改成统一框架，除非当前 regression 证明它们同样 broken。

## Acceptance

1. `zsh -lc 'source ./bin/wt-add -- README.md'` 不再因 wrapper 读取 `BASH_SOURCE` 而在入口处崩溃。
2. `zsh -lc 'source ./bin/wt-enter develop'` 不再因 wrapper 读取 `BASH_SOURCE` 而在入口处崩溃。
3. `wt-add` 仍保持当前 branch protection behavior。
4. `wt-enter` 仍保持当前 worktree entry behavior。
5. Focused regressions 覆盖实际 `bin/` wrapper path，避免内部脚本与用户命令路径再漂移。

## Current Evidence

1. `zsh -lc 'source ./bin/wt-add -- README.md'` currently fails with `BASH_SOURCE[0]: parameter not set`.
2. `zsh -lc 'source ./bin/wt-enter develop'` currently fails with the same wrapper-level error.
3. `bash -lc 'source ./bin/wt-add -- README.md'` reaches the intended protection gate, proving the problem is the wrapper shell contract rather than helper semantics.
4. `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow` currently exercises copied internal scripts under `bash`, not the documented `bin/` wrappers.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/issues/worktree-helper-shell-source-compatibility-governance.md`
- `docs/B2-docs/config/packaging/brainstorms/b-worktree-helper-shell-source-compatibility-governance.md`
- `docs/B2-docs/config/packaging/prd.md`
- `docs/B2-docs/config/packaging/pre-tests.md`
- `docs/B2-docs/config/packaging/tasks.md`
- `docs/progress/freely-product-architecture/p-worktree-helper-shell-source-compatibility-governance.md`
- `docs/B2-docs/config/packaging/code-reviews/20260405-worktree-helper-shell-source-compatibility-verification.md`
- `bin/wt-add`
- `bin/wt-enter`
- `docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- `docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`

## Verification

- `zsh -lc 'source ./bin/wt-add -- README.md'`
- `zsh -lc 'source ./bin/wt-enter develop'`
- `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- `bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` via guarded merge `3e0c8b9`.
- Verification is recorded in `docs/B2-docs/config/packaging/code-reviews/20260405-worktree-helper-shell-source-compatibility-verification.md`.
- Reopen only if canonical `develop` again requires shell-specific workarounds for documented worktree helper commands, or if adjacent sourced worktree helpers prove to share the same contract break.
