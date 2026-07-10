---
local_id: raw-20260620T060132Z32Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T060132Z-A
platform_ids:
  github:
    issue_id: '3149'
    url: https://github.com/chatterzhao/freely/issues/3149
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T06:01:50Z'
updated_at: '2026-06-20T06:01:50Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Problem

Claude Code reads CLAUDE.md from project root for project-level instructions.
codex CLI and opencode read AGENTS.md, but Claude Code does not. After 'freely init',
Claude Code users get no project context unless they manually create CLAUDE.md.

## Solution

'freely init' generates a minimal CLAUDE.md in the project root:

  # CLAUDE.md
  Read AGENTS.md for project governance, conventions, workflow, and Freely AI
  runtime instructions. This file is the single source of truth for AI agents
  working on this project.

This is the industry standard pattern: CLAUDE.md as a pointer file that
delegates to the full documentation.

Reference: Claude Code documentation recommends placing project-level
instructions in CLAUDE.md at the repo root. The standard pattern is a
short file that may reference other docs.

## Implementation

In ensure_project_agents_md(), add CLAUDE.md generation alongside AGENTS.md.
Only create if CLAUDE.md doesn't already exist (don't overwrite user's).
