# Brainstorms - 20260426-0000--opencode-direct-launcher-integration

## Problem

Freely's runtime currently supports `codex`, `cc`, `iflow`, and `kiro-cli` as AI tool launchers. The `opencode` CLI tool is installed and available but has no launch path in `tool_run_direct_from_prompt_file`. The user needs to switch from `codex` (which has API balance issues) to `opencode` for autonomous development.

## Context

- `opencode` v1.14.26 is installed at `/Users/zhaoyu/.opencode/bin/opencode`
- `opencode run` provides non-interactive mode with `--dangerously-skip-permissions` for auto-approval
- `opencode` uses `-s <session_id>` for session resume
- Session IDs follow format `ses_*` and are logged via `--print-logs`
- The runtime already recognizes `opencode` as a valid tool name but has no launch implementation

## Decision

Add `opencode` to the `direct` adapter launch path in `tool_run_direct_from_prompt_file`, updating tool classification functions and session ID extraction to match.
