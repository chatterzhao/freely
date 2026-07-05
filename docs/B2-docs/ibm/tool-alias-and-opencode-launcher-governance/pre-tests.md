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

### PT-8
- id: `PT-8`
- requirement: `B1 intake→issue sync design complete and milestone issues synced to both platforms`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-8`
- case_design: `Verify 161 milestone issues synced to GitHub and Gitee with correct platform_ids. Verify gitee-issue.py API path fix.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-b1-intake-issue-sync-design.md`

### PT-9
- id: `PT-9`
- requirement: `tool_extra_args unbound variable fix does not break tool launching`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-9`
- case_design: `Verify bash -n passes. Verify tool launch with and without AI_TOOL_EXTRA_ARGS.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-tool-extra-args-unbound.md`

### PT-10
- id: `PT-10`
- requirement: `claude recognized in tool validation lists for alias resolution`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-10`
- case_design: `Verify start-lead-agent.sh and tool-launchers.sh include claude in validation lists.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-claude-tool-validation.md`

### PT-11
- id: `PT-11`
- requirement: `chat→issue migration writes to docs/issues/ and scan detects raw issues`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-11`
- case_design: `Verify write_intake_item creates docs/B1-docs/raw-*/issue.md. Verify scan_raw_issues returns raw issues.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-chat-intake-to-issue.md`

### PT-12
- id: `PT-12`
- requirement: `chat --issue appends comment, --urgent triggers signal for active issues`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-12`
- case_design: `Verify --issue appends ### comment to existing issue.md. Verify --urgent triggers signal for B2/dev/verification phases.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-chat-comment-append.md`

### PT-13
- id: `PT-13`
- requirement: `chat message with issue reference routes to that issue as comment`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-13`
- case_design: `Verify message with raw-xxx reference appends comment. Message without reference creates new raw issue.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-chat-routing-integration.md`


### PT-14
- id: `PT-14`
- requirement: `chat requires --issue or --new-issue for explicit intent`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-14`
- case_design: `Verify chat without flags errors. Verify --issue appends comment. Verify --new-issue creates raw issue.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-chat-explicit-flags.md`

### PT-15
- id: `PT-15`
- requirement: `chat usage text shows --issue and --new-issue flags`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-15`
- case_design: `Verify usage text includes --issue, --new-issue, --urgent.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-chat-usage-update.md`

### PT-16
- id: `PT-16`
- requirement: `governance-merge-gate enforces raw→C key chain for promoted candidates`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-16`
- case_design: `Verify gate errors when promoted candidate has no matching raw-* issue.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-gate-raw-c-keychain.md`

### PT-17
- id: `PT-17`
- requirement: `task-source-scan uses docs/issues/ exclusively`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-17`
- case_design: `Verify build_payload does not call scan_intake. Verify scan_raw_issues and scan_linked_issues are called.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-scan-clean-break.md`

### PT-19
- id: `PT-19`
- requirement: `intake functions marked as DEPRECATED`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-19`
- case_design: `Verify intake_dir_for_project and scan_intake have DEPRECATED comments.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-remaining-tasks.md`

### PT-20
- id: `PT-20`
- requirement: `GATE 6.2 checks platform_ids for linked issues in governance-merge-gate`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-20`
- case_design: `Verify gate errors when linked issue has no platform_ids in docs/issues/.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-final-gates.md`

### PT-21
- id: `PT-21`
- requirement: `interruption dispatch detects new raw issues in docs/issues/`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-21`
- case_design: `Verify ensure_interruption_dispatch_once scans docs/B1-docs/raw-* for unprocessed issues.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-b2-handler-bridge.md`

### PT-22
- id: `PT-22`
- requirement: `unknown tools pass start-lead-agent.sh validation for alias resolution`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-22`
- case_design: `Verify cc-ds-auto passes tool validation.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-alias-validation.md`

### PT-23
- id: `PT-23`
- requirement: `AI stall detection uses multi-signal liveness check`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-23`
- case_design: `Verify _ai_shows_liveness checks debug log mtime and process state before declaring AI stalled.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-ai-stall-liveness.md`

### PT-24
- id: `PT-24`
- requirement: `AI_RESUME_ON_RESTART=true prefers resume over fresh_with_handoff`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-24`
- case_design: `Verify select_launch_kind returns resume when AI_RESUME_ON_RESTART=true and evidence missing.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-resume-config.md`

### PT-25
- id: `PT-25`
- requirement: `AI_RESUME_ON_START skips fresh when session state exists`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-25`
- case_design: `Verify daemon start with AI_RESUME_ON_START=true and existing session state falls through to resume.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-resume-on-start.md`

