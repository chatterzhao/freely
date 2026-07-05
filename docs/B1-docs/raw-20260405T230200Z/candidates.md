# Candidates - 20260405-2302--worktree-helper-shell-source-compatibility

### C-20260405T230200Z-A: legacy issue

- candidate_format_version: `v2`
- title: Worktree helper shell source compatibility governance
- problem: Freely documents `source ./bin/wt-add ...` and `source ./bin/wt-enter ...` as standard helper entrypoints, but the actual `bin/` wrappers break in the default `zsh` context because they depend on `BASH_SOURCE`. The current regression suite only tests internal worktree scripts, so the user-facing CLI path can fail while tests stay green.
- why_now:
  - this is a real dogfood failure on the documented CLI path, not a hypothetical shell preference edge case
  - the repo is explicitly CLI-first, so a broken documented command path is capability drift
  - the fix surface is narrow and testable: wrapper source-safety plus command-path regression coverage
- acceptance_criteria:
  - `source ./bin/wt-add ...` works from default `zsh` and still preserves current protection behavior
  - `source ./bin/wt-enter ...` works from default `zsh` and still enters the expected worktree path
  - focused regressions exercise the actual `bin/` wrappers instead of only the internal worktree scripts
  - the owner remains a narrow follow-on of the completed worktree helper/tooling family rather than a new umbrella worktree redesign
- promotion_gate:
  - prove the failure is on the documented wrapper path, not only an ad hoc shell invocation pattern
  - keep the change bounded to helper shell compatibility and test coverage
  - prove current tests missed the bug because they bypassed the `bin/` wrappers
- open_questions:
  - whether the narrowest fix should make the `bin/` wrappers shell-agnostic themselves or route through a different source-safe indirection
  - whether additional sourced `bin/` wrappers share the same bug and need to be absorbed in the same narrow owner
- acceptance_reviews:
  - reviewer: `governance-initial-review`
    verdict: `supports`
    note: the bug is a concrete CLI-first contract failure on documented commands and merits a dedicated follow-on owner.
  - reviewer: `testing-surface-review`
    verdict: `supports`
    note: current tests cover the wrong entrypoint and should be widened to the documented wrapper path.
  - reviewer: `scope-boundary-review`
    verdict: `supports`
    note: this should stay a narrow helper/wrapper shell-compat slice rather than reopening worktree bootstrap as an umbrella.
- decision_reason:
  - a documented CLI path is currently broken in the default shell context
  - the missing regression is now known and easy to reproduce
  - absorbing this into an already-completed owner would blur closeout truth instead of recording a new regression-driven follow-on
- priority: `P1`
- status: `promoted`
- milestone: `M-20260326-freely-product-architecture`
- source_brainstorm: `docs/B1-docs/raw-20260405-2302/brainstorms.md`
- promoted_issue_id: `I-20260405T230200Z-A`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/worktree-helper-shell-source-compatibility-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialize this candidate as a narrow develop-bound owner
  - implement the shell-safe wrapper fix and focused wrapper-path regressions in the same lane
- revisit_trigger:
  - documented `wt-add` / `wt-enter` source commands regress again on canonical `develop`
  - future work proposes a broader wrapper framework without first preserving this narrow command contract
