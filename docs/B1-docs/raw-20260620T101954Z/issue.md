---
local_id: raw-20260620T101954Z54Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T101954Z-A
platform_ids:
  github:
    issue_id: '3156'
    url: https://github.com/chatterzhao/freely/issues/3156
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T10:20:11Z'
updated_at: '2026-06-20T10:20:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Problem

consume_delegate_workers generates Worker prompt files with only task description +
WORKER_STATE_INJECT (task_id + a2a-exit format). worker-agent.md exists at
docs/system/workspace/agents/worker-agent.md with full role definition, intent_kind→skill
mapping, execution flow, and completion spec — but it's NEVER injected into Worker prompts.

The $_task_skill field from the A2A task DB (e.g., freely-doc-B1_IBM-execution) is also
never injected into the prompt.

Consequences:
- Worker doesn't know it's a Worker Agent with specific capabilities
- Worker doesn't know what skill to invoke for the task's intent_kind
- Worker doesn't know the full pipeline: commit → pr-create → pr-merge → wt-close
- Worker writes files but doesn't commit them (work is lost on worktree cleanup)
- Worker completion_summary echoes the original prompt text instead of actual results

## Fix

In consume_delegate_workers, after writing the task message to the prompt file,
prepend worker-agent.md content and skill context:

1. Read docs/system/workspace/agents/worker-agent.md → prepend as '# Worker Agent' section
2. If $_task_skill is set, read the SKILL.md and inject its workflow steps
3. Ensure the prompt includes: 'After completing work: git add + git commit + a2a-exit
   with real completion summary (not original prompt)'
