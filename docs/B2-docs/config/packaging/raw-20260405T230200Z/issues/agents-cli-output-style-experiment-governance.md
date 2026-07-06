# Issue: agents-cli-output-style-experiment-governance

- issue_id: `I-20260405-cli-output-style-A`
- title: AGENTS project entry and output style governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `agents-cli-output-style-experiment-governance`
- issue-name: `agents-cli-output-style-experiment-governance`
- priority: P2
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-cli-output-style`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/config/packaging/raw-20260405T230200Z/verification/pre-tests.md
- progress_path: `docs/progress/freely-product-architecture/p-agents-cli-output-style-experiment-governance.md`
- verification_artifact_dir: docs/B2-docs/config/packaging/raw-20260405T230200Z/code-reviews
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The current discussion is no longer a generic token-efficiency research question. The chosen scope is narrower:

1. keep the output-style experiment inside `AGENTS.md`
2. constrain it to developer-facing CLI/chat responses while building Freely
3. avoid promoting it into `docs/system/**`, `bin/**`, `src/**`, or other capability truth

The same review also confirms an existing Freely capability boundary that matters for self-hosting: runtime/init already ensure a minimal project-level `AGENTS.md`, and execution reads the target project's `AGENTS.md` before falling through to reusable Freely capability docs.

That makes this a product-architecture/developer-entrypoint governance writeback aligned with an existing capability fact, not a new reusable capability lifecycle.

## Scope

1. Record the experiment as an `AGENTS.md` entrypoint rule for developer-facing CLI/chat output.
2. Keep the rule on concise plain Chinese rather than classical Chinese.
3. Clarify in `AGENTS.md` how project-level `AGENTS.md` generation/consumption currently works for managed projects and for Freely self-hosting.
4. Keep the experiment explicitly outside Freely capability directories and runtime truth, while pointing at the already-existing runtime capability boundary.
5. Write back the matching pre-brainstorm, candidate, milestone, progress, and verification artifacts required for a lawful `develop` merge.

## Non-Goals

1. Do not define a new Freely runtime/agent/skill/CLI capability.
2. Do not widen into tokenizer benchmarking or generalized token-efficiency infrastructure.
3. Do not rewrite `PROJECT_INTENT`, `CONSTITUTION`, or `LAWS` for this experiment.
4. Do not silently redefine the runtime template for generated project `AGENTS.md`; only document the current contract and self-hosting implication.
5. Do not impose this style on product-facing runtime output beyond the current developer-facing experiment boundary.

## Acceptance

1. `AGENTS.md` contains a clear experimental output-style section that:
   - uses concise plain Chinese
   - rejects classical Chinese as the default
   - preserves precision for commands, paths, status words, and evidence
2. `AGENTS.md` now also states that Freely-managed projects treat project-root `AGENTS.md` as the first governance surface, and that self-hosting Freely follows the same rule.
3. The pre-brainstorm and candidate truth say this remains an `AGENTS.md`-only experiment rather than a new capability materialization, while acknowledging the existing generated-AGENTS capability.
4. The milestone records a concrete owner issue instead of leaving the change as candidate-only evidence.
5. `./bin/governance-check` passes in the source feature worktree.

## Completion

- `AGENTS.md`
- `docs/B1-docs/raw-INDEX.md`
- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Zissues/agents-cli-output-style-experiment-governance.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Zbrainstorms/b-agents-cli-output-style-experiment-governance.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Zprd.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Zpre-tests.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Ztasks.md`
- `docs/B2-docs/config/packaging/raw-20260405T230200Zcode-reviews/20260405-agents-cli-output-style-experiment-governance-verification.md`
- `docs/progress/freely-product-architecture/p-agents-cli-output-style-experiment-governance.md`

## Verification

- `./bin/governance-check`
- review `docs/system/workspace/scripts/runtime/freely` and existing init tests for the current generated-AGENTS contract

## Next

- Completed on canonical `develop` with closeout verification recorded in `docs/B2-docs/config/packaging/raw-20260405T230200Zcode-reviews/20260405-agents-cli-output-style-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` stops treating this as an `AGENTS.md`-only experiment or if project-level `AGENTS.md` entrypoint truth needs stronger capability-level materialization.
