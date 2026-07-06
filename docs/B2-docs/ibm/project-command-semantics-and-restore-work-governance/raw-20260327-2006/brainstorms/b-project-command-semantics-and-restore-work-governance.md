# Brainstorm: project-command-semantics-and-restore-work-governance

## Frozen boundary

- 本 issue 只拥有单项目 command family：
  - `freely start`
  - `freely stop`
  - `freely restart`
  - `freely start --force`
  - `freely restore-work`
- future global `stop/restart/reset` 是独立 all-project control-plane action，不是 project force 的别名。

## Mandatory carry-over truth

- `cmd_stop()` 已具备 project-scoped pid ownership truth，可作为 lower-layer supporting fact。
- `cmd_start()` 当前仍缺 attach-vs-repair-vs-fail-fast contract，需要在本 issue 冻结。
- process discovery / kill scope 必须继续依赖 project anchor：pidfile、`--project/-C` command line、cwd fallback。
- interrupted local AI work 默认不得在 project restart 中 silent resume。
- explicit AI-work restore 优先作为 dedicated `restore-work` surface；flag alias 只可次级存在。

## Open implementation questions for dev-loop

1. `restart` 与 `start --force` 的 CLI surface 如何表达而不与 `init --force` 混层。
2. safe repair set 如何映射到 `.freely/run/` 下的具体 artifact 处理顺序。
3. `restore-work` 入口如何消费 continuity / interruption / intake evidence，而不把 auxiliary artifacts 提升成 mandatory restore anchors。

## Downstream handoff

- `global-restart-restore-memory-governance` 只能消费本 issue 已冻结的 taxonomy / restore-anchor boundary。
- 若 dev-loop 发现 command blast radius 仍需重新拆 owner，回到 source candidate，而不是在下游 global issue 中补救。
