# opencode direct launcher integration - premerge verification

- issue: `I-20260401-0840-A`
- absorbed_candidate: `C-20260426-0000-A`
- verified: `2026-04-26`
- reviewer: `manual`
- status: pass

## Scope
Add opencode as a direct-adapter AI tool launcher in the freely runtime. Changes are limited to:
- tool-launchers.sh: add opencode case to tool_run_direct_from_prompt_file
- monitor-ai-cli.sh: add opencode session ID extraction pattern
- freely: add opencode to tool_prefers_explicit_resume_target
- start-lead-agent.sh: add opencode to tool validation list

## Verification
- bash -n syntax check passes for all modified files
- opencode run tested with --dangerously-skip-permissions (auto mode) and deepseek-v4-pro model
- Session ID extraction verified: pattern matches ses_* format from opencode --print-logs output
- Full daemon lifecycle verified: supervisor_started -> ai_launch_begin -> ai_cycle_finished
- Tool validation gate passes: opencode recognized in all tool lists
