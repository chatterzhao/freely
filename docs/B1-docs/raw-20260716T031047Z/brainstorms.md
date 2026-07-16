# Brainstorm: worker session_id not written to agent_working

## Problem
`capture_worker_session_id_and_store()` has two bugs preventing worker session IDs from being recorded:
1. Uses `agent_id` ("worker_01") as raw_key instead of actual raw_key ("20260716T025126Z")
2. The pre-launch `agent_assign` at L13275 hardcodes raw_key="develop"

Without session_id in agent_working, other agents cannot session/prompt to interject.

## Root Cause Analysis

### Bug 1: capture_worker_session_id_and_store raw_key
- Function signature: `capture_worker_session_id_and_store() { local manager_project="$1" worker_cycle_log="$2" task_id="$3" target_project="${4:-}" agent_id="${5:-}" slot="${6:-}"`
- At L13082, calls `acp_session_register('${manager_project}', '${agent_id}', 'worker', '${agent_id}', ...)` 
- `${agent_id}` is "worker_01" — not a raw_key
- The function has NO raw_key parameter

### Bug 2: agent_assign pre-launch raw_key
- At L13275: `agent_assign('${PROJECT_ROOT}', 'develop', 'worker', '${_worker_agent_id}', ...)`
- Hardcodes "develop" as raw_key
- Should be the actual worktree raw_key

## Call Sites
1. L13263: `capture_worker_session_id_and_store "$manager_project" "$worker_cycle_log" "$task_id" "$target_project" "worker_01" "${AGENT_AI_TOOL:-claude}"`
2. L13305: `capture_worker_session_id_and_store "$manager_project" "$worker_cycle_log" "$task_id" "$target_project" "$_worker_agent_id" "$_worker_slot"`

## Fix Strategy

### Option A: Extract raw_key from target_project path
Worktree paths contain the raw_key: `.../freely-worktrees/fix-raw-20260716T031047Z-...`
Extract with regex: `grep -oE '[0-9]{8}T[0-9]{6}Z'`

Pros: No API changes needed, works at all call sites
Cons: Fragile if path format changes

### Option B: Add raw_key parameter to function
Add 7th parameter. Call sites extract raw_key from their context.

Pros: Explicit, clear ownership
Cons: Requires call-site changes

### Option C: Extract raw_key from branch name in target_project
`git -C "$target_project" symbolic-ref --short HEAD | grep -oE '[0-9]{8}T[0-9]{6}Z'`

Pros: Authoritative source, git-based
Cons: Slower (git call)

## Recommended: Option A (path extraction)
- Simplest: one line added to function, no call-site changes
- All worktrees follow the same naming convention
- Already used elsewhere in freely (see L24564 for similar extraction)
