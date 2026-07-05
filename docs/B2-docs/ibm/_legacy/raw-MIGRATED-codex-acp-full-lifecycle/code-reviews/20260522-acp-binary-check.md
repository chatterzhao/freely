# Code Review: ACP Binary Availability Check

## Implementation Decision Note

This change adds pre-flight ACP binary availability checks to `freely init`, `ai login` (apikey), and `ai switch` commands.

### Decisions
1. **`_require_acp_binary()` in `ai-cli`**: A single function that checks ACP binary per tool.
   - codex → `ensure_codex_acp_binary_for_launch` (auto-downloads if needed)
   - Other tools → checks `claude-agent-acp` via `command -v`
2. **`freely init` inline check**: Gated on `$tool_adapter == "acp"`, placed after adapter resolution.
3. **`import sys` in `handoff.py`**: Missing import that caused `NameError` on error paths at L194-195.

### Rationale
- ACP is now the default adapter; missing binaries cause silent failures in daemon.
- Blocking early at init/login/switch prevents confusing runtime errors.
- Using `case "$tool"` pattern for extensibility (future tools add their own binary checks).

### Verification
- `test-acp-binary-check-require-available`: 6 test cases, all pass
- Manual: `_require_acp_binary claude → PASS`, `FREELY_CLAUDE_ACP_BIN=/nonexistent _require_acp_binary claude → FAIL (blocked)`
