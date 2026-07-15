---
b1_id: B1-20260715T115327Z
phase_state: completed
source_raw: raw-20260715T115327Z
---
# B1: AI monitor script selection uses wrong adapter variable

## Problem
freely script line 22757 uses `${AGENT_AI_TOOL_ADAPTER:-direct}` to select the monitor script (acp vs direct). AGENT_AI_TOOL_ADAPTER is NOT set in config.toml (agent-table replaces AI_TOOL entirely). The variable always defaults to "direct", routing all AI launches through the deprecated monitor-ai-cli.sh instead of monitor-ai-acp.sh.

Meanwhile, line 22720 correctly resolves tool_adapter="acp" from the tool registry ([claude.adapters].default = "acp"). But this resolved value is never used.

## Decision
Change line 22757 from `${AGENT_AI_TOOL_ADAPTER:-direct}` to `${tool_adapter:-acp}`.

Use the registry-resolved adapter. Fallback to acp (never direct — direct is forbidden).

## Candidate
C-20260715T115327Z-A promoted M-20260715T115327Z-A
