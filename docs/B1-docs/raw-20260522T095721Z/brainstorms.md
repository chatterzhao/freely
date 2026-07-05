# Brainstorm: codex acp full lifecycle

## Discovery

- Source: GitHub issue #2125 (raw-20260522T095721Z)
- Proposed at: 2026-05-22T09:57:21Z
- Still relevant: Yes — ACP is the default adapter; missing lifecycle handling causes silent failures.

## Problem Definition

ACP became the default adapter for AI CLI tools, but the codebase lacked pre-flight checks for ACP binary availability. This caused silent failures in the daemon when ACP binaries were missing or misconfigured.

Key gaps:
1. No binary availability check before ACP adapter launch
2. Silent failures at daemon runtime (hard to diagnose)
3. `handoff.py` had a missing `import sys` causing `NameError` on error paths

## Research

### Affected entry points
- `freely init` — adapter resolution doesn't validate ACP binary
- `ai login` (apikey) — no pre-flight check
- `ai switch` — no pre-flight check
- Daemon runtime — discovers missing binary only on first ACP launch

### Available tooling
- `ensure_codex_acp_binary_for_launch` — auto-downloads codex-acp binary (exists for codex)
- `command -v claude-agent-acp` — checks system PATH for Claude's ACP binary
- ACP binary can be overridden via `FREELY_{TOOL}_ACP_BIN` env vars

### Approaches considered
1. **Block at daemon start**: Too early — ACP may not be used in every session
2. **Block at adapter resolution**: Better — check when ACP is selected as adapter
3. **Pre-flight at init/login/switch**: Best — fail fast at user-facing commands with clear error messages

## Decision

Approach 3 was chosen: pre-flight ACP binary availability checks at user-facing commands.

Specific implementation:
1. `_require_acp_binary()` function in `ai-cli` — single source of truth
   - codex → delegates to `ensure_codex_acp_binary_for_launch` (auto-download)
   - Other tools → checks `claude-agent-acp` via `command -v`
2. `freely init` inline check — gated on `$tool_adapter == "acp"`, placed after adapter resolution
3. `ai login` (apikey) check — same function call
4. `ai switch` check — same function call
5. `import sys` fix in `handoff.py` — missing import causing `NameError`

### Acceptance criteria
- [x] Pre-flight check blocks init when ACP binary not available
- [x] Pre-flight check blocks login when ACP binary not available
- [x] Pre-flight check blocks switch when ACP binary not available
- [x] Clear error message on failure (not silent)
- [x] `test-acp-binary-check-require-available`: 6 test cases pass
- [x] Manual verification: `_require_acp_binary` blocks with non-existent path

## Status

Converged. Candidate promoted to I-20260522T095721Z-A, implemented and completed.
