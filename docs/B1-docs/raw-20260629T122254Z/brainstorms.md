---
b1_id: B1-20260629T122254Z
phase_state: completed
source_raw: raw-20260629T122254Z
produced_candidate: C-20260629T122254Z-A
---
# B1_IBM: command standardization — freely subcommands

## Analysis
All ./bin/ scripts categorized:

### External CLI (registered as freely xxx):
Workflow [cmd] nodes: cycle, watchdog, pr-review-guarded, deploy-skills
Diagnostic: governance-check
Gates (semi-user-facing): checkpoint-guard, pretests-gate, pretests-retirement-gate

### Internal only (stay ./bin/xxx):
governance-merge/promotion/closeout-gate (hooks), freely-review (pr-review), merge-guarded (pr-merge)
All test-*, check-*, build scripts, libraries (worktree-common.sh, toml2env)

## Decision
Add 8 freely subcommands via case dispatch + exec functions.
