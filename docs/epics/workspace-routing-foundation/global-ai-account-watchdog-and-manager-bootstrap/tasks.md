# Tasks: global-ai-account-watchdog-and-manager-bootstrap

- [x] materialize global watchdog issue and boundaries
- [x] add CLI-first ensure-manager entry
- [x] separate global account recovery from manager/worker duties
- [ ] add live integration test for running-manager bad-account to good-account recovery
- [ ] verify manager restarts and resumes supervision after recovery
- [x] add script-level regression for account selection before manager bootstrap
- [ ] verify each account switch causes a new codex process launch before continuing
