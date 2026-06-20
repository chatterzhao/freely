# B1: Brainstorm — A2A SSE Supervision + Worker Session Tracking

## Problem

A2A Server has full SSE streaming infrastructure (SSE endpoint, subscriber registry,
TaskStatusUpdateEvent, session/prompt mechanism) — but Manager never uses any of it.
Manager only polls DB via `list --status completed` during patrol.

Two missing pieces:
1. Worker session ID not stored in A2A task after launch → Manager can't use session/prompt
2. Manager patrol doesn't subscribe to SSE or check worker liveness

## Brainstorm Options

### Option A: Full SSE-based event-driven Manager
- Manager subscribes to SSE for each active worker
- Events drive patrol flow (no more polling)
- Requires long-lived SSE connections in Manager's ACP session
- Complex: SSE event parsing in bash/AI context

### Option B: Hybrid — SSE subscription + polling fallback (chosen)
- Store worker session_id in A2A task
- Manager can optionally subscribe to SSE via curl
- Polling remains the primary patrol mechanism
- session/prompt intervention when workers stall

### Option C: Manager-only polling (current state, rejected)
- No session_id tracking
- No intervention capability
- Workers can silently fail

## Chosen: Option B — Hybrid

Rationale:
- SSE infrastructure already exists; adding session_id tracking unlocks it
- Polling remains reliable primary mechanism
- session/prompt gives Manager active intervention capability
- Incremental change, low risk

## Implementation Scope
1. Fix session_id pass-through chain: A2A Server POST/PATCH → a2a_task.py → freely runtime
2. Capture worker's ACP session_id after launch and update A2A task
3. Update manager-agent.md patrol flow with SSE awareness and intervention instructions
4. Add `prompt` CLI command for session/prompt intervention

## Trade-offs
- Session ID capture is async (background process) → up to 30s delay
- SSE subscription needs curl in AI context → may not be reliable for all AI models
- session/prompt stores message on task but real-time delivery depends on ACP bridge integration
