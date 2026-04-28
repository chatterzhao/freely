# Issue: tool-alias-and-opencode-launcher-governance

- issue_id: `I-20260426-0000-A`
- title: Add opencode direct launcher and AI_TOOL alias resolution
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `tool-alias-and-opencode-launcher-governance`
- issue-name: `tool-alias-and-opencode-launcher-governance`
- source_candidate: `docs/pre-brainstorms/20260426-0000--opencode-direct-launcher-integration/candidates.md#c-20260426-0000-a`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/code-reviews`
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
