# Brainstorm: global-restart-restore-memory-governance

## Frozen boundary

- 本 issue 只拥有 all-project global restart 的 restore memory 与 manifest durability。
- project command blast radius、safe repair set、`restore-work` default 已由 `I-20260327-2006-A` 冻结，不在这里重判。

## Mandatory carry-over truth

- global restart manifest home: `$FREELY_HOME/control-plane/restart/{latest.json,history/<timestamp>.json}`
- retention: keep `latest.json` plus last 20 history files
- mandatory restore anchors:
  - `workcell-state.env`
  - `manager-worker-launch-state.env`
  - continuity artifacts
  - interruption resolutions
  - delegated prompt evidence
  - `.freely/intake/**`
- auxiliary evidence:
  - `session-state.env`
  - `session-handoff.txt`
  - pid files
  - stop marker
  - restart-storm window
  - `codex-slot-cooldowns.tsv`

## Open implementation questions for dev-loop

1. manifest required fields 如何编码 previously-running set、operator-stopped exclusion 与 restore outcome history。
2. global restart 如何与 current live-status / fleet-status truth 对齐。
3. retention 与 corruption recovery 如何设计，才能让 `latest.json` 与 history 共存而不污染恢复路径。

## Downstream guard

- 若 dev-loop 发现需要改变 project command blast radius，必须回到 `I-20260327-2006-A` 或 source candidate，不得在本 issue 内偷偷扩权。
