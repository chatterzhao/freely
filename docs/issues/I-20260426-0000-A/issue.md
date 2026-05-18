---
local_id: I-20260426-0000-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '2'
    url: https://github.com/chatterzhao/freely/issues/2
    synced_at: '2026-04-27T11:11:27Z'
  gitee:
    issue_id: IJFOAK
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAK
    synced_at: '2026-04-27T13:17:44Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:11:27Z'
hash: ''
created_at: '2026-04-27T11:11:27Z'
updated_at: '2026-05-17T12:25:14Z'
issue_title: Add opencode direct launcher and AI_TOOL alias resolution
platform_state: closed
---

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
