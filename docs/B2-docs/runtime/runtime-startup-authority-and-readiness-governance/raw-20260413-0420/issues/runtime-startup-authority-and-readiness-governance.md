# Issue: runtime-startup-authority-and-readiness-governance

- issue_id: `I-20260413-0420-A`
- title: `Runtime startup authority and readiness governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-startup-authority-and-readiness-governance`
- issue-name: `runtime-startup-authority-and-readiness-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260413T020800Z/candidates.md#c-20260413-0420-a`
- source_brainstorm: `docs/B1-docs/raw-20260413T020800Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260413-0420/verification/pre-tests.md
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-startup-authority-and-readiness-governance.md`
- verification_artifact_dir: docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260413-0420/code-reviews
- created_at: `2026-04-13`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` still let startup truth drift behind PID heuristics:

1. supervisor identity was inferred from argv resemblance instead of runtime-published authority
2. `daemon start` treated "some supervisor-looking pid exists" as ready
3. the same-project start lock was released before startup truth was durably published
4. stop cleanup and stop-marker retention could still be influenced by ghost or fake supervisor hints

The root-cause packet is already canonically split. This owner is the bounded execution lane that turns the startup-authority half into runtime truth and focused regressions.

## Scope

1. Introduce authoritative startup identity truth for project supervisors.
2. Make supervisor validation depend on runtime-published authority rather than argv resemblance.
3. Delay same-project start-lock release until startup truth is published.
4. Make `daemon start` ready semantics depend on current-launch startup truth.
5. Keep stop followthrough and stop-marker preservation aligned with authoritative supervisor truth.
6. Add focused regressions for fake-supervisor rejection and daemon-ready truth.

## Non-Goals

1. Do not redesign the manager startup continuity contract in this owner.
2. Do not widen into a general runtime state-machine rewrite beyond the bounded authority/readiness seam.
3. Do not reopen foreground-versus-daemon entrypoint semantics that were already frozen by `I-20260413-0208-A`.
4. Do not claim manager-ready semantics are solved just because startup authority is now explicit.

## Acceptance

1. Runtime publishes authoritative startup identity for the active supervisor instead of trusting argv resemblance.
2. Fake argv or ghost processes do not validate as project supervisors.
3. Same-project startup does not expose an attach/repair window before startup truth is published.
4. `daemon start` returns running only after the current launch has published startup truth.
5. Stop followthrough and stop-marker cleanup only retain stop state when another authoritative supervisor still exists.
6. Focused regressions plus adjacent runtime command/status regressions remain green.

## IBM Handoff

- implementation_scope_summary:
  - Introduce a runtime-owned supervisor identity surface, route readiness through that surface, and tighten stop/cleanup to the same authority model.
  - Keep the launch model bounded to startup identity and readiness. Leave manager continuity and wider phase modeling to the follow-on owner.
- required_doc_refs:
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zissues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zbrainstorms/b-runtime-startup-authority-and-readiness-governance.md`
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zprd.md`
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zpre-tests.md`
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Ztasks.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/tests/test-freely-fake-supervisor-argv-does-not-validate`
  - `docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`
  - `docs/system/workspace/scripts/tests/test-freely-start-serializes-same-project-concurrent-starts`
  - `docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
  - `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`

## Verification

- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-implementation-decision.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-verification.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-closeout-verification.md`
- `bash docs/system/workspace/scripts/tests/test-freely-fake-supervisor-argv-does-not-validate`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`
- `bash docs/system/workspace/scripts/tests/test-freely-start-serializes-same-project-concurrent-starts`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `./bin/governance-check`
- `git diff --check`

## Completion

- `docs/B1-docs/raw-20260413T020800Z/candidates.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zissues/runtime-startup-authority-and-readiness-governance.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zbrainstorms/b-runtime-startup-authority-and-readiness-governance.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zprd.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zpre-tests.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Ztasks.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-implementation-decision.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-verification.md`
- `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/raw-20260705T061416Zcode-reviews/20260413-runtime-startup-authority-and-readiness-closeout-verification.md`
- `docs/progress/workspace-routing-foundation/p-runtime-startup-authority-and-readiness-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `docs/system/workspace/scripts/tests/test-freely-fake-supervisor-argv-does-not-validate`
- `docs/system/workspace/scripts/tests/test-freely-daemon-start-ignores-fake-supervisor-argv`

## Next

- This owner should remain closed once canonical `develop` carries authoritative startup identity, daemon-ready truth, and fake-supervisor rejection.
- Reopen only if later runtime work regresses authority publication timing, daemon ready truth, or stop cleanup back toward pid/argv heuristics.
