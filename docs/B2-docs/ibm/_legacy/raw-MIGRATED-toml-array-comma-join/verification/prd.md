# PRD: TOML array comma-join + feedback validation + bash 3.2 guard

- issue_id: I-20260626T150328Z-A

## Goal

Fix the delimiter mismatch between Python `tool-registry-query.py` (space-joined TOML arrays) and bash `tool-launchers.sh` (comma-split consumers). Add format validation to `cmd_feedback`. Guard empty array iteration for bash 3.2 + `set -u` compatibility.

## Scope

### In Scope
1. `tool-registry-query.py`: TOML array join delimiter space → comma
2. `tool-launchers.sh`: alias loop split on commas
3. `freely` `cmd_feedback`: title/body format validation (4 checks)
4. `freely` `_ensure_acp_bridge_running`: empty array guard

### Out of Scope
- Changing the TOML registry schema
- Changing other bash array iteration patterns (they work — arrays non-empty when iterated)
- Changing the platform-adapter.py issue creation logic

## Dev-Loop Handoff

- Code already committed on `fix/raw-20260626T150328Z-toml-array-comma-join`
- B1_IBM governance done (brainstorms.md, candidates.md, milestones.md)
- B2_IBM governance in progress (this PRD + pre-tests + tasks + code-review)
- Next: pr-create-guarded → pr-review-guarded → pr-merge-guarded → wt-close
