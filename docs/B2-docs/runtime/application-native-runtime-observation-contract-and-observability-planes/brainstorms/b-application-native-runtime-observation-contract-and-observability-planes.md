# IBM Brainstorm: application-native-runtime-observation-contract-and-observability-planes

## Focus

- freeze the shared observation contract without over-expanding into richer product surfaces
- keep Freely self-host as the first concrete profile, not the only profile
- carry only the minimum fields required for issue completion judgement, delete-gate judgement, and human/manager/watchdog observation

## Frozen IBM Inputs

1. `acceptance evidence schema` stays canonical in the artifact plane
2. current-state / fleet / API surfaces mirror only a minimum summary plus `acceptance_ref`
3. CLI / TUI / GUI / API share one minimum `deep ref group` vocabulary
4. richer runtime / UI observability remains follow-on scope
5. `live-status` / `fleet-status` remain the day-1 current-state / fleet concrete profile for Freely self-host
6. multi-subagent activity remains aggregated under lane / worktree / session surfaces on day 1

## Implementation Bias

- start with truth-surface and machine-readable contract updates
- do not block the shared contract on richer TUI / GUI rendering
- route later productization into follow-on issues once the shared contract is stable
