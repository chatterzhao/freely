# Issue: runtime-startup-authority-and-readiness-governance

- issue_id: `I-20260413-0420-A`
- title: `Runtime startup authority and readiness governance`
- phase_state: `in_ibm`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-startup-authority-and-readiness-governance`
- issue-name: `runtime-startup-authority-and-readiness-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/candidates.md#c-20260413-0420-a`
- source_brainstorm: `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-startup-authority-and-readiness-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- created_at: `2026-04-13`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Canonical `develop` still has a live startup-authority defect across both foreground and daemon entrypoints:

1. supervisor identity is inferred from argv or cwd resemblance instead of runtime-owned launch truth
2. the project start lock is released before durable startup truth is published
3. daemon ready is currently approximated as "there exists a PID that looks like a supervisor"
4. stop cleanup can preserve stop markers or repair state based on ghost or fake supervisors

This is not a request to reopen old owners wholesale. The completed owners in this area each closed a narrower boundary correctly:

- `I-20260408-0231-A` closed the earlier bounded concurrent-start and stop followthrough slice
- `I-20260413-0208-A` closed the foreground-versus-daemon entrypoint semantics freeze
- `I-20260407-0215-A` closed the bounded continuity-gap status surface

The remaining problem is a fresh bounded owner: Freely still lacks an authoritative launch model that both entrypoints can trust.

## Scope

1. Introduce an authoritative launch identity or equivalent startup truth owned by runtime rather than by process discovery heuristics.
2. Move startup readiness and attach or wait or repair decisions onto that launch truth.
3. Extend the project start critical section until startup truth is durably published for the current launch.
4. Redefine daemon ready to require current-launch startup truth instead of mere PID resemblance.
5. Prevent fake or ghost supervisors from validating as authoritative project runtime owners.
6. Keep stop-marker retention and stop cleanup aligned with validated launch ownership rather than argv-only discovery.
7. Add focused regressions plus one real-repo or equivalent high-fidelity replay proving the new authority model holds under dogfood conditions.

## Non-Goals

1. Do not redesign the manager continuity contract or force the final handoff shape in this owner.
2. Do not rename foreground or daemon command surfaces or reopen the entrypoint-semantics contract.
3. Do not widen into generic worker recovery, prompt wording policy, or unrelated watchdog redesign.
4. Do not claim that synthetic tests alone are sufficient evidence for daemon adequacy on canonical `develop`.

## Acceptance

1. A fake argv process no longer passes authoritative supervisor validation for the target project.
2. Same-project bootstrap produces exactly one authoritative launch during the bounded startup window.
3. Later starters attach, wait, or boundedly repair against current launch truth instead of guessing from a half-published `supervisor.pid`.
4. `daemon start` only reports ready after the current launch has published startup truth for that launch.
5. Stop cleanup preserves stop state only when another validated launch truly exists.
6. Verification includes a real-repo-shaped replay or equivalent high-fidelity fixture proving foreground and daemon both obey the same startup-authority model.

## IBM Handoff

- implementation_scope_summary:
  - This owner repairs the runtime's definition of startup authority and readiness across both foreground and daemon entrypoints.
  - It may touch startup identity publication, lock release boundary, attach or repair decision inputs, daemon ready semantics, and stop cleanup truth.
  - It must not absorb manager continuity contract redesign; that remains a follow-on boundary.
- required_doc_refs:
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/brainstorms/b-runtime-startup-authority-and-readiness-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/prd.md`
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/pre-tests.md`
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/tasks.md`
  - `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/brainstorms.md`
  - `docs/system/workspace/scripts/runtime/freely`

## Verification

- `bash -n docs/system/workspace/scripts/runtime/freely`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- add a focused fake-supervisor rejection regression
- add a focused current-launch-ready regression for daemon start
- add a focused bootstrap-publication-boundary regression
- capture one real-repo-shaped foreground or daemon replay proving the authority model under dogfood conditions
- `./bin/governance-check`
- `git diff --check`
