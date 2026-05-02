# Pre-Tests: freely-tool-autonomy-policy-materialization-governance

## Story-Level Acceptance Items

1. `id: materialization-layering-contract`
- requirement: issue artifacts clearly distinguish Freely canonical policy, tool adapter injection, and tool-local config materialization
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/issues/freely-tool-autonomy-policy-materialization-governance.md`

2. `id: current-split-reproduced`
- requirement: issue artifacts reproduce the current split between launcher/tool-doc auto posture and guarded project Codex config
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/brainstorms/b-freely-tool-autonomy-policy-materialization-governance.md`

3. `id: manual-only-home-config-guidance`
- requirement: issue artifacts clearly state that user-global tool config remains manual-only by default
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/prd.md`

4. `id: acp-not-blocker`
- requirement: issue artifacts clearly state ACP is an optional adapter follow-up and not a prerequisite for materializing this owner
- evidence_level: `doc-read`
- status: `done`
- artifact_ref: `docs/epics/freely-product-architecture/freely-tool-autonomy-policy-materialization-governance/prd.md`

## Acceptance Items

### codex-project-local-auto-approval
- id: `codex-project-local-auto-approval`
- requirement: project-local Codex config materialization follows Freely auto posture by writing approval_policy equals never when the project is initialized in auto mode
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-init-codex-project-config-force`

### codex-launcher-auto-posture
- id: `codex-launcher-auto-posture`
- requirement: Codex launch-time materialization still makes the non-interactive auto posture explicit in launcher truth
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-monitor-ai-cli-codex-args`

### claude-launcher-auto-posture
- id: `claude-launcher-auto-posture`
- requirement: Claude Code launch-time materialization remains explicit and consistent with the documented non-interactive auto posture
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-monitor-ai-cli-cc-args`

## Pre-merge Focused Regression / Smoke

1. environment:
   - feature worktree
2. required evidence:
  - `./bin/governance-check`
  - wording readback across issue / brainstorm / prd / pre-tests / tasks stays consistent
  - focused implementation evidence for the first project-local Codex materialization slice
  - focused launcher/doc readback evidence for Codex and Claude Code profile auto posture
3. failure signal:
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
4. failure handling / replay expectation:
  - repair the issue-bound artifacts before claiming materialization is complete
5. current verification result:
  - `./bin/governance-check` passes in this feature worktree
  - `test-monitor-ai-cli-codex-args` passes
  - `test-monitor-ai-cli-cc-args` passes
