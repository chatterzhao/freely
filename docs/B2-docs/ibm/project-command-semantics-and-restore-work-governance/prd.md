# PRD: project-command-semantics-and-restore-work-governance

## Goal

把 Freely 的单项目 lifecycle command family 冻结成可实现的 contract，让 `start` / `stop` / `restart` / `start --force` / `restore-work` 的 blast radius、repair order 与 interrupted-AI policy 都能被后续 dev-loop 直接消费。

## Why Now

当前 runtime 只有 project-scoped ownership 的底层事实，没有稳定的高层 command semantics。继续拖延会让 project repair、global reset 与 AI-work restore 的边界继续混层。

## Product Surface

1. `freely start`
2. `freely stop`
3. `freely restart`
4. `freely start --force`
5. `freely restore-work`
6. project-local `.freely/run/**` runtime/control-plane artifacts

## Non-Goals

1. 不定义 global restart history manifest 的持久化 schema。
2. 不定义 slot/account watchdog recovery。
3. 不在本轮完成 code review、progress 或 verification artifact。
4. 不把 `session-state.env`、`session-handoff.txt`、pid files 等 auxiliary evidence 提升成 mandatory restore anchors。

## Non-Negotiables

1. project command 不得触碰其他 project 的 runtime/AI/shared watchdog state。
2. process discovery / kill scope 必须锚定 Freely-owned project identity，而不是 generic process names。
3. `restart` 默认不静默恢复 interrupted local AI work。
4. explicit AI-work restore 优先走 dedicated `restore-work` surface。
5. future global action 必须是一眼可见的 all-project control-plane surface。

## Context Pack

1. `cmd_stop()` 已只处理当前 project `.freely/run/` 下并通过 `valid_*_pid_for_project()` 校验的 pid。
2. `cmd_start()` 当前只提供 bootstrap / already-running gate，尚未冻结 repair priority。
3. `I-20260318-1630` 已完成 global watchdog/bootstrap owner，不能 reopen。
4. source candidate 已冻结 mandatory restore anchors：
   - `workcell-state.env`
   - `manager-worker-launch-state.env`
   - continuity artifacts
   - interruption resolutions
   - delegated prompt evidence
   - `.freely/intake/**`
5. source candidate 已冻结 auxiliary evidence：
   - `session-state.env`
   - `session-handoff.txt`
   - pid files
   - stop marker
   - restart-storm window
   - `codex-slot-cooldowns.tsv`

## Decomposition Tree

1. Define command taxonomy
   - freeze `start` / `stop` / `restart` / `start --force` / `restore-work`
2. Define repair order
   - attach/reuse
   - local repair
   - fresh bootstrap
   - explicit global escalation
3. Define safe repair set
   - project-local pid/state cleanup
   - same-project supervisor/dispatcher/watchdog rebuild
   - same-project AI child rebuild
4. Define AI-work restore policy
   - no silent resume on restart
   - explicit restore-work path consumes durable evidence

## Prototype Path

1. First materialize CLI surfaces and internal branching for `restart` / `start --force` / `restore-work`.
2. Then lock project-local repair ordering and forbidden global touches in focused tests.
3. Finally wire restore-work to canonical continuity anchors without reusing auxiliary-only artifacts as required inputs.

## Eval Plan

### Pre-merge focused regression / smoke

- environment: feature worktree
- evidence: runtime-focused shell tests plus targeted command-path checks
- failure signal: project command mutates shared/global artifacts or `restart` silently resumes interrupted AI work
- failure handling / replay expectation: fix in the same feature worktree and rerun focused tests

### Post-merge integration acceptance

- environment: `develop`
- evidence: command-family smoke in canonical runtime path
- failure signal: `develop` command semantics diverge from frozen project taxonomy
- failure handling / replay expectation: failure routes back to feature worktree for repair; `develop` stays verification-only

### Post-merge application-native real-environment acceptance

- environment: `develop` protected verification worktree
- evidence: real project-scoped start/stop/restart/restore-work operator walkthrough with continuity artifacts present
- failure signal: operator cannot distinguish project repair from global escalation, or interrupted AI work is silently resumed/discarded
- failure handling / replay expectation: capture verification artifact and replay a fix from a feature worktree

### Post-merge end-to-end dogfood acceptance

- environment: `develop` protected verification worktree
- evidence: Freely uses the new project command contract during its own runtime lifecycle handling
- failure signal: dogfood run reintroduces mixed project/global blast radius or ambiguous restore-work behavior
- failure handling / replay expectation: reopen as new follow-on lifecycle rather than mutating this finished issue in place

## Execution Slices

1. CLI surface and routing slice for `restart`, `start --force`, `restore-work`
2. Project-local repair ordering slice
3. Safe repair set enforcement slice
4. Continuity-anchor-based restore-work slice
5. Focused regression and governance writeback slice

## Revisit Triggers

1. global action surface needs to own some behavior currently frozen as project-local
2. interrupted AI restore requires different mandatory anchors than the current taxonomy
3. process identity anchor changes away from `--project/-C + pidfile + cwd fallback`
4. live incidents show project force still has cross-project blast radius

## Dev-Loop Handoff

- implement against `docs/B2-docs/ibm/project-command-semantics-and-restore-work-governance/pre-tests.md`
- keep downstream `global-restart-restore-memory-governance` blocked on this contract, not vice versa
- write progress only once implementation starts
