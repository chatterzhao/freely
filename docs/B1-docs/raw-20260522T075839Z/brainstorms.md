# Brainstorm: switch auto-extract tool from slot name

## Discovery

Auto-extract tool selection is hardcoded to a specific tool path. When the tool is rearranged (e.g., moved to a different slot or renamed), auto-extract breaks silently.

### Involved files

- `freely` runtime script — auto-extract invocation
- Tool slot configuration

## Research

### Option A: Keep hardcoded tool path
- Simple but fragile
- Breaks on tool reorganization

### Option B: Resolve auto-extract tool from slot name (selected)
- Look up the tool by its slot name at runtime
- Resilient to tool relocation/renaming
- Consistent with how other tools are resolved

## Decision

**Option B — Switch auto-extract to dynamic slot-based resolution.**

### Implementation
1. Replace hardcoded tool path with slot-name-based lookup
2. Verify auto-extract works after tool relocation
3. Test edge cases (missing slot, empty result)

### Acceptance
- [x] Auto-extract resolves tool from slot name
- [x] Works after tool is moved to different path
- [x] Graceful failure when slot is missing
