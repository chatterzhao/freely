# Tasks: global-ai-account-watchdog-and-manager-bootstrap

- [x] materialize global watchdog issue and boundaries
- [x] add CLI-first ensure-manager entry
- [x] separate global account recovery from manager/worker duties
- [x] add live integration test for running-manager bad-account to good-account recovery
- [x] verify manager restarts and resumes supervision after recovery
- [x] add script-level regression for account selection before manager bootstrap
- [x] verify each account switch causes a new codex process launch before continuing
- [x] probe saved accounts when cooldown records are stale before falling back to earliest reset
- [x] write structured manager bootstrap handoff before watchdog relaunches the manager
- [x] let the live test discover a usable account by real probe when no good account is provided
- [x] make `freely ai switch codex` reuse the same active probe / cooldown update contract as the watchdog path
- [x] make `ensure-manager --watch` survive all-accounts-cooling waits, retry after failed readiness passes, and re-probe before relaunch
- [x] serialize manual/auto account switch sweeps so watchdog probe/bootstrap waits for the shared switch lock instead of racing a transient bad account
