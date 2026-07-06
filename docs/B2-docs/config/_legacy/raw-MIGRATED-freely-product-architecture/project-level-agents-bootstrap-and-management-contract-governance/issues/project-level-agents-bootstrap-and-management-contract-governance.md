# Issue: project-level-agents-bootstrap-and-management-contract-governance

- issue_id: `I-20260405-1130-A`
- title: Project-level AGENTS bootstrap and management contract governance
- phase_state: `completed`
- milestone: `M-20260326-freely-product-architecture`
- epic-name: `freely-product-architecture`
- story-name: `project-level-agents-bootstrap-and-management-contract-governance`
- issue-name: `project-level-agents-bootstrap-and-management-contract-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260405T230200Z/candidates.md#c-20260405-1130-a`
- source_brainstorm: `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/packaging/raw-20260402-0403pre-tests.md`
- progress_path: `docs/progress/freely-product-architecture/p-project-level-agents-bootstrap-and-management-contract-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews`
- depends_on:
  - `docs/B2-docs/config/packaging/raw-20260402-0403issues/agents-cli-output-style-experiment-governance.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/start-lead-agent.sh`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely already behaves as if project-root `AGENTS.md` were a formal product contract:

1. `freely init` creates a minimal project-level `AGENTS.md` when missing.
2. runtime and lead-agent prompts read the project root `AGENTS.md` first.
3. self-hosting Freely follows the same pattern.

But that behavior has been scattered across runtime code, tests, and high-level guidance rather than frozen as a reusable capability contract. The missing contract leaves four important boundaries implicit:

1. existing project-owned `AGENTS.md` should be preserved
2. the generated default template is not the same layer as this repo's hand-maintained `AGENTS.md`
3. workspace capability docs come after the project entrypoint rather than replacing it
4. self-hosting uses the same project-level contract instead of a special-case path

## Scope

1. Freeze a reusable capability doc for project-level `AGENTS.md` bootstrap, read-order, preservation, and self-hosting semantics.
2. Add a focused regression proving `freely init` preserves an existing project-owned `AGENTS.md`.
3. Clarify the layer split between:
   - generated minimal project entrypoint
   - project-owned customized `AGENTS.md`
   - reusable Freely capability truth under `docs/system/workspace/**`
4. Keep the first slice narrow and documentation-first; do not redesign template customization or migration flow.

## Non-Goals

1. Do not introduce richer generated templates or project-specific prompt synthesis.
2. Do not add merge/diff/update workflows for existing `AGENTS.md`.
3. Do not rewrite current root `AGENTS.md` governance into capability docs.
4. Do not change runtime behavior beyond freezing the existing preserve-existing contract with tests and docs.

## Acceptance

1. `docs/system/workspace/**` contains a formal capability doc for project-level `AGENTS.md` bootstrap and management semantics.
2. The contract states that `freely init` only creates `AGENTS.md` when missing and preserves an existing file.
3. The contract states that runtime reads `<project-root>/AGENTS.md` before reusable workspace capability docs.
4. The contract states that self-hosting Freely uses the same project-level entrypoint rule.
5. A focused regression proves `freely init` preserves an existing project-owned `AGENTS.md`.
6. The lifecycle writeback is lawful for a `develop` replay.

## Completion

- `docs/B1-docs/raw-20260405T230200Z/brainstorms.md`
- `docs/B1-docs/raw-20260405T230200Z/candidates.md`
- `docs/milestones.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403issues/project-level-agents-bootstrap-and-management-contract-governance.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403brainstorms/b-project-level-agents-bootstrap-and-management-contract-governance.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403prd.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403pre-tests.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403tasks.md`
- `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-governance-verification.md`
- `docs/progress/freely-product-architecture/p-project-level-agents-bootstrap-and-management-contract-governance.md`
- `docs/system/workspace/README.md`
- `docs/system/workspace/project-agents-contract.md`
- `docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-init-preserves-existing-agents-md`
- `bash docs/system/workspace/scripts/tests/test-freely-init-cc-config`
- `bash docs/system/workspace/scripts/tests/test-freely-init-ai-default-precedence`
- `./bin/governance-check`

## Next

- Completed on canonical `develop` with closeout verification recorded in `docs/B2-docs/config/packaging/raw-20260402-0403code-reviews/20260405-project-level-agents-bootstrap-and-management-contract-canonical-closeout-verification.md`.
- Reopen only if canonical `develop` regresses the project-level `AGENTS.md` preservation contract or stops treating the project root entrypoint as authoritative before reusable workspace capability docs.