### PT-26
- id: `PT-26`
- requirement: `session state persisted immediately for resume after SIGTERM`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-26`
- case_design: `Verify session-state.env written after ensure_runtime_tool_session_anchor. Verify cc session ID extraction from debug log.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-persist-session-early.md`

### PT-27
- id: `PT-27`
- requirement: `cc-ds-auto generates and persists Claude session ID`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-27`
- case_design: `Verify tool_uses_claude_session_id returns true for cc-ds-auto. Verify session-state.env written after launch.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-cc-ds-auto-session.md`

### PT-28
- id: `PT-28`
- requirement: `tool family auto-detected from alias resolution`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-28`
- case_design: `Verify cc-ds-auto resolves to claude family. Verify ccglm resolves to claude family. Verify codex resolves to codex.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-auto-detect-tool-family.md`

### PT-29
- id: `PT-29`
- requirement: `alias resolution works on zsh and bash`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-29`
- case_design: `Verify alias resolved on zsh. Verify bash fallback when $SHELL is bash.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-cross-shell-alias.md`

### PT-30
- id: `PT-30`
- requirement: `intake claim/resolve works with docs/issues/ raw-* IDs`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-30`
- case_design: `Verify claim updates frontmatter status. Verify resolve updates frontmatter. Verify legacy path still works.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-todo-cleanup-complete.md`

### PT-31
- id: `PT-31`
- requirement: `all TODO markers removed, CHG 2.2/4.2 migration verified`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-31`
- case_design: `Verify zero TODO CHG markers in runtime scripts. Verify intake claim/resolve/handler work with docs/issues/.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-todo-cleanup-complete.md`

### PT-32
- id: `PT-32`
- requirement: `file size guidelines in AGENTS.md, check script runs`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-32`
- case_design: `Verify AGENTS.md has file size section. Verify bin/check-file-size runs without errors.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-file-size-guidelines.md`

### PT-33
- id: `PT-33`
- requirement: `file size check configurable, skip markers work`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-33`
- case_design: `Verify FILE_SIZE_WARN/ERROR from config.env. Verify skip markers exclude files. Verify 0 errors.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-file-size-config.md`

### PT-34
- id: `PT-34`
- requirement: `file size check has TIP level for proactive refactoring hints`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-34`
- case_design: `Verify FILE_SIZE_TIP=300 default. Verify [TIP] output for files >300 lines. Verify tips counter in summary.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-file-size-tip.md`

### PT-35
- id: `PT-35`
- requirement: `skipped files are shown in check-file-size output with [SKIP] prefix`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-35`
- case_design: `Verify [SKIP] output for files with skip markers. Verify skips counter in summary. Verify no silent skips.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-file-size-skip-visible.md`

### PT-36
- id: `PT-36`
- requirement: `TIP renamed to DANGER, threshold 750 between WARN 500 and ERROR 1000`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-36`
- case_design: `Verify FILE_SIZE_DANGER=750 default. Verify [DANGER] output for files >750 lines. Verify check order: WARN → DANGER → ERROR.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-file-size-danger-rename.md`

### PT-37
- id: `PT-37`
- requirement: `parse_ai_spec passes through unknown tools for alias resolution`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-37`
- case_design: `Verify parse_ai_spec warns but does not exit on cc-ds-auto. Verify claude is in known list. Verify codex still works.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-parse-ai-spec-pass-through.md`

### PT-38
- id: `PT-38`
- requirement: `cmd_chat parses --issue/--new-issue/--urgent flags, defaults to --new-issue`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-38`
- case_design: `Verify cmd_chat --issue works. Verify --new-issue works. Verify --urgent flag is forwarded. Verify no-flag default to --new-issue.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-chat-issue-flags.md`

### PT-39
- id: `PT-39`
- requirement: `rc=1 normalized to 0 when debug log has clean SessionEnd`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-39`
- case_design: `Verify rc=1 with SessionEnd completed status 0 in debug log normalizes to ai_exit_rc_0. Verify rc=1 without SessionEnd stays ai_exit_rc_1.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-rc1-sessionend-normalize.md`

### PT-40
- id: `PT-40`
- requirement: `resume target extracted from debug log, CLAUDE_SESSION_ID_CURRENT fallback`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-40`
- case_design: `Verify session ID extracted from debug log. Verify main log fallback works. Verify CLAUDE_SESSION_ID_CURRENT fallback when both logs fail.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-resume-target-extraction.md`

### PT-41
- id: `PT-41`
- requirement: `worker prompt paths extracted from continuity files with AI-written section headers and prose format`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-41`
- case_design: `Verify "## Worker Prompt" (singular) + "See: /path" format extracts path. Verify "## Worker Prompts" (plural) + list format still works. Verify rg fallback works.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260427-fix-worker-prompt-extraction.md`

