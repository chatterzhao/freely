# Issue: worktree-tool-boundary-bootstrap-governance

- issue_id: `I-20260403-2041-A`
- title: Worktree tool boundary bootstrap governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `worktree-tool-boundary-bootstrap-governance`
- issue-name: `worktree-tool-boundary-bootstrap-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260403/candidates.md#c-20260403-2041-a`
- source_brainstorm: `docs/B1-docs/raw-20260403/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
- reopen_reason: `the first tool-materialization slice did not yet rematerialize managed local tool boundaries into sibling worktrees or normalize raw worktree entrypoints around that contract`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-worktree-tool-boundary-bootstrap-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/issues/freely-tool-autonomy-policy-materialization-governance.md`
  - `docs/B2-docs/config/packaging/issues/canonical-product-posture-bootstrap-reconciliation-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already froze the high-level product/tool posture contract, but the current dogfood workflow still had one practical gap: sibling worktrees could exist without inheriting the managed local tool boundary surfaces that make owner development safe.

That meant a new worktree could lack:

1. tool-native project config such as `.codex/config.toml`
2. Freely wrapper-local boundary bootstrap truth
3. explicit launch-time allowance for the sibling worktrees root on tools such as `iflow`

If that gap remains, the canonical workflow still tempts operators back toward protected-root editing or ad hoc tool reconfiguration.

## Scope

1. Add a managed `freely sync-tooling` path that rematerializes project-local tool surfaces into a target worktree.
2. Make standard worktree entrypoints call that sync path:
   - `wt-create`
   - protected-branch `post-checkout` auto-worktree path
3. Keep project root as the integration / merge surface while extending the managed writable/trusted boundary to `{project}-worktrees` where tools support it.
4. Document the per-tool split between:
   - tool-native project config
   - Freely wrapper/bootstrap surface
   - launch-time boundary extension
5. Rewrite governance guidance so raw `git worktree add` becomes manual fallback plus `freely sync-tooling`, not the normal managed path.

## Non-Goals

1. Do not redefine the already-completed autonomy or activation-consent contract.
2. Do not force unsupported tools into invented project-local config formats.
3. Do not turn project root into a forbidden read-only shell; merge and integration remain valid there.
4. Do not widen into general manager/runtime orchestration redesign.

## Acceptance

1. New worktrees can regain the managed local tool boundary surfaces without depending on Git copying ignored or untracked files.
2. `freely sync-tooling` is the canonical fallback when a worktree is created manually.
3. `wt-create` and protected-branch `post-checkout` automatically rematerialize tool boundaries into sibling worktrees.
4. `codex` keeps its tool-native project config surface while `iflow` and similar tools use wrapper and launch-time boundary extension where no verified project-local surface exists.
5. `AGENTS.md`, skills, and hook guidance treat `wt-create` as standard and raw `git worktree add` as explicit manual fallback only.
6. Focused regressions cover explicit sync, `wt-create`, `post-checkout`, and launch-time `iflow` boundary injection.

## Completion

- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260403/brainstorms.md`
- `docs/B1-docs/raw-20260403/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
- `docs/B2-docs/config/packaging/brainstorms/b-worktree-tool-boundary-bootstrap-governance.md`
- `docs/B2-docs/config/packaging/prd.md`
- `docs/B2-docs/config/packaging/pre-tests.md`
- `docs/B2-docs/config/packaging/tasks.md`
- `docs/B2-docs/config/packaging/code-reviews/20260403-worktree-tool-boundary-bootstrap-implementation-decision.md`
- `docs/B2-docs/config/packaging/code-reviews/20260403-worktree-tool-boundary-bootstrap-verification.md`
- `docs/progress/freely-product-architecture/p-worktree-tool-boundary-bootstrap-governance.md`
- `AGENTS.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/hooks/pre-commit.sh`
- `docs/system/workspace/skills/premerge-reconcile/SKILL.md`
- `docs/system/workspace/skills/branch-management/references/feature-worktree-flow.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/runtime/interruption-manager-handler`
- `docs/system/workspace/scripts/runtime/signal-intent-handler`
- `docs/system/workspace/scripts/worktree/wt-create`
- `.githooks/post-checkout`
- `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`
- `docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
- `docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`
- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`
- `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`
- `bash docs/system/workspace/scripts/tests/test-tool-launchers-iflow-add-dir`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
- `bash docs/system/workspace/scripts/tests/test-signal-intent-handler-cc`
- `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
- `bash docs/system/workspace/scripts/tests/test-wt-create-syncs-tooling`
- `bash docs/system/workspace/scripts/tests/test-post-checkout-syncs-tooling`
- `bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` after closeout verification recorded in `docs/B2-docs/config/packaging/code-reviews/20260405-worktree-tool-boundary-bootstrap-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` regresses sibling-worktree boundary rematerialization, re-teaches raw `git worktree add` as the managed default, or weakens the per-tool split between project-local config, wrapper bootstrap, and launch-time boundary extension.
