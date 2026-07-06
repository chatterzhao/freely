# Candidates - 20260405-2358--cli-command-audit-regressions

## C-20260405T235800Z-A: legacy issue

- candidate_format_version: `v2`
- title: Fresh-project bootstrap and baseline scoping followthrough after CLI audit
- status: `promoted`
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/B2-docs/config/packaging/raw-20260402-0403issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- promoted_issue_id: `I-20260405T235800Z-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: followthrough on canonical `develop` narrowed the original bundle, but not as far as the previous draft claimed. `freely ensure-interruption-dispatch --project <x>` now fails through the doc gate instead of leaking raw `find` noise, but `freely sync-tooling --source-project <repo> --project <fresh-git-project>` still omits `.githooks`, a subsequent `freely init` still fails on missing hook assets, and `freely baseline-status --project <x>` plus the baseline segment of `freely status --project <x>` still drift back to the Freely root instead of the target project.
- why_now:
  - fresh-project bootstrap is still a first-hop CLI contract, and failing there blocks every later command audit on non-root projects
  - the 2026-04-06 replay proves the old candidate must be narrowed, but not all the way down to `.githooks`; the baseline scoping defect is still live on canonical `develop`
  - the surviving defects are still narrow enough to keep separate from runtime restart semantics and from already-completed wrapper-packaging work
- acceptance_criteria:
  - `freely sync-tooling --source-project <repo> --project <fresh-git-project>` materializes the hook assets needed for a subsequent `freely init`, or `freely init` synthesizes the same minimum hook surface instead of failing on missing `.githooks`
  - `freely baseline-status --project <x>` reports baseline metadata for `<x>`, not the Freely root
  - `freely status --project <x>` keeps both `baseline` and `live` segments pinned to `<x>`, not a split root/project view
  - `freely ensure-interruption-dispatch --project <x>` continues to fail with an explicit semantic result rather than raw filesystem noise when the intake/doc prerequisites are absent
- promotion_gate:
  - keep this owner scoped to fresh-project bootstrap, baseline scoping, and adjacent non-regression guards for project-targeted CLI surfaces
  - do not absorb runtime supervision churn or intake counter reconciliation here
- next_action: This candidate is now materialized as `I-20260405T235800Z-A`. Keep the owner narrow: repair `sync-tooling` retargeting plus `.githooks` rematerialization, prove `baseline-status` / `status --view baseline` stay pinned to the target project, and keep `ensure-interruption-dispatch` as a non-regression guard rather than reopening runtime control-plane work.
- revisit_trigger: fresh-project bootstrap still requires manual hook copying, `baseline-status` / `status` baseline scoping still drifts from the target project, or another project-targeted CLI command regresses the current doc-gate semantics.

## C-20260405T235800Z-A: legacy issue

- candidate_format_version: `v2`
- title: Runtime control-plane CLI stability after full command audit
- status: `proposed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- promoted_issue_id: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: real start/restart/stop/chat/restore-work flows still expose stale pid repair, readiness instability, hanging chat completion, and inconsistent intake status counters, which means the control-plane contract is not yet reliable under end-to-end CLI use.
- why_now:
  - these failures emerged only when the runtime commands were exercised end-to-end instead of via isolated unit-style wrappers
  - stale pid cleanup and inconsistent intake accounting both directly undermine operator trust in runtime state
  - this should stay separate from bootstrap scoping because the diagnosis and fixes will likely live in supervision and intake state transitions
- acceptance_criteria:
  - `freely start` / `restart` / `stop` / `restore-work` behave deterministically without stale foreign pid repairs or unexpected hard-kill fallback in the normal path
  - `freely chat` completes the expected intake/control-plane flow without hanging after recording and claim
  - `freely intake status` reports internally consistent counters before and after claim / resolve transitions
- promotion_gate:
  - keep the owner focused on runtime/control-plane semantics surfaced by the audited commands
  - do not bundle unrelated wrapper executable-bit fixes or project bootstrap decisions
- next_action: keep this candidate in `M-20260306-workspace-routing-foundation`, separate “stale pid / readiness / restart” evidence from “intake status / chat completion” evidence, and confirm whether they belong in one supervision owner or two adjacent ones.
- revisit_trigger: any audited runtime command still requires manual cleanup of stale children or reports contradictory intake state on canonical develop.

