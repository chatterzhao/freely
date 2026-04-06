# Candidates - 20260405-2358--cli-command-audit-regressions

## C-20260405-2358-A

- candidate_format_version: `v2`
- title: Project-targeted CLI bootstrap and status scoping audit
- status: `proposed`
- milestone: `pending://milestone-binding`
- promoted_issue_path: `pending://issue-materialization`
- promoted_issue_id: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: project-targeted CLI surfaces do not consistently honor the passed `--project` boundary. `baseline-status` / `status` drift their baseline project display back to the repo root, `sync-tooling` leaves `freely init` unable to enable hooks because `.githooks` is missing, and `ensure-interruption-dispatch` emits raw filesystem errors when the intake tree is absent.
- why_now:
  - these are first-hop setup and observability commands, so wrong project identity or broken bootstrap contaminates all later testing
  - the failures were reproduced both on a feature worktree and on a fresh temporary repo, so they are not tied to one dirty local lane
  - the fix surface is narrow enough to keep separate from runtime restart semantics
- acceptance_criteria:
  - `freely baseline-status --project <x>` and `freely status --project <x>` report baseline metadata for `<x>`, not the repository root
  - `freely sync-tooling` materializes the hook assets needed for a subsequent `freely init`, or `freely init` degrades with a precise contract instead of failing on missing `.githooks`
  - `freely ensure-interruption-dispatch` handles a missing intake directory without raw `find` noise and with an explicit semantic result
- promotion_gate:
  - keep this owner scoped to project targeting, bootstrap, and status/intake preflight contracts
  - do not absorb runtime supervision churn or intake counter reconciliation here
- next_action: decide whether `.githooks` should be copied by `sync-tooling`, synthesized by `init`, or both; then materialize a narrow owner.
- revisit_trigger: another project-targeted CLI command is shown to ignore `--project` or fresh-project bootstrap still requires manual hook copying.

## C-20260405-2358-B

- candidate_format_version: `v2`
- title: Runtime control-plane CLI stability after full command audit
- status: `proposed`
- milestone: `pending://milestone-binding`
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
- next_action: separate “stale pid / readiness / restart” evidence from “intake status / chat completion” evidence and confirm whether they belong in one supervision owner or two adjacent ones.
- revisit_trigger: any audited runtime command still requires manual cleanup of stale children or reports contradictory intake state on canonical develop.

## C-20260405-2358-C

- candidate_format_version: `v2`
- title: CLI wrapper packaging and regression-surface audit
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/cli-wrapper-packaging-and-regression-surface-governance/issues/cli-wrapper-packaging-and-regression-surface-governance.md`
- promoted_issue_id: `I-20260405-2358-C`
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
