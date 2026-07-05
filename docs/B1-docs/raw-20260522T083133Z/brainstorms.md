# Brainstorm: switch auto all tools

## Discovery

The "auto" tool mode only auto-selects a subset of tools (extract, fallback). Other tools still require explicit user selection. This limits the autonomy of AI-driven operations.

### Involved files

- `freely` runtime script — tool mode dispatch
- Tool selection configuration

## Research

### Option A: Extend auto mode incrementally
- Add one tool at a time
- Lower risk but slower

### Option B: Switch auto mode for ALL tools at once (selected)
- All tools use auto-selection in "auto" mode
- Consistent behavior across tool categories
- One-shot change, easier to verify

## Decision

**Option B — Extend auto mode to all tools.**

### Implementation
1. Replace per-tool auto flag with global auto mode
2. Ensure all tool categories respect the auto setting
3. Remove individual tool auto overrides

### Acceptance
- [x] All tools use auto-selection in auto mode
- [x] No per-tool auto flags remain
- [x] Backward compatible with existing configurations
