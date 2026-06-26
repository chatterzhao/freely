---
b1_id: B1-20260626T150328Z
phase_state: completed
source_raw: raw-20260626T150328Z
source_url: https://github.com/chatterzhao/freely/issues/3563
produced_candidate: C-20260626T150328Z-A
created_at: 2026-06-26
---

# B1_IBM: TOML array join delimiter mismatch breaks ACP adapter detection

## Input
- **source_raw**: raw-20260626T150328Z
- **source_url**: https://github.com/chatterzhao/freely/issues/3563
- **discovered during**: Freely daemon start with --task-mode auto
- **symptom**: All AI tools (claude, opencode, codex) fail with `unsupported adapter 'acp'` despite acp being in the supported list

## Problem

`tool-registry-query.py` joins TOML array values with spaces (`" ".join`), but bash consumers in `tool-launchers.sh` split on commas (`tr ',' '\n'`).  This delimiter mismatch causes:

1. `tool_supported_adapters` returns `direct acp` (one line) instead of two lines `direct` and `acp`
2. `grep -Fxq "acp"` fails to match the single combined line
3. `tool_adapter_is_supported` returns false → AI launch aborts with exit 1

Additionally discovered during investigation:
- `freely cmd_feedback` has no title/body format validation — allows titles that violate conventions
- `_ensure_acp_bridge_running` empty array iteration triggers "unbound variable" on bash 3.2 with `set -u`

## Brainstorm

### Option A: Fix only the Python join (minimal)
Change `" ".join` → `",".join` in tool-registry-query.py. Fixes the immediate bug.
- Pro: minimal change, low risk
- Con: breaks `_resolve_tool_by_binary` which does `for _a in $_aliases` (space splitting)

### Option B: Fix only the bash side (backward compatible)
Change `tr ',' '\n'` to also handle spaces: `tr ', ' '\n'`. 
- Pro: doesn't change Python output format, backward compatible
- Con: fragile if any value contains spaces; doesn't fix root cause of format mismatch

### Option C: Fix both sides (comprehensive)
Change Python to comma-join + update bash alias loop. Also fix:
- bash 3.2 `_bridge_env[@]` unbound variable (guarded with length check)
- feedback format validation (title prefix, length, body structure)

## Decision: Option C

- **why_this**: Fixes the root cause (Python→bash format contract) and two other blocking bugs discovered in the same session. Makes feedback format enforceable so future issues have consistent titles.
- **alternatives_considered**: A (too minimal, breaks alias resolution), B (fragile, doesn't address root cause)
- **boundary_non_goals**: Not changing the TOML schema; not changing other bash array iteration patterns (they work because arrays are non-empty when iterated)
- **residual_risk**: Other TOML array consumers might exist in Python code — verified none do

## Candidate
- candidate_id: C-20260626T150328Z-A
- status: promoted
- milestone: M-20260626T150328Z-A
