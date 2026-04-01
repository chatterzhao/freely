# Pre-Tests: multi-tool-availability-manager-governance

## Acceptance Contract

1. 新项目 config 默认写出 `AUTO_SWITCH_SLOT=false`、`AUTO_SWITCH_TOOL=false`、`AI_FALLBACK_TOOLS=""`，并保持 `AI_TOOL` 仍是 active tool pointer。
2. `ensure-manager` 会重新读取 project config，不依赖旧进程启动时缓存的 `AI_TOOL`。
3. 当当前工具具备 canonical same-tool recovery truth 时，control plane 必须先走同工具恢复，再考虑 cross-tool fallback。
4. 当当前工具 tool-local failure 或 same-tool recovery exhausted 且 `AUTO_SWITCH_TOOL=true` 时，control plane 会按 `AI_FALLBACK_TOOLS` 顺序挑选下一个可用工具，而不是硬编码 `codex`。
5. 每次跨工具 fallback 必须显式记录 `launch_kind=fresh_with_handoff`，不得冒充 resume。
6. 若所有配置中的工具都不可用，`ensure-manager` 仍保持 no-launch，并显式记录 earliest-reset hint。
7. 当 auto-switch 未开启时，Kiro availability failure 仍应保持“本地 stop + defer control plane”的旧 contract。

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
   - 锁住兼容性路径：Kiro tool-local failure 仍能在 order 中选到 Codex
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
   - 锁住 fallback 会继续扫描配置顺序，而不是把 Codex 硬编码成唯一 target
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
   - 锁住 Codex 先 same-tool recovery，穷尽后才 cross-tool
4. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
   - 锁住 all-tools-unavailable 时 no-launch 与 earliest-reset waiting truth
5. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
   - 锁住 auto-switch 未开启时，Kiro availability failure 仍只 stop/defer，不在本地 blind relaunch

## Regression Risks

1. `ensure-manager` 如果不 reload config，watchdog 进程会继续持有旧的 `AI_TOOL=kiro-cli`，导致 config 改了也不生效。
2. 如果把 `tools.md` 优先级直接当成 fallback order，routing truth 与 runtime availability truth 会再次混淆。
3. 如果 cross-tool fallback 没有强制 `fresh_with_handoff`，会把不同 continuity class 的工具误当成可 resume 等价物。
