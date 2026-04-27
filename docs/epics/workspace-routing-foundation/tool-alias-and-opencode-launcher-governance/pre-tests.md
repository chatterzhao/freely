# Pre-Tests: tool-alias-and-opencode-launcher-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `opencode direct launcher + alias resolution`
- testing layer: `integration + manual foreground`
- target environment: `feature worktree`
- required evidence: `syntax check, launch verification, session ID extraction, alias resolution`
- blocker taxonomy:
  - `definition_missing`
  - `commands_only`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

## Unit
- acceptance target: `opencode launcher case and alias resolver`
- testing layer: `syntax validation`
- target environment: `feature worktree`
- required evidence: `bash -n pass on all modified files`
- blocker taxonomy: `execution_pending_or_failed`
- evidence_summary: `All modified files pass bash -n: tool-launchers.sh, monitor-ai-cli.sh, freely, start-lead-agent.sh.`

## Integration
- acceptance target: `opencode direct adapter launch and ccds alias resolution in daemon`
- testing layer: `runtime integration daemon`
- target environment: `feature worktree daemon`
- required evidence: `daemon start, ai_launch_begin with tool=opencode, alias resolution log`
- blocker taxonomy: `execution_pending_or_failed`
- evidence_summary: `Daemon start with AI_TOOL=opencode: lifecycle trace records ai_launch_begin with tool=opencode tool_adapter=direct. ccds alias resolution: zsh -ic returns claude --settings path, binary detection enters cc family.`

## End-to-End
- acceptance target: `full daemon lifecycle with opencode and ccds`
- testing layer: `end-to-end daemon`
- target environment: `real macOS host`
- required evidence: `complete lifecycle from supervisor start to ai_cycle_finished`
- blocker taxonomy: `execution_pending_or_failed`
- evidence_summary: `Full daemon cycle: supervisor_started -> prompt build -> ai_launch_begin (tool=opencode/ccds) -> model response -> ai_cycle_finished. Session IDs captured.`

## Real-Environment
- acceptance target: `real macOS host with opencode v1.14.26 and ccds alias`
- testing layer: `real-environment daemon`
- target environment: `macOS Darwin 25.3`
- required evidence: `real AI model call, real session tracking, real alias resolution`
- blocker taxonomy: `execution_pending_or_failed`
- real_environment_status: pass
- real_environment_reason: `Tested on real macOS host. opencode with deepseek-v4-pro: session ID ses_233722117ffeOuUkPrDjl06elo captured. ccds alias resolved correctly via zsh -ic. deepseek-v4-pro confirmed working via ccds --resume session test.`

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `opencode launches via direct adapter in auto mode`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `cli`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-1`
- case_design: `Set AI_TOOL=opencode, AI_MODE=auto. Verify daemon start launches opencode with --dangerously-skip-permissions.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`

### PT-2
- id: `PT-2`
- requirement: `opencode session ID extracted from --print-logs output`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `cli`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-2`
- case_design: `Launch opencode, verify monitor extracts ses_* session ID from output.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`

### PT-3
- id: `PT-3`
- requirement: `AI_TOOL=ccds alias resolves to claude binary via zsh -ic`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `cli`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-3`
- case_design: `Set AI_TOOL=ccds. Verify alias resolves to claude --settings ~/.claude/settings_deepseek.json, enters cc family.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`

### PT-4
- id: `PT-4`
- requirement: `AI_TOOL_EXTRA_ARGS injected into tool launch command`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `cli`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-4`
- case_design: `Set AI_TOOL_EXTRA_ARGS with custom flag. Verify flag appears in exec line before freely-managed flags.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`
