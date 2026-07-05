# Brainstorm: help text generic

## Discovery

Help text in several CLI commands is hardcoded with specific tool names and paths. This makes it brittle when tools are renamed or reorganized.

### Involved files

- `freely` runtime script — usage/help output
- Various subcommand help strings

## Research

### Option A: Keep specific help text
- Simple but brittle
- Every tool rename requires help text update

### Option B: Generic help text with dynamic references (selected)
- Help text references tools by variable/slot name rather than hardcoded values
- Self-documenting as tools evolve

## Decision

**Option B — Replace hardcoded help text with dynamic/generic references.**

### Implementation
1. Identify all hardcoded tool names in help output
2. Replace with variable references or generic descriptions
3. Verify help output remains informative

### Acceptance
- [x] No hardcoded tool names in help text
- [x] Help output clearly describes functionality without specific tool names
- [x] All CLI subcommands reviewed
