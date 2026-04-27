# Pre-Tests: tool-alias-and-opencode-launcher-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `opencode direct launcher + AI_TOOL alias resolution`
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
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The opencode case and alias resolver are shell functions without isolatable unit boundaries. bash -n is the appropriate validation at this layer.`
- replacement_evidence: `All modified files pass bash -n syntax check: tool-launchers.sh, monitor-ai-cli.sh, freely, start-lead-agent.sh.`

## Integration
- acceptance target: `opencode direct adapter launch and ccds alias resolution in daemon`
- testing layer: `runtime integration daemon`
- target environment: `feature worktree daemon`
- required evidence: `daemon start, ai_launch_begin event, alias resolution log`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `Integration validation is through real daemon lifecycle observation, not isolated integration tests. PT items 1-4 cover the integration surface.`
- replacement_evidence: `Daemon start recorded ai_launch_begin with tool=opencode, tool_adapter=direct. ccds alias resolved via zsh -ic to claude binary.`

## End-to-End
- acceptance target: `full daemon lifecycle with opencode and ccds alias`
- testing layer: `end-to-end daemon`
- target environment: `real macOS host`
- required evidence: `supervisor start to ai_cycle_finished, session ID capture, model response`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `covered_by_more_realistic_required_surface`
- not_applicable_explanation: `E2E is validated by the Real-Environment section below, which runs on the real macOS host with the same daemon lifecycle.`
- replacement_evidence: `Real-Environment section documents the full daemon cycle on macOS Darwin 25.3.`

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
- surface_kind: `integration`
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
- surface_kind: `integration`
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
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-3`
- case_design: `Set AI_TOOL=ccds. Verify alias resolves to claude --settings path, enters cc family.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`

### PT-4
- id: `PT-4`
- requirement: `AI_TOOL_EXTRA_ARGS injected into tool launch command`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-4`
- case_design: `Set AI_TOOL_EXTRA_ARGS with custom flag. Verify flag appears in exec line before freely-managed flags.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-tool-alias-opencode-premerge-verification.md`

### PT-5
- id: `PT-5`
- requirement: `AGENTS.md break-glass guidance hardened`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-5`
- case_design: `Verify AGENTS.md line 114 explicitly lists forbidden break-glass patterns and narrowed verified_false_negative.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-break-glass-agents-guidance-hardening.md`

### PT-7
- id: `PT-7`
- requirement: `IBM Framework documentation unified across all active governance docs`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-7`
- case_design: `Verify ibm-framework.md defines B1_IBM/B2_IBM, all active docs (AGENTS.md, CONSTITUTION, three-loop, LAWS, skills, agents) use unified terminology, terminology table maps old→new.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260426-ibm-framework-docs.md`
