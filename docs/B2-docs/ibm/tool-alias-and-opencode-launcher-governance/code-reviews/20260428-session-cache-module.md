# Session-cache module - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Extract session/cache operations into unified session-cache.sh module with tool-abstracted API. Each tool's fork/resume/fresh args, session dir, and ID extraction are in one place.`
- why_this: `Session logic was scattered across 3 files with hardcoded claude args. Adding a new tool required changes in multiple places. The module provides a single abstraction point.`
- alternatives_considered: `1) Keep scattered: rejected, maintenance burden. 2) Full refactor: rejected, risky. 3) Module with fallbacks: chosen, gradual migration.`
- boundary_non_goals: `Lifecycle logic (select_launch_kind) stays in freely. Module handles tool-specific ops only.`
- residual_risk: `Fallback code paths remain in all files for bootstrap.`

## Verification
- bash -n: `pass` (session-cache.sh, freely, tool-launchers.sh, monitor-ai-cli.sh)
- session_fork_args claude: `pass` (outputs --resume <p> --fork-session --session-id <c>)
- session_dir_for_tool claude: `pass` (correct slug with leading -)
- session_extract_id_from_log claude: `pass` (debug log + main log fallback)