### PT-42
- id: `PT-42`
- requirement: `bin/issue-sync create/update/close/comment/promote works for raw and I-* issues on both platforms`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-42`
- case_design: `Verify issue-sync create writes platform_ids to frontmatter. Verify update pushes title/body/labels. Verify promote closes raw + creates I-* with cross-refs. Verify pr-merge-guarded triggers sync on changed issues.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-issue-platform-sync-architecture.md`

### PT-43
- id: `PT-43`
- requirement: `bin/issue-sync dedup prevents duplicate platform issue creation and update`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-43`
- case_design: `Verify create skips when platform_ids exist. Verify update skips when content hash unchanged. Verify scan shows none on first run. Verify batch only processes changed issues.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-issue-sync-dedup-scan-state.md`

### PT-44
- id: `PT-44`
- requirement: `resume circuit breaker prevents fresh-launch token waste loops`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-44`
- case_design: `Verify CLAUDE_SESSION_ID_CURRENT protected from empty overwrite. Verify JSONL fallback recovers session ID from tool directory. Verify circuit breaker trips after 3 fresh launches in 300s. Verify manager/worker session IDs are independent per worktree.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-claude-slug.md`


### PT-45
- id: `PT-45`
- requirement: `resume enforced on start/restart based on JSONL evidence; start allows fresh if no JSONL, restart never allows fresh`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-45`
- case_design: `Verify AI_RESUME_ON_START with JSONL files forces resume. Verify AI_RESUME_ON_START without JSONL allows one fresh. Verify AI_RESUME_ON_RESTART without JSONL hard-errors. Verify JSONL directory check is per-tool.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-claude-slug.md`


### PT-46
- id: `PT-46`
- requirement: `Claude session dir slug preserves leading - from absolute path`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-46`
- case_design: `Verify _tool_session_dir claude returns ~/.claude/projects/-Users-x-project (not Users-x-project). Verify find finds JSONL files in correct dir.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-claude-slug.md`


### PT-47
- id: `PT-47`
- requirement: `session state consistency: SESSION_PARENT_ID survives full lifecycle, anchor merge preserves non-anchor fields, fork launch kind supported`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-47`
- case_design: `Verify SESSION_PARENT_ID persisted across cycles. Verify anchor merge preserves FRESH_LAUNCH_COUNT. Verify fork launch kind produces --fork-session. Verify write_session_state includes SESSION_PARENT_ID.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fork-detection-startup.md`



### PT-48
- id: `PT-48`
- requirement: `fork detection on startup: SESSION_PARENT_ID set + no own session → fork from parent; manager injects parent session to worker`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-48`
- case_design: `Verify worker forks from parent when SESSION_PARENT_ID set. Verify fork generates child UUID while preserving parent ID. Verify fork passes --resume <parent> --fork-session --session-id <child>. Verify worker resume uses own ID after fork.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fork-detection-startup.md`



### PT-49
- id: `PT-49`
- requirement: `session-cache.sh module unified API for tool session operations`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-49`
- case_design: `Verify session_fork_args for Claude outputs correct flags. Verify session_resume_args for Claude. Verify session_fresh_args for Claude. Verify session_dir_for_tool returns correct paths for Claude/Codex/OpenCode. Verify fallback code when module not loaded.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-session-cache-module.md`



### PT-50
- id: `PT-50`
- requirement: `I-20260426-0000-A phase_state updated to completed`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-50`
- case_design: `Verify phase_state=completed in docs/B2-docs/ibm/_legacy-issues/I-20260426-0000-A/issue.md. Verify scan excludes completed issues.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-phase-state.md`



### PT-51
- id: `PT-51`
- requirement: `gitee-issue.py close/update use correct PATCH path and accept string IDs`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-51`
- case_design: `Verify close accepts IJFOAK format. Verify PATCH uses repo_path_post. Verify 161 issues closable.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-gitee-close-api.md`



### PT-52
- id: `PT-52`
- requirement: `freely new-session forces fresh launch even when JSONL dir has old sessions`
- evidence_level: `integration`
- status: `pass`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#T-52`
- case_design: `Verify new-session writes FORCE_FRESH=true. Verify select_launch_kind checks FORCE_FRESH before JSONL fallback. Verify FORCE_FRESH stripped after first launch.`
- artifact_ref: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews/20260428-fix-force-fresh.md`

