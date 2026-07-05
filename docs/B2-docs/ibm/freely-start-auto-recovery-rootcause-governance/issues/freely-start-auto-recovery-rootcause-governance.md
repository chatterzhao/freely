# Issue: freely-start-auto-recovery-rootcause-governance

- issue_id: `I-20260414-0255-A`
- title: `Freely start codex after-failure recovery honors saved-slot order`
- phase_state: `completed`
- completed_at: `2026-04-28`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `freely-start-auto-recovery-rootcause-governance`
- issue-name: `freely-start-auto-recovery-rootcause-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260414/candidates.md#c-20260414-0255-a`
- source_brainstorm: `docs/B1-docs/raw-20260414/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-freely-start-auto-recovery-rootcause-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/freely-start-auto-recovery-rootcause-governance/code-reviews`
- depends_on:
  - `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
  - `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

真实 `freely start` 重放已经把这条 lane 的问题收敛到一个更窄、更准确的根因：

1. `codex` 运行期 after-failure same-tool recovery 仍复用了 cached-ready 选择器。
2. 该选择器会先看 availability cache，于是像 `worahe1012`、`a1018-1` 这样的 saved slot 可能在真正执行前就被跳过。
3. 一旦 inner loop 先跳号，现场就会伪装成 “failure type 判断错了” 或 “应该分 limit/network/auth 多种切法”，但那不是根因。
4. 正确合同只有一条：任何触发切号的失败都走统一切号方法；在同工具内部，先切到当前后的下一个 saved slot 并真正执行，直到 same-tool 耗尽后再交给跨工具外循环。

## Scope

1. 修正 `codex` after-failure recovery 的 next-slot 语义，让它严格按 saved-slot 顺序前进。
2. 保留 cached-ready 探测给非 after-failure readiness 场景使用，不把它继续误用到真实失败后的切号。
3. 保持统一切号方法和既有外循环顺序；不重新按错误类型拆多套切号实现。
4. 用 focused regressions、真实坏号 replay、以及正常可用号 replay 证明 Freely 能从坏号切到可用号并继续做任务。

## Non-Goals

1. 不重写跨工具优先级或 slot inventory 设计。
2. 不把手工 `switch` 下的 `hi` 探测规则和 runtime 实际工作态失败探测混成一条逻辑。
3. 不把其他独立 runtime 问题塞进这条 owner。
4. 不在 protected branch 上补实现；所有实现与文档纠偏都留在 dedicated feature worktree 完成。

## Root Cause

**最佳根因：`codex` 运行期 after-failure recovery 误用了 cache-filtered ready-slot 选择器，导致 saved codex slots 会在真实执行前被跳过；这破坏了预期的 same-tool inner loop，并把问题伪装成 failure label / error taxonomy 争议。**

## Implementation Fix

1. `tool_select_ready_slot_for_manager_auto_recovery()` 在 `codex + after_failure` 模式下改为直接走 `switch_to_next_codex_slot(... after_failure_exec_recovery_next_slot)`。
2. `select_next_codex_slot()` 保持给 cached-ready 路径使用，但语义收紧为严格向后选择，不再尾部回绕。
3. 新增 `select_next_codex_saved_slot()`，供 `switch_to_next_codex_slot()` 在 after-failure 场景下忽略 availability cache，只按 saved-slot 顺序挑下一个。
4. same-tool codex slots 耗尽后，继续沿既有 cross-tool 外循环推进；不新增第二套切号机制。

## Acceptance

1. 真实坏号起步时，`freely start` 会在 codex 内部按 saved-slot 顺序逐个执行，而不是跳过中间 slot。
2. 对任意 runtime 实际工作失败，只要命中失败触发条件，就走统一切号方法；不会因 failure label 不同而切不同逻辑。
3. same-tool codex slots 全部失败后，Freely 会按既有工具优先级继续外循环，不会在 codex 内部无界回绕。
4. 切到当前可用号后，Freely 能继续领取/完成任务；这次 feature lane 已在真实环境生成 `healthcheck14.txt` 与 `healthcheck15.txt`。
5. runtime 停止后保持停止，不让验证过程空转消耗 token。

## Verification

- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-codex-after-failure-next-slot-ignores-availability-cache`
- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-codex-select-next-slot-does-not-wrap`
- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-codex-after-failure-uses-next-slot-not-probe`
- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-codex-after-failure-next-slot-ignores-availability-cache`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-codex-select-next-slot-does-not-wrap`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-codex-after-failure-uses-next-slot-not-probe`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `./bin/governance-check`

## Current Evidence

1. 真实坏号 replay 已证明同工具 codex 顺序遍历从 `worahe1000 -> worahe1001 -> worahe1002 -> worahe1012 -> a1018-1 -> a1018-2 -> a1019-1`，不再提前跳过 saved slot。
2. 当前可用号 replay 已证明切到 `a1020-1` 后，`freely start` 可以正常续跑并完成 `healthcheck14` / `healthcheck15`。
3. runtime 目前已人工停止，避免 token 空转；后续只剩 develop promote 与 post-merge followthrough。

## Closeout

1. 先让 feature lane 携带正确 candidate/issue/pre-tests/review 真相通过 guarded promote。
2. 再在 `develop` 做 post-merge followthrough：确认当前可用号能继续自动做任务。
3. followthrough 通过后，立即 retire `test-pre-merge-*` 与 feature worktree。
