# Issue: tool-alias-and-opencode-launcher-governance

- issue_id: `I-20260426-0000-A`
- title: Add opencode direct launcher and AI_TOOL alias resolution
- phase_state: `completed`
- completed_at: `2026-04-28`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `tool-alias-and-opencode-launcher-governance`
- issue-name: `tool-alias-and-opencode-launcher-governance`
- source_candidate: `docs/B1-docs/raw-20260426/candidates.md#c-20260426-0000-a`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/tool-alias-and-opencode-launcher-governance/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/ibm/tool-alias-and-opencode-launcher-governance/code-reviews`
- session_refs:
  - {tool: opencode, session_id: "20260426-opencode-launcher", jsonl_path: "unavailable://manual", role: "author"}

## Why

Freely runtime recognizes opencode as a valid tool name but has no launch implementation. Users need to switch from codex to opencode after API balance exhaustion. Additionally, users with shell aliases (e.g. ccds for Claude Code + custom settings) cannot use them directly as AI_TOOL.

## Scope

1. Add opencode case to tool_run_direct_from_prompt_file with --dangerously-skip-permissions auto mode.
2. Add opencode session ID extraction (ses_* pattern) in monitor-ai-cli.sh.
3. Add opencode to all tool validation lists (freely, start-lead-agent.sh, tool-launchers.sh).
4. Add AI_TOOL_EXTRA_ARGS injection to all direct launcher exec lines.
5. Add shell alias resolution: unknown AI_TOOL values resolved via zsh -ic, binary extracted for family detection, alias args injected.
6. Add AI_TOOL_FAMILY override for resume/session convention control.

## Non-Goals

1. Full opencode probe/watchdog parity with codex.
2. OpenCode slot/account switching support.
3. OpenCode ACP adapter support.
4. OpenCode --add-dir boundary support.
5. Auto-detection of session patterns from tool output.

## Acceptance

1. opencode launches via direct adapter in auto mode with --dangerously-skip-permissions.
2. Session ID extracted from opencode --print-logs output pattern ses_*.
3. AI_TOOL=ccds resolves alias via zsh -ic, extracts claude binary, enters cc family.
4. AI_TOOL_EXTRA_ARGS injected into all tool exec lines.
5. AI_TOOL_FAMILY overrides detected family.
6. Tool validation lists include opencode.

### C-20260426-0002-A: AGENTS.md break-glass guidance hardening
- absorbed_at: `2026-04-26`
- reason: `Post-merge governance fix. AGENTS.md guidance hardened to prevent future bypass rationalization.`

### C-20260426-0003-A: IBM Framework canonical documentation
- absorbed_at: `2026-04-26`
- reason: `Governance terminology unification. Formalized B1_IBM/B2_IBM naming across all active governance docs as Freely capability.`

### C-20260427-0000-A: B1 intake→issue sync design
- absorbed_at: `2026-04-27`
- reason: `B1 pre-brainstorm design for unifying chat/intake into issue-centric model. 161 milestone issues synced to GitHub and Gitee. Platform adapter, storage layer, sync scripts implemented.`
- scope: `brainstorms (26 sections), candidates (7 decisions), TASKS (30 items), ibm-framework.md update, docs/issues/ storage, bin/issue-* scripts, gitee-issue.py fix, platform-adapter.py`

### Bug fix: tool_extra_args unbound variable
- fixed_at: `2026-04-27`
- reason: `tool_extra_args[@] under set -u caused unbound variable error when AI_TOOL_EXTRA_ARGS was not set. Fixed with :- default operator.`

### Bug fix: claude not in tool validation lists
- fixed_at: `2026-04-27`
- reason: `cc-ds-auto resolves to claude binary, but start-lead-agent.sh and tool-launchers.sh validation lists were missing claude.`

### CHG 2.1-2.3: chat→issue migration
- implemented_at: `2026-04-27`
- reason: `write_intake_item now also writes to docs/issues/. New scan_raw_issues() in task-source-scan.py. Backward compatible.`

### CHG: chat --issue/--urgent + comment append
- implemented_at: `2026-04-27`
- reason: `--issue flag appends chat as ### comment. Active B2+dev+verification phases trigger urgent signal.`

### CHG: chat routing auto-detection
- implemented_at: `2026-04-27`
- reason: `_route_chat_to_issue() extracts issue references from messages. Script-based matching against ISSUES.md.`

