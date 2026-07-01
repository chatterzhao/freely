---
b1_id: B1-20260701T003241Z
phase_state: completed
source_raw: raw-20260701T003241Z
produced_candidate: C-20260701T003241Z-A
---
# B1: remove --ai, deprecate AI tool fields, block init on config

## Problem
--ai fills AI_TOOL/AI_MODEL/AI_MODE which are deprecated. AI_MODEL overriding slot config causes errors (wrong model for tool). AI_MODE permissions come from slot config.

## Decision
- Remove --ai from init
- Remove AI_TOOL/AI_MODEL/AI_MODE/AI_REASONING_EFFORT from example
- Remove Codex-specific fields from example
- Block init when config.toml exists without --reset
- Guide users to agent-table.toml for tool config
