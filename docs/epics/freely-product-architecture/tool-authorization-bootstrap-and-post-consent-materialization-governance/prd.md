# PRD: tool-authorization-bootstrap-and-post-consent-materialization-governance

## Goal

Make Freely's post-consent tool authorization/bootstrap contract explicit, so project onboarding and later settings changes share one truthful model for what can be automated, what stays manual, and how degradation is explained.

## User/Operator Outcome

- Users can tell what they are authorizing when they trigger `freely init` or later tooling repair/settings actions.
- Operators get a stable per-tool matrix instead of guessing whether a wrapper, adapter, or config write counts as trust/bootstrap.
- Future CLI/TUI/GUI/settings work can reuse one backend contract instead of drifting into separate semantics.
- Follow-on implementation owners can split by seam instead of reopening umbrella architecture debate.

## Constraints

- Freeze the contract before widening runtime implementation.
- Do not over-claim automation for tools that lack verified project-local config/trust surfaces.
- Keep home-level trust/config out of default automatic mutation unless explicitly approved and officially supported.
- Keep degradation reporting symmetric across CLI, TUI, GUI, and future settings surfaces.
