# Brainstorm: update fallback tool priority

## Discovery

Fallback tool priority is outdated — some high-quality tools are ranked below lower-quality fallbacks. When primary tools fail, the system falls back to suboptimal alternatives.

### Involved files

- `freely` runtime script — fallback tool selection logic
- Tool capability ranking configuration

## Research

### Option A: Manual reordering of hardcoded fallback list
- Quick fix
- Must be re-evaluated periodically

### Option B: Priority-based fallback selection (selected)
- Assign explicit priority scores to fallback tools
- Choose highest-priority available tool
- Easier to maintain and extend

## Decision

**Option B — Priority-based fallback tool selection.**

### Implementation
1. Assign priority scores to all fallback tools
2. Update selection logic to choose highest-priority available tool
3. Remove outdated hardcoded ordering

### Acceptance
- [x] Fallback selection uses priority scores
- [x] Higher-quality tools selected before lower-quality ones
- [x] No regressions in fallback behavior