### CHG 2.2/4.2: TODO markers removed
- completed_at: `2026-04-27`
- reason: `All intake CRUD functions migrated to docs/issues/. Handler bridge in place. Zero TODO markers remaining.`

### File size check: configurable + skip markers
- completed_at: `2026-04-27`
- reason: `Made FILE_SIZE_WARN/ERROR configurable via .freely/config.env. Added skip markers for legacy/third-party files.`
- scope: `bin/check-file-size rewritten, .freely/config.env updated`

### File size check: TIP level for proactive refactoring hints
- completed_at: `2026-04-27`
- reason: `Added FILE_SIZE_TIP (default 300) threshold as a gentle nudge before WARN. Output [TIP] prefix.`
- scope: `bin/check-file-size (tips counter, TIP level), .freely/config.env (FILE_SIZE_TIP=300)`

### File size check: skip visibility
- completed_at: `2026-04-27`
- reason: `Skipped files now shown with [SKIP] prefix and counted in summary instead of silently ignored.`
- scope: `bin/check-file-size (skips counter, [SKIP] output)`

### File size check: TIP → DANGER rename, threshold 750
- completed_at: `2026-04-27`
- reason: `Renamed TIP to DANGER and raised threshold from 300 to 750. DANGER sits between WARN (500) and ERROR (1000) with clear urgency.`
- scope: `bin/check-file-size (dangers counter, [DANGER] output, check order WARN→DANGER→ERROR)`

### Bug fix: parse_ai_spec hard reject blocks alias resolution
- fixed_at: `2026-04-27`
- reason: `parse_ai_spec() in freely rejected unknown tools with exit 1 before alias resolution could run. Changed to warn + pass through, added claude to known list.`
- scope: `docs/system/workspace/scripts/runtime/freely (parse_ai_spec)`

### Bug fix: cmd_chat not parsing --issue/--new-issue flags
- fixed_at: `2026-04-27`
- reason: `cmd_chat() documented --issue/--new-issue in usage but never parsed them. All chat messages were broken. Also default to --new-issue for backward compatibility.`
- scope: `docs/system/workspace/scripts/runtime/freely (cmd_chat, submit_human_frontdoor_message, cmd_intake_chat)`

### Bug fix: rc=1 exit after clean SessionEnd causes restart loop
- fixed_at: `2026-04-27`
- reason: `Claude Code -p mode exits rc=1 after SessionEnd:other even when session completed cleanly. Daemon treated this as failure, creating a restart loop. Now checks debug log for SessionEnd completed with status 0 to normalize rc.`
- scope: `docs/system/workspace/scripts/runtime/freely (rc normalization before exit reason recording)`

### Bug fix: resume target extraction fails for Claude -p mode
- fixed_at: `2026-04-27`
- reason: `Session ID extraction searched the main cycle log (empty for claude -p). Now searches debug log first, with CLAUDE_SESSION_ID_CURRENT fallback. This enables resume to pass --resume flag.`
- scope: `docs/system/workspace/scripts/monitor-ai-cli.sh (extract_tool_session_id_from_log_if_present, write_live_session_state_if_possible)`

### Bug fix: worker prompt paths not extracted from continuity files
- fixed_at: `2026-04-27`
- reason: `Two format mismatches: section header (code expected "worker prompts" plural, AI wrote "Worker Prompt" singular) and line format (code expected "- /path" list item, AI wrote "See: /path"). This caused all 150+ worker prompts to be invisible to the dispatch mechanism.`
- scope: `docs/system/workspace/scripts/runtime/freely (manager_worker_prompt_paths_from_continuity_by_mode section normalization, line regex, rg fallback)`

### Feature: issue platform sync complete (bin/issue-sync, chat routing, merge hook)
- completed_at: `2026-04-28`
- reason: `Replaced scattered sync scripts with unified bin/issue-sync. Added issue_title, promoted_from, absorbed_into to issue model. I-* body is self-contained summary + links (hybrid). Chat auto-routes raw→I-* when absorbed. Merge hook syncs changed issues to platforms. Deleted dead ISSUES.md.`
- scope: `bin/issue-sync (create/update/comment/close/promote/status), docs/system/workspace/scripts/runtime/freely (chat auto-redirect), docs/system/workspace/scripts/worktree/pr-merge-guarded (post-merge sync), docs/system/workspace/ibm-framework.md (design doc), bin/issue-index (fix stray 0), docs/issues/ISSUES.md (deleted)`
