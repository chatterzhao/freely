# PRD: codex-verified-resume-evidence-governance

## Goal

让 Freely 只在 `codex` 具有可追溯 rollout/jsonl 证据时才执行下一轮 `resume`，避免把弱观察到的 `session_id` 误当成可恢复事实。

## Why Now

- canonical `develop` 已真实出现 `session_id` 可见、`jsonl_path=unavailable`、随后连续无效 `resume` 的链条
- 同一个 thread id 在隔离工位中可直接复现 `no rollout found for thread id`
- 当前系统同时还能看到带真实 `jsonl_path` 的健康 `resume`
- 所以这是一个可分离、可验证、不能靠广义猜测修复的恢复证据问题

## Product Surface

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-explicit-resume-target-contract`
- `docs/system/workspace/scripts/tests/test-freely-session-rotation`
- any new focused regression needed for invalid resume evidence

## Non-Goals

- 不改 auth/watchdog account recovery contract
- 不改 `live-status` / fleet observability surface
- 不把 cross-tool shared resolver 当成本 issue 的前置条件

## Non-Negotiables

- `codex` 的健康 explicit `resume` 能力不能退化
- `session_id` 不能单独自动成为强 resume evidence
- runtime 必须显式区分：
  - observed session hint
  - persistable continuity state
  - resumable target
- 当 evidence 不够强时，默认降级到 non-resume recovery，而不是继续撞同一个坏 id

## Context Pack

- field evidence:
  - `.freely/logs/runtime-events.log:328-335` on `develop`
- isolated reproduction:
  - `.freely/logs/invalid-resume-direct.log` in repro worktree
- healthy contrast:
  - later `develop` runtime events show valid `session_id + jsonl_path` pairs on successful resume cycles
- current runtime helpers involved:
  - `extract_tool_session_id_from_log()`
  - `find_codex_jsonl_path_for_session()`
  - `tool_runtime_resume_target_after_cycle()`
  - `tool_has_resume_evidence()`

## Decomposition Tree

1. freeze the proven codex-only evidence boundary
2. define the downgrade path for session-id-only false positives
3. add regression coverage before widening abstraction
4. audit later whether any shared explicit-session tool helper should be extracted

## Eval Plan

成功：

- the false-positive `session_id`-only case stops selecting `resume`
- a valid rollout-backed `codex` session still selects `resume`
- restart-storm churn from the reproduced invalid target no longer occurs through this path

失败：

- runtime still treats non-empty `resume_target` as enough
- invalid target still re-enters `resume`
- valid target gets over-downgraded to fresh unnecessarily

不可接受退化：

- removing explicit resume entirely
- coupling this fix to auth/watchdog changes
- shipping a codex-specific field fix that hides the reason and cannot be tested deterministically
