# Issue: multi-tool-auto-switch-v1-codex-fallback-governance

- issue_id: `I-20260331-1840-A`
- title: Multi-tool availability manager governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `multi-tool-auto-switch-v1-codex-fallback-governance`
- issue-name: `multi-tool-auto-switch-v1-codex-fallback-governance`
- source_candidate: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md#c-20260331-1840-a`
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 最早的 availability-manager 研究和 `20260331-1840` brainstorm 都要求同一条恢复状态机：

- 先做当前工具内部的 slot / profile family 恢复
- 当前工具 exhausted 后，再按项目定义的工具顺序尝试下一个工具
- 所有工具都不可用时，保持 no-launch，并把最早恢复提示写成显式控制面真相

后来物化时把这条 contract 收窄成了 `kiro-cli -> codex` bridge。当前 owner 要把它抬回原始设计，但保留 Codex watchdog 的 probe-first / shared-lock / no-launch invariants。

## Scope

1. 冻结 runtime-owned availability config：`AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS`。
2. 保持 `AI_TOOL` 仍是 active tool pointer，但把 `AI_FALLBACK_TOOLS` 变成真正的 ordered recovery list，而不是单一 target hint。
3. 保持 same-tool automatic recovery 优先于 cross-tool fallback；当前已有 canonical truth 的 `codex` 必须先走既有 watchdog contract。
4. 让 `ensure-manager` 在当前工具 exhausted 或 tool-local failure 后，按配置顺序尝试下一个工具，而不是只做 `kiro-cli -> codex`。
5. 当所有工具都不可用时，保持 no-launch，并把 earliest-reset target 写成 machine-readable control-plane truth。
6. 冻结 cross-tool continuity downgrade：一律强制 `fresh_with_handoff`，不保留 resume 语义。

## Non-Goals

1. 不把 `tools.md` 的任务路由优先级直接复用成 runtime fallback order。
2. 不把 host/network-global failures 误当成 cross-tool fallback 触发器。
3. 不要求所有工具在本轮都拥有和 Codex 等价的 probe/slot truth；能力缺口要显式标注，不能假装等价。
4. 不把 worker lane 或完整结构化 tool-group config 文件迁移一起塞进本 owner。

## Acceptance

1. `write_config()` 为新项目写出 `AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS` 默认字段。
2. `ensure-manager` 每轮都重新读取 project config，因此 control plane 可以消费最新 active tool truth。
3. 当当前工具具备 canonical same-tool recovery truth 时，control plane 必须先走同工具恢复；Codex 继续受既有 watchdog readiness gate 约束。
4. 若 same-tool recovery exhausted，且 `AUTO_SWITCH_TOOL=true`，`ensure-manager` 会按 `AI_FALLBACK_TOOLS` 的顺序尝试下一个工具，而不是硬编码 `codex`。
5. cross-tool fallback 一旦开始，扫描总是从 `AI_FALLBACK_TOOLS` 最左侧重新开始；current tool 只作为 active pointer / same-tool recovery truth，不会被隐式插回 fallback 顺序最前。
6. cross-tool fallback 必须显式记录 `previous_tool`、`active_tool`、`reason` 与 `launch_kind=fresh_with_handoff`。
7. 当所有配置中的工具都不可用时，manager launch 继续 blocked，并写出 machine-readable waiting event 与 earliest-reset hint。
8. 现有 Kiro defer contract 不回退：当 auto-switch 未开启时，runtime 仍在本地 stop 并 defer 给 control plane。
9. cleanup-time one-shot `ensure-manager` recheck 若撞到旧 supervisor 正在退出的窗口，必须先等待 teardown 完成，再进入 fallback selection / relaunch；不能把 exiting supervisor 误判成“already running”。

## Completion

- `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md`
- `docs/milestones.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- `docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
- live validation on `develop` with ordered fallback enabled and at least one non-current tool available

## Verification

- Focused regressions:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
  - `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
  - `bash docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
- Governance:
  - `./bin/governance-check`
- Live repro:
  - Start on `develop`, force current-tool unavailability, and verify manager control plane first consumes same-tool recovery truth, then walks the configured fallback order, and finally emits waiting truth instead of blind relaunch when every tool is unavailable
  - Guard the live Kiro launch path from stale default-model drift: when `AI_MODEL` is empty, Kiro launcher must fall back to a supported model instead of aborting before availability recovery can classify the cycle
  - Guard the cleanup/recheck boundary from false `already_running_attach`-style attach reuse: if cleanup has already written `desired=running + supervisor=down + ai=down`, the one-shot recheck must wait for the old supervisor to disappear before deciding whether fallback or relaunch is needed

## Next

- `2026-04-01 09:55 PDT` ordered fallback v1 is closed: canonical `develop` now carries the left-to-right fallback list, Kiro default-model repair, and teardown-aware recheck required for the bounded v1 contract.
- Follow-on work stays out of scope here:
  - per-tool same-tool probe parity belongs to new per-tool capability lifecycles
  - all-tools slot parity already moved to and closed under `I-20260401-0840-A`
  - cross-tool resume equivalence still requires a separate lifecycle
