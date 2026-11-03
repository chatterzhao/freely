# PRD: 平台 handler 探活缓存与执行守卫

- issue_id: I-20261102T130603Z-A

## Goal
让 PR 入口不再因一次网络探活抖动抛 `AttributeError`；同一进程内 handler 探活只付一次网络成本，失败以可执行的平台级 error 呈现。

## Modules
- `docs/system/workspace/scripts/sync/platform-adapter.py`
  - `_HANDLER_PROBE_CACHE` + `_probe_handler()`：成功缓存、失败不缓存、`_retry_read` 有界重试。
  - `_handler_for()` 改为调用 `_probe_handler()`；`_discover_one` 移除重复 retry。
  - `_ensure_handler()`：None 时返回 `{'status':'error','stage':'execute','error':'platform handler unavailable: <platform>'}`。
  - `guarded_pr_update()` 执行循环使用 `_ensure_handler`，error 时写入平台结果并 continue。
- `docs/system/workspace/scripts/tests/test-platform-handler-probe.py`（新）：缓存计数 / 重试恢复 / 结构化错误。

## Invariants
- 探活失败不缓存，后续调用仍可恢复。
- 多平台循环中某平台不可用不得中断其它平台结果收集。
- 不改变 PR gate 的阻断语义（失败仍阻断，但错误结构化）。

## Non-Goals
- 不改各平台 handler 的 detect 实现。
- 不改 `configured_platforms()` 与平台注册表。
- 不做跨进程缓存。

## Eval Plan
- unit：`test-platform-handler-probe.py`。
- integration：`guarded_pr_update` 在 handler 不可用时返回结构化 error（单测覆盖 execute 路径）。
- end-to-end：本分支自身 guarded PR/merge receipts（not_applicable 由真实链路替代）。

## Dev-Loop Handoff
先写 RED（缓存/重试/结构化错误三组断言），再实现 `_probe_handler`/`_ensure_handler` 并接入 `guarded_pr_update`。
