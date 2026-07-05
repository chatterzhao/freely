# Issue: manager-bootstrap-prompt-publication-without-continuity-materialization-governance

- issue_id: `I-20260404-1405-A`
- title: Manager bootstrap prompt publication without continuity materialization governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-bootstrap-prompt-publication-without-continuity-materialization-governance`
- issue-name: `manager-bootstrap-prompt-publication-without-continuity-materialization-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260404/candidates.md#c-20260404-1405-a`
- source_brainstorm: `docs/B1-docs/raw-20260404/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/code-reviews`
- depends_on: `docs/B2-docs/ibm/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Current canonical `develop` can reach manager prompt publication during `freely start`, but the control plane was not yet truthful end-to-end. The first replay exposed a bootstrap race where the watchdog restarted a fresh supervisor before `ai.pid` appeared. After that bounded grace fix, the next replay proved continuity artifacts were being written, but the manager/runtime handoff still misreported `latest_manager_worker_prompts_generated=none` because the current continuity format recorded the delegated prompt under `## Worker Dispatch`, which the runtime parser did not treat as a launchable worker prompt section.

## Scope

1. Freeze the exact bootstrap path from dispatcher-ready to prompt publication, continuity materialization, worker handoff parsing, and steady-state runtime survival.
2. Distinguish explicit stop semantics from internal early-exit and recovery-driven stop paths during startup.
3. Repair the prompt-publication-to-continuity contract so fresh manager startup either publishes durable continuity plus launchable worker-prompt truth, or records a bounded failure artifact with the right reason.
4. Align `live-status`, runtime events, and prompt/continuity artifacts so they expose the true boundary instead of hiding launchable prompts behind an unparsed continuity section.

## Acceptance

- `freely start` on canonical `develop` no longer stops during bootstrap before the first AI launch solely because `ai.pid` has not appeared yet.
- when a manager continuity writes a delegated prompt under the current `## Worker Dispatch` contract, runtime parsing and status surfaces recognize it as a launchable worker prompt instead of reporting `none`.
- `live-status` differentiates human/operator stop from bootstrap/control-plane failure.
- runtime events and prompt/continuity artifacts are sufficient to explain whether the manager actually launched, wrote continuity, surfaced launchable worker prompts, consumed continuity, or exited before ownership transfer.
- the lane remains focused on manager bootstrap and continuity materialization, not broader watchdog or unrelated supervision redesign.

## Verification

- `freely live-status --project <project-root>`
- `freely start --project <project-root>`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- inspect `.freely/logs/runtime-events.log`
- inspect `.freely/run/prompt-*.txt` and latest manager continuity artifacts

## Next

- `2026-04-04` closeout: canonical `develop` already absorbed the runtime fix through merge `8d29609`, and this closeout lane only writes back completed lifecycle truth.
- Keep this owner closed as the bounded bootstrap-and-worker-dispatch materialization record; future restart churn or auth-slot instability must reopen as a new owner on current `develop`.
