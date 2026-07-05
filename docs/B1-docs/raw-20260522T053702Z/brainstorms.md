# Brainstorm: cmd_login apikey unified at top

## Discovery

Current `cmd_login` apikey handling is fragmented — some paths handle apikey at the caller level, others deep inside the login flow. This creates inconsistent behavior and makes it hard to add new login methods.

### Involved files

- `freely` runtime script — cmd_login dispatch
- `ai-cli` — apikey-based auth paths

## Research

### Option A: Keep existing scattered apikey handling
- No changes needed
- Fragmentation remains, future maintenance burden

### Option B: Unify apikey handling at top of cmd_login (selected)
- Single apikey resolution point before dispatching to sub-commands
- Consistent behavior across all login paths
- Future login methods benefit from unified path

## Decision

**Option B — Unify apikey handling at cmd_login entry point.**

### Implementation
1. Move apikey resolution to top of `cmd_login` function
2. Remove scattered apikey handling in sub-paths
3. Ensure backward compatibility for existing callers

### Acceptance
- [x] apikey resolved once at cmd_login entry
- [x] All sub-paths use the unified apikey value
- [x] No regressions in existing login flows
