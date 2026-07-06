# PRD: global-restart-restore-memory-governance

## Goal

为 future all-project global restart 冻结 restore memory contract，使 Freely 能在 global restart 后按 previously-running set 恢复正确的 projects，并保留足够 durable evidence 支撑可追溯恢复。

## Why Now

source candidate 已经明确 global restart 不能成为 project force 的隐式副作用。若不先冻结 restore memory contract，后续实现很容易再次把 global reset、operator intent 与 project-local continuity 混成一个 owner。

## Product Surface

1. future explicit global `restart` surface
2. `$FREELY_HOME/control-plane/restart/latest.json`
3. `$FREELY_HOME/control-plane/restart/history/<timestamp>.json`
4. fleet restore policy for previously-running projects

## Non-Goals

1. 不定义单项目 command semantics。
2. 不把 auxiliary runtime artifacts 提升成 required manifest anchors。
3. 不在本轮实现 global reset / restart code path。
4. 不承担 watchdog/account-slot recovery owner。

## Non-Negotiables

1. global restart 只能是显式 all-project action。
2. operator-stopped projects 不得被误恢复。
3. restore memory 必须消费 durable continuity anchors，而不是瞬态 pid/run-state。
4. 本 issue 继承 `I-20260327-2006-A` taxonomy，不重写 project blast radius。

## Context Pack

1. source candidate 已冻结 global restart durable home 与 retention。
2. mandatory restore anchors 已从 project-vs-global taxonomy 中剥离出来。
3. `I-20260318-1630` 只提供 supporting truth：global watchdog/bootstrap exists, but not this manifest contract.
4. current repo 尚无 canonical global restart manifest artifact。

## Decomposition Tree

1. Define explicit global restart surface
2. Define manifest schema and retention
3. Define previously-running set and operator-stopped exclusion
4. Define restore inputs vs auxiliary evidence
5. Define fleet restore replay and verification path

## Prototype Path

1. First add manifest writer/reader contract with latest + history retention.
2. Then capture previously-running project set and exclusion rules.
3. Finally wire fleet restore replay and protected-branch verification.

## Eval Plan

### Pre-merge focused regression / smoke

- environment: feature worktree
- evidence: manifest schema tests, retention tests, fleet selection tests
- failure signal: manifest loses required anchors, includes operator-stopped projects, or consumes auxiliary-only evidence as required truth
- failure handling / replay expectation: fix in the same feature worktree and rerun focused tests

### Post-merge integration acceptance

- environment: `develop`
- evidence: one global restart rehearsal over a controlled set of projects
- failure signal: global restart cannot reconstruct previously-running set or restores a project that should stay stopped
- failure handling / replay expectation: record verification artifact and repair from a feature worktree

### Post-merge application-native real-environment acceptance

- environment: `develop` protected verification worktree
- evidence: Freely's own fleet survives an explicit global restart with correct restore memory
- failure signal: restart loses durable continuity anchors or cross-restores wrong projects
- failure handling / replay expectation: capture recovery note and replay fix from feature worktree

### Post-merge end-to-end dogfood acceptance

- environment: `develop` protected verification worktree
- evidence: dogfood global restart uses the same manifest and retention contract
- failure signal: dogfood run recreates blind global relaunch behavior
- failure handling / replay expectation: open follow-on lifecycle if the failure reveals a new owner

## Execution Slices

1. manifest schema and retention slice
2. previously-running set capture slice
3. operator-stopped exclusion slice
4. fleet restore replay slice
5. verification artifact slice

## Revisit Triggers

1. global restart surface expands into reset/wipe semantics needing a separate owner
2. mandatory restore anchors change due to new continuity architecture
3. fleet selection cannot be derived from current `workcell-state.env` and launch-state truth
4. real incidents show retention or restore replay is insufficient

## Dev-Loop Handoff

- keep `depends_on` on `I-20260327-2006-A`
- implement against `docs/B2-docs/ibm/global-restart-restore-memory-governance/raw-20260327-2006/verification/pre-tests.md`
- write progress only after dev work starts
