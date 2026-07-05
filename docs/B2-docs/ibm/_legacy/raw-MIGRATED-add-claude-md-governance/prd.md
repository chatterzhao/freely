# PRD: CLAUDE.md governance auto-loading

## Problem
Claude Code auto-loads CLAUDE.md but Freely project only has AGENTS.md.
AI sessions start without project governance rules in context, leading to
direct develop commits, manual raw issue creation, and other violations.

## Fix
Create lightweight CLAUDE.md at project root containing:
1. Pointer to AGENTS.md and core docs
2. Absolute prohibitions (CONSTITUTION §5)
3. Standard workflow summary
4. Session startup checklist

## Design Decision
- CLAUDE.md is a ~40 line summary, not a full mirror of AGENTS.md
- Acts as a "quick reference" that leads AI to the full docs when needed