## C-20260405T235800Z-A: legacy issue

- candidate_format_version: `v2`
- title: CLI wrapper packaging and regression-surface audit
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/config/cli-wrapper-packaging-and-regression-surface-governance/raw-20260405-2358issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- promoted_issue_id: `I-20260405T235800Z-C`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: several `bin/` wrappers and test wrappers are present but not directly executable, `freely ai --help` emits shell errors before usage text, and at least one auth-change wake regression test behaves inconsistently across worktrees.
- why_now:
  - the repo is explicitly CLI-first, so “command requires `bash <script>` to run” is a packaging defect, not a cosmetic issue
  - unstable test wrappers weaken confidence in later develop-bound gating
  - these defects are independent from runtime semantics and should be fixable with a narrow packaging / regression owner
- acceptance_criteria:
  - documented `bin/` entrypoints that are meant to be runnable are directly executable from the shell
  - `freely ai --help` prints clean help text without stray shell evaluation errors
  - `test-ai-cli-switch-triggers-auth-change-wake` is deterministic across equivalent worktrees, or its environment contract is explicitly tightened and enforced
- promotion_gate:
  - distinguish genuine CLI wrappers from internal libraries before changing executable bits broadly
  - keep this owner on packaging, command surface, and deterministic regression coverage
- next_action: materialize the packaging-focused owner under `workspace-routing-foundation`, then repair the broken runnable wrapper set, clean the `freely ai --help` surface, and stabilize the auth-change wake regression coverage.
- revisit_trigger: newly added `bin/` wrappers ship without executable permission or audited regression commands remain shell-noisy / worktree-sensitive.

## C-20260405T235800Z-A: legacy issue

- candidate_format_version: `v2`
- title: CLI help and dry-run contract followthrough after canonical audit
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/human/cli-help-and-dry-run-contract-followthrough-governance/issues/cli-help-and-dry-run-contract-followthrough-governance.md`
- promoted_issue_id: `I-20260405T235800Z-D`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: canonical CLI surface replay still exposes a narrow but real contract gap beyond the already-completed wrapper-packaging owner. `wt-create --help` misroutes into branch creation instead of a safe help path, `wt-enter --help` and `wt-add --help` do not expose a standard help contract, `pr-merge-guarded --help` prints usage but exits non-zero, and `ai switch codex --dry-run --format json` can return `No slots found or all probing failed` even while `whoami/status` prove an active apikey slot exists.
- why_now:
  - these are first-hop command-surface contracts in a CLI-first product, so help and dry-run semantics are part of the product behavior, not operator trivia
  - `wt-create --help` is not just noisy; it currently attempts the creation path and therefore carries avoidable side-effect risk
  - the affected commands span workspace helpers, guarded merge tooling, and ai switching, so the remaining gap is broader than one single wrapper but still much narrower than runtime/control-plane lifecycle work
- acceptance_criteria:
  - `wt-create --help`, `wt-enter --help`, `wt-add --help`, and `pr-merge-guarded --help` all expose explicit, side-effect-free help behavior with success exit codes where the command is only asking for usage
  - the root `freely` command exposes a deliberate top-level help/usage contract instead of relying on ambiguous “missing command” behavior
  - `ai switch codex --dry-run --format json` reports a stable, machine-consumable result that remains consistent with `ai list` / `whoami` / `status` when saved apikey slots exist
- promotion_gate:
  - keep this owner on command-surface ergonomics, help/usage/exit-code semantics, and ai dry-run contract alignment
  - do not absorb fresh-project bootstrap, runtime supervision, or generic executable-bit packaging work
- next_action: This candidate is now materialized as `I-20260405T235800Z-D`. Keep the owner narrow: make the audited help paths explicit and side-effect free, pin their success/exit semantics with focused regressions, and make `ai switch codex --dry-run --format json` emit one stable machine-readable result without reopening runtime/auth lifecycle work.
- revisit_trigger: canonical CLI replay still shows help invocations with side effects/non-zero-only usage paths, or `ai switch --dry-run` remains inconsistent with the saved-slot inventory.
