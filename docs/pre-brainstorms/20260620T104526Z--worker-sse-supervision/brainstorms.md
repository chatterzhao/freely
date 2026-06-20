# Brainstorms

## Option A: Full SSE-based event-driven Manager
- Manager subscribes to SSE for each active worker
- Events drive patrol flow (no more polling)
- Requires long-lived SSE connections in Manager's ACP session
- Complex: SSE event parsing in bash/AI context

## Option B: Hybrid — SSE subscription + polling fallback (chosen)
- Store worker session_id in A2A task
- Manager can optionally subscribe to SSE via curl
- Polling remains the primary patrol mechanism
- session/prompt intervention when workers stall

## Option C: Manager-only polling (current state, rejected)
- No session_id tracking, no intervention capability
- Workers can silently fail

## Chosen: B — Hybrid
- SSE infrastructure already exists; adding session_id tracking unlocks it
- Polling remains reliable primary mechanism
- session/prompt gives Manager active intervention capability
- Incremental change, low risk
