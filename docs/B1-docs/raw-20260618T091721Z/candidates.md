# Candidates: CLAUDE.md project governance auto-loading

## C-20260618T091721Z-A: legacy issue
- title: Add CLAUDE.md for automatic AI governance rule loading
- status: promoted
- promoted_issue_path: docs/issues/I-20260618T091721Z-A/issue.md
- milestone: M-20260618T091721Z-A
- summary: |
    Claude Code auto-loads CLAUDE.md at the project root into every AI session
    context. Freely project only has AGENTS.md which is NOT auto-loaded.
    Adding CLAUDE.md ensures governance rules (CONSTITUTION, LAWS, workflow)
    are visible to AI from the start of every session.

### Alternatives considered
- **Rename AGENTS.md to CLAUDE.md**: Rejected. AGENTS.md is the established
  entry point referenced by many other docs. Better to add CLAUDE.md as a
  lightweight redirect/summary.
- **Symlink CLAUDE.md → AGENTS.md**: Rejected. CLAUDE.md should be a curated
  summary, not the full 500+ line AGENTS.md.
