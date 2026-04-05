# Verification: agents-cli-output-style-experiment-governance

- issue_id: `I-20260405-cli-output-style-A`
- reviewer: `codex`
- date: `2026-04-04`
- disposition: `pass_for_verification`

## Scope

Verify the narrow owner that records the current CLI/chat output-style experiment in `AGENTS.md`, while also documenting the already-existing project-level `AGENTS.md` generation/consumption contract without promoting a new Freely capability.

## Checks

1. Confirmed `AGENTS.md` now carries a dedicated experimental section for developer-facing CLI/chat output.
2. Confirmed the section keeps concise plain Chinese as the default and does not adopt classical Chinese.
3. Confirmed `AGENTS.md` now states that project-level `AGENTS.md` is the first governance surface, that Freely init/runtime already ensure a minimal file for managed projects, and that self-hosting follows the same rule.
4. Confirmed `docs/system/workspace/scripts/runtime/freely` contains `ensure_project_agents_md()`, and `docs/system/workspace/scripts/tests/test-freely-init-cc-config` asserts that `freely init` creates `AGENTS.md`.
5. Confirmed the pre-brainstorm and candidate truth say this remains an `AGENTS.md` experiment plus generated-AGENTS contract clarification instead of a new capability materialization.
6. Ran:
   - `./bin/governance-check`

## Result

- pass: the output-style change is now carried by a concrete owner issue instead of candidate-only evidence
- pass: the experiment remains bounded to `AGENTS.md` and developer-facing output
- pass: the owner now explicitly states how Freely already generates/consumes project-level `AGENTS.md`, including self-hosting
- pass: governance writeback is consistent enough for develop-bound replay

## Residual Risk

- The experiment is intentionally heuristic. If future dogfooding shows the wording is still too verbose or too restrictive, or that generated-AGENTS management needs stronger product truth, it should reopen as another narrow follow-on rather than silently expanding into runtime/capability truth.
